#!/usr/bin/env python3
"""Build a one-shot commit payload for GitHub's "Upload files" page.

Why this exists: the AI that maintains this repository works through the owner's signed-in Chrome (no git credentials,
no API token — see AI_BRIEF.md §3). GitHub's upload page (https://github.com/<repo>/upload/<branch>/<dir>) accepts
files from a script, so a commit is: edit files locally, run this tool, open the upload page in Chrome, run the payload
with the browser's JavaScript tool, done. The payload is self-checking: it fetches the live file at commit time, applies
exact text hunks, compares the SHA-1 of the result with the local file and throws (nothing is staged) on any mismatch —
a stale copy can never produce a wrong commit. New files are sent whole.

Usage
  python3 tools/upload_payload.py --dir pipeline --summary "..." --description "..." --out payload.js research.py qc.py
  python3 tools/upload_payload.py --dir "" --summary "..." --out payload.js WEEKLY_PASS.md audit_overrides.json
  python3 tools/upload_payload.py --check --dir pipeline research.py        # only verify the hunks apply to live main

Then in Chrome: navigate to the URL the tool prints, run the payload text with the JavaScript tool. It returns
{shas, listed, before, after, how}; `after` different from `before` (or a "target navigated" error) means the commit
was submitted. Verify with: curl -s https://raw.githubusercontent.com/<repo>/<branch>/<dir>/<file>?nc=1 | sha1sum.
"""
import argparse, difflib, hashlib, json, os, random, sys, urllib.request

def fetch(url):
    req = urllib.request.Request(url + ("&" if "?" in url else "?") + f"nc={random.random()}", headers={"Cache-Control": "no-cache", "User-Agent": "upload_payload/1"})
    try:
        return urllib.request.urlopen(req, timeout=40).read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def hunks(old, new):
    """Minimal unique text replacements that turn old into new (merged ops with enough context to be unique)."""
    a, b = old.splitlines(keepends=True), new.splitlines(keepends=True)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
    groups = []
    for op in ops:
        if groups and op[1] - groups[-1][-1][2] <= 3:
            groups[-1].append(op)
        else:
            groups.append([op])
    out = []
    for g in groups:
        i1, j1, i2, j2 = g[0][1], g[0][3], g[-1][2], g[-1][4]
        ctx = 1
        while True:
            ai, aj = max(0, i1 - ctx), min(len(a), i2 + ctx)
            o = "".join(a[ai:aj]); n = "".join(b[j1 - (i1 - ai):j2 + (aj - i2)])
            if old.count(o) == 1 or ctx > 40:
                break
            ctx += 1
        if old.count(o) != 1:
            raise SystemExit(f"cannot make a unique hunk at line {i1}; send the whole file instead (--whole)")
        out.append([o, n])
    return out

def sha_tail(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[-8:]

JS = r"""
await new Promise(r=>setTimeout(r,2000));
window.__addFiles = function(files){ const input=document.getElementById('upload-manifest-files-input'); if(!input) throw new Error('not on the upload page'); const dt=new DataTransfer(); for(const [name,content] of files){ dt.items.add(new File([content], name, {type:'text/plain'})); } input.files=dt.files; input.dispatchEvent(new Event('change',{bubbles:true})); return input.files.length; };
const sha=async s=>{const h=await crypto.subtle.digest('SHA-1', new TextEncoder().encode(s)); return [...new Uint8Array(h)].map(b=>b.toString(16).padStart(2,'0')).join('').slice(-8)};
const get=async p=>{const r=await fetch(__BASE__+p+'?nc='+Math.random(),{cache:'no-store'}); if(!r.ok) throw new Error('fetch '+p+' '+r.status); return await r.text();};
const P = __P__;
const FULL = __FULL__;
const EXPECTED = __EXPECTED__;
const out = {}; const files = []; const bad = [];
for (const [f, pairs] of Object.entries(P)) { let t = await get(f); for (const [o,n] of pairs) { const k = t.split(o).length - 1; if (k !== 1) throw new Error(f + ' hunk count ' + k + ' :: ' + o.slice(0,40)); t = t.replace(o, () => n); } const h = await sha(t); out[f] = h; if (h !== EXPECTED[f]) bad.push(f); files.push([f, t]); }
for (const [f, t] of Object.entries(FULL)) { const h = await sha(t); out[f] = h; if (h !== EXPECTED[f]) bad.push(f); files.push([f, t]); }
if (bad.length) throw new Error('sha mismatch: ' + bad.join(',') + ' ' + JSON.stringify(out));
window.__addFiles(files);
await new Promise(r=>setTimeout(r,3000));
const setVal=(el,v)=>{const proto=el.tagName==='TEXTAREA'?HTMLTextAreaElement.prototype:HTMLInputElement.prototype; const d=Object.getOwnPropertyDescriptor(proto,'value'); d.set.call(el,v); el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));};
const s=document.getElementById('commit-summary-input'); setVal(s, __SUMMARY__);
const d=document.getElementById('commit-description-textarea')||document.querySelector('textarea[name="commit-description"]'); if(d){ setVal(d, __DESC__); }
const btnOf=()=>[...document.querySelectorAll('button')].find(b=>/commit changes/i.test(b.textContent||''));
const listedOf=()=>document.querySelector('main').innerText.split('\n').filter(l=>/\.[A-Za-z0-9]{1,6}$/.test(l.trim()));
let btn=null, listed=[]; const want = files.length;
for (let i=0;i<40;i++){ await new Promise(r=>setTimeout(r,1500)); btn=btnOf(); listed=listedOf(); if(btn && !btn.disabled && listed.length>=want) break; }
if(!btn) throw new Error('no commit button; listed='+listed.join(','));
if(btn.disabled) throw new Error('commit button still disabled; listed='+listed.join(','));
if(listed.length < want) throw new Error('listed only '+listed.join(','));
if(s.value.length < 10) throw new Error('summary empty');
btn.scrollIntoView({block:'center'}); await new Promise(r=>setTimeout(r,500));
const rect=btn.getBoundingClientRect(); const before=location.href;
btn.click(); await new Promise(r=>setTimeout(r,4000));
let how='click';
if(location.href===before && document.contains(btn) && !btn.disabled){ try{ btn.form.requestSubmit(btn); how='requestSubmit'; }catch(e){ how='requestSubmit failed '+e.message; } await new Promise(r=>setTimeout(r,5000)); }
({shas: out, listed, rect:[Math.round(rect.x+rect.width/2), Math.round(rect.y+rect.height/2)], before, after: location.href, how})
"""

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", help="file names relative to --dir")
    ap.add_argument("--repo", default="DANCEATLAS/crawler")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--dir", default="", help="directory inside the repo (e.g. pipeline); '' for the root")
    ap.add_argument("--local", default=".", help="local working copy root (files are read from <local>/<dir>/<file>)")
    ap.add_argument("--summary", default="")
    ap.add_argument("--description", default="")
    ap.add_argument("--out", default="payload.js")
    ap.add_argument("--whole", action="store_true", help="send every file whole (no hunks); the sha check still applies")
    ap.add_argument("--check", action="store_true", help="only verify that the hunks apply to the live files")
    args = ap.parse_args()
    d = args.dir.strip("/")
    base = f"https://raw.githubusercontent.com/{args.repo}/{args.branch}/" + (d + "/" if d else "")
    P, FULL, EXPECTED = {}, {}, {}
    for f in args.files:
        local_path = os.path.join(args.local, d, f) if d else os.path.join(args.local, f)
        local = open(local_path, encoding="utf-8").read()
        remote = fetch(base + f)
        EXPECTED[f] = sha_tail(local)
        if remote is None or args.whole:
            FULL[f] = local
            print(f"{f}: {'new file' if remote is None else 'whole file'} ({len(local)} chars) sha {EXPECTED[f]}")
            continue
        if remote == local:
            print(f"{f}: identical to live {args.branch}; skipped")
            continue
        hs = hunks(remote, local)
        t = remote
        for o, n in hs:
            assert t.count(o) == 1
            t = t.replace(o, n)
        assert t == local, f"{f}: patched text != local"
        P[f] = hs
        print(f"{f}: {len(hs)} hunk(s) sha {EXPECTED[f]}")
    if args.check:
        print("check passed: every hunk applies to live", args.branch)
        return
    if not P and not FULL:
        raise SystemExit("nothing to commit")
    if not args.summary:
        raise SystemExit("--summary is required for a payload")
    import re
    fill = {"__BASE__": json.dumps(base), "__P__": json.dumps(P, ensure_ascii=False), "__FULL__": json.dumps(FULL, ensure_ascii=False),
            "__EXPECTED__": json.dumps(EXPECTED), "__SUMMARY__": json.dumps(args.summary), "__DESC__": json.dumps(args.description)}
    # one pass over the template only: inserted file contents are never re-scanned (this very file contains the markers)
    js = re.sub(r"__(?:BASE|P|FULL|EXPECTED|SUMMARY|DESC)__", lambda m: fill[m.group(0)], JS)
    open(args.out, "w", encoding="utf-8").write(js)
    print(f"wrote {args.out} ({len(js)} chars)")
    print(f"open in Chrome: https://github.com/{args.repo}/upload/{args.branch}/{d}".rstrip("/"))
    print("then run the payload text with the JavaScript tool on that tab; 'after' != 'before' (or a 'target navigated' error) = submitted")

if __name__ == "__main__":
    main()

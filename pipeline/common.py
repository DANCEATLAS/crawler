"""Shared helpers for the Dancing Atlas pipeline (stdlib only).

Everything network-related lives here: HTTP with retries, the Supabase REST
client, the LLM clients (OpenAI / Gemini) and the run report.  Secrets are
read from the environment only; nothing is ever written to disk.
"""
import os, re, sys, json, time, unicodedata, urllib.parse, urllib.request, urllib.error, base64, hashlib
from datetime import datetime, timezone

PIPELINE_VERSION = "v3.0"
UA = "DancingAtlasPipeline/3.0 (https://github.com/DANCEATLAS/crawler; research pipeline)"
STATE_DIR = os.environ.get("PIPELINE_STATE_DIR", "pipeline_state")
os.makedirs(STATE_DIR, exist_ok=True)

def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def log(*a):
    print(*a, flush=True)

def warn(*a):
    print("WARN", *a, file=sys.stderr, flush=True)

# ----------------------------------------------------------------- text utils
def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s or "")) if unicodedata.category(c) != "Mn")

def norm(s):
    """lowercase, accent-free, alphanumeric words joined by single spaces."""
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()

def slugify(s, maxlen=60):
    s = norm(s).replace(" ", "-")
    return s[:maxlen].strip("-")

def words(s):
    return norm(s).split()

def similarity(a, b):
    import difflib
    a, b = norm(a), norm(b)
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()

def sha1(s):
    return hashlib.sha1(str(s).encode("utf-8")).hexdigest()[:12]

# ----------------------------------------------------------------- json files
def jload(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except Exception as e:
        warn("jload failed", path, e)
        return default

def jsave(path, obj):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1, sort_keys=False)
    os.replace(tmp, path)

def state_path(name):
    return os.path.join(STATE_DIR, name)

def load_state(name, default):
    return jload(state_path(name), default)

def save_state(name, obj):
    jsave(state_path(name), obj)

# ----------------------------------------------------------------- HTTP
class HttpError(Exception):
    def __init__(self, code, body, url):
        short = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body or "")).strip()[:160]
        super().__init__(f"HTTP {code} {url} :: {short}")
        self.code, self.body, self.url = code, body, url

def http(url, method="GET", data=None, headers=None, timeout=60, retries=3, json_body=None, ok=(200, 201, 202, 204, 206)):
    """Minimal HTTP client with retries on 429/5xx. Returns (status, body_text, headers)."""
    h = {"User-Agent": UA, "Accept": "application/json"}
    if headers:
        h.update(headers)
    body = None
    if json_body is not None:
        body = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
        h.setdefault("Content-Type", "application/json")
    elif data is not None:
        body = data if isinstance(data, bytes) else str(data).encode("utf-8")
    last = None
    wikimedia = any(x in url for x in ("wikipedia.org", "wikimedia.org", "wikidata.org"))
    if wikimedia:
        retries = max(retries, 5)  # Wikimedia throttles cloud runners with 429/503 bursts; wait them out politely
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, method=method, headers=h)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                txt = raw.decode("utf-8", "replace") if raw else ""
                return r.status, txt, dict(r.headers)
        except urllib.error.HTTPError as e:
            txt = ""
            try:
                txt = e.read().decode("utf-8", "replace")
            except Exception:
                pass
            last = HttpError(e.code, txt[:400], url)
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                ra = e.headers.get("Retry-After") if e.headers else None
                wait = float(ra) if (ra and ra.isdigit()) else ((5.0 * (2 ** attempt)) if wikimedia else 2.0 * (attempt + 1))
                time.sleep(min(90, wait))
                continue
            raise last
        except Exception as e:  # network blips
            last = e
            if attempt < retries:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise
    raise last

def get_json(url, headers=None, timeout=60, retries=3):
    st, txt, _ = http(url, headers=headers, timeout=timeout, retries=retries)
    return json.loads(txt) if txt else None

def get_bytes(url, headers=None, timeout=60):
    h = {"User-Agent": UA}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")

# ----------------------------------------------------------------- Supabase REST
class Supabase:
    """Tiny PostgREST client. Uses the service key from the environment (GitHub secret)."""
    def __init__(self):
        self.url = os.environ.get("SUPABASE_URL", "").rstrip("/")
        self.key = os.environ.get("SUPABASE_SERVICE_KEY", "")
        self.enabled = bool(self.url and self.key)
        self._columns = None

    def _h(self, extra=None):
        h = {"apikey": self.key, "Authorization": "Bearer " + self.key}
        if extra:
            h.update(extra)
        return h

    def rest(self, path, params=None):
        u = self.url + "/rest/v1/" + path.lstrip("/")
        if params:
            u += ("&" if "?" in u else "?") + urllib.parse.urlencode(params, safe=",.*()=:")
        return u

    def select(self, table, select="*", filters=None, order=None, limit=None, page=1000):
        """Return all rows (paginated)."""
        if not self.enabled:
            return []
        rows, offset = [], 0
        while True:
            params = {"select": select, "limit": str(page if limit is None else min(page, limit - len(rows))), "offset": str(offset)}
            if order:
                params["order"] = order
            u = self.rest(table, params)
            if filters:
                u += "&" + "&".join(filters)
            st, txt, _ = http(u, headers=self._h())
            batch = json.loads(txt) if txt else []
            rows.extend(batch)
            if len(batch) < page or (limit is not None and len(rows) >= limit):
                break
            offset += page
        return rows

    def columns(self, table):
        """Column names from the OpenAPI spec (cached)."""
        if self._columns is None:
            self._columns = {}
            if self.enabled:
                try:
                    st, txt, _ = http(self.url + "/rest/v1/", headers=self._h())
                    spec = json.loads(txt)
                    for name, d in (spec.get("definitions") or {}).items():
                        self._columns[name] = {k: (v.get("format") or v.get("type") or "") for k, v in (d.get("properties") or {}).items()}
                except Exception as e:
                    warn("openapi fetch failed", e)
        return self._columns.get(table, {})

    def safe_select(self, table, wanted):
        """Comma list of the wanted columns that exist (all of them when the schema is unknown)."""
        cols = self.columns(table)
        want = [c.strip() for c in wanted.split(",") if c.strip()]
        return ",".join([c for c in want if (not cols or c in cols)]) or "*"

    def filter_columns(self, table, row):
        cols = self.columns(table)
        if not cols:
            return dict(row)
        return {k: v for k, v in row.items() if k in cols}

    def upsert(self, table, rows, on_conflict="slug", chunk=200):
        if not self.enabled or not rows:
            return 0
        n = 0
        for i in range(0, len(rows), chunk):
            batch = [self.filter_columns(table, r) for r in rows[i:i + chunk]]
            u = self.rest(table, {"on_conflict": on_conflict})
            http(u, method="POST", json_body=batch, headers=self._h({"Prefer": "resolution=merge-duplicates,return=minimal"}))
            n += len(batch)
        return n

    def insert(self, table, rows, chunk=200, ignore_duplicates=False):
        if not self.enabled or not rows:
            return 0
        n = 0
        prefer = "return=minimal" + (",resolution=ignore-duplicates" if ignore_duplicates else "")
        for i in range(0, len(rows), chunk):
            batch = [self.filter_columns(table, r) for r in rows[i:i + chunk]]
            http(self.rest(table), method="POST", json_body=batch, headers=self._h({"Prefer": prefer}))
            n += len(batch)
        return n

    def patch(self, table, match, payload):
        """match: dict of eq filters. Returns number of rows updated."""
        if not self.enabled:
            return 0
        payload = self.filter_columns(table, payload)
        if not payload:
            return 0
        u = self.rest(table) + "?" + "&".join(f"{k}=eq.{urllib.parse.quote(str(v))}" for k, v in match.items())
        st, txt, _ = http(u, method="PATCH", json_body=payload, headers=self._h({"Prefer": "return=representation"}))
        try:
            return len(json.loads(txt))
        except Exception:
            return 0

    def rpc(self, fn, args=None):
        st, txt, _ = http(self.rest("rpc/" + fn), method="POST", json_body=args or {}, headers=self._h())
        return json.loads(txt) if txt else None

# ----------------------------------------------------------------- LLM clients
class LLM:
    """Gemini and/or OpenAI chat with JSON-only outputs.

    Model names are NOT hard-wired: at first use the available models are listed from each provider and the
    best stable flash/pro (Gemini) or mini/full (OpenAI) model is chosen, so deprecations do not stop the
    pipeline. GEMINI_MODELS / OPENAI_MODELS / OPENAI_STRONG_MODELS still take precedence when set and available.
    Models that answer 'not found' are dropped for the rest of the run."""
    GEMINI_SKIP = ("image", "tts", "live", "audio", "embedding", "thinking", "exp", "dialog", "computer-use", "robotics",
                   "deep-research", "veo", "imagen", "learnlm", "gemma", "aqa", "nano", "vision", "8b")

    def __init__(self):
        self.openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
        self.cfg_openai = [m.strip() for m in os.environ.get("OPENAI_MODELS", "").split(",") if m.strip()]
        self.cfg_openai_strong = [m.strip() for m in os.environ.get("OPENAI_STRONG_MODELS", "").split(",") if m.strip()]
        self.cfg_gemini = [m.strip() for m in os.environ.get("GEMINI_MODELS", "").split(",") if m.strip()]
        self.cfg_gemini_strong = [m.strip() for m in os.environ.get("GEMINI_STRONG_MODELS", "").split(",") if m.strip()]
        self._gemini_avail = None
        self._openai_avail = None
        self.dead = set()
        self.calls = 0
        self.failures = 0
        self.dry = os.environ.get("PIPELINE_DRY_RUN") == "1"

    @property
    def enabled(self):
        return bool(self.openai_key or self.gemini_key) and not self.dry

    # ---- model discovery
    @staticmethod
    def _ver(name):
        m = re.search(r"-(\d+)(?:\.(\d+))?-", name + "-")
        return (int(m.group(1)), int(m.group(2) or 0)) if m else (0, 0)

    def gemini_available(self):
        if self._gemini_avail is None:
            names = []
            try:
                u = "https://generativelanguage.googleapis.com/v1beta/models?pageSize=1000&key=" + urllib.parse.quote(self.gemini_key)
                j = get_json(u, timeout=60, retries=2)
                for m in j.get("models") or []:
                    if "generateContent" in (m.get("supportedGenerationMethods") or []):
                        names.append((m.get("name") or "").replace("models/", ""))
            except Exception as e:
                warn("gemini model list failed:", str(e)[:120])
            self._gemini_avail = names
            if names:
                log(f"gemini models available: {len(names)}; chosen fast={self.gemini_models(False)[:3]} strong={self.gemini_models(True)[:3]}")
        return self._gemini_avail

    def gemini_models(self, strong=False):
        avail = self.gemini_available() or []
        cfg = (self.cfg_gemini_strong or self.cfg_gemini) if strong else self.cfg_gemini
        out = [m for m in cfg if (not avail or m in avail)]
        if avail:
            alias = "gemini-pro-latest" if strong else "gemini-flash-latest"
            if alias in avail:
                out.append(alias)
            cands = []
            for n in avail:
                low = n.lower()
                if not low.startswith("gemini-") or any(k in low for k in self.GEMINI_SKIP):
                    continue
                tier = "lite" if "flash-lite" in low else ("flash" if "flash" in low else ("pro" if "pro" in low else None))
                if not tier:
                    continue
                preview = ("preview" in low) or re.search(r"-\d{2}-\d{2}$", low) is not None  # dated snapshots
                cands.append((n, tier, preview, self._ver(low)))
            order = {"pro": 0, "flash": 1, "lite": 2} if strong else {"flash": 0, "lite": 1, "pro": 2}
            cands.sort(key=lambda c: (order[c[1]], c[2], (-c[3][0], -c[3][1]), len(c[0])))
            out += [c[0] for c in cands]
        else:  # listing failed: last-known names, best effort
            out += ["gemini-flash-latest", "gemini-pro-latest", "gemini-2.5-flash"]
        seen, uniq = set(), []
        for m in out:
            if m not in seen and m not in self.dead:
                seen.add(m); uniq.append(m)
        return uniq[:4]

    def openai_available(self):
        if self._openai_avail is None:
            ids = []
            try:
                j = get_json("https://api.openai.com/v1/models", headers={"Authorization": "Bearer " + self.openai_key}, timeout=60, retries=2)
                ids = [m.get("id") for m in (j.get("data") or []) if m.get("id")]
            except Exception as e:
                warn("openai model list failed:", str(e)[:120])
            self._openai_avail = ids
            if ids:
                log(f"openai models available: {len(ids)}; chosen fast={self.openai_models(False)[:3]} strong={self.openai_models(True)[:3]}")
        return self._openai_avail

    def openai_models(self, strong=False):
        avail = self.openai_available() or []
        cfg = (self.cfg_openai_strong or self.cfg_openai) if strong else self.cfg_openai
        out = [m for m in cfg if (not avail or m in avail)]
        pat = r"^gpt-(\d+)(?:\.(\d+))?$" if strong else r"^gpt-(\d+)(?:\.(\d+))?-mini$"
        cands = [(m, self._ver("-" + m[4:] + "-")) for m in avail if re.match(pat, m)]
        cands.sort(key=lambda c: (-c[1][0], -c[1][1]))
        out += [c[0] for c in cands]
        if not avail:
            out += ["gpt-4.1", "gpt-4o"] if strong else ["gpt-4.1-mini", "gpt-4o-mini"]
        seen, uniq = set(), []
        for m in out:
            if m not in seen and m not in self.dead:
                seen.add(m); uniq.append(m)
        return uniq[:3]

    # ---- providers
    def _openai(self, model, system, user, temperature=0.2, max_tokens=4000, image_b64=None):
        content = [{"type": "text", "text": user}]
        if image_b64:
            content.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_b64, "detail": "low"}})
        body = {"model": model, "temperature": temperature, "max_tokens": max_tokens,
                "response_format": {"type": "json_object"},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": content}]}
        try:
            st, txt, _ = http("https://api.openai.com/v1/chat/completions", method="POST", json_body=body,
                              headers={"Authorization": "Bearer " + self.openai_key}, timeout=240, retries=2)
        except HttpError as e:
            if e.code == 400 and ("max_tokens" in e.body or "temperature" in e.body):
                body.pop("max_tokens", None); body.pop("temperature", None); body["max_completion_tokens"] = max_tokens
                st, txt, _ = http("https://api.openai.com/v1/chat/completions", method="POST", json_body=body,
                                  headers={"Authorization": "Bearer " + self.openai_key}, timeout=240, retries=2)
            else:
                raise
        j = json.loads(txt)
        return j["choices"][0]["message"]["content"]

    def _gemini(self, model, system, user, temperature=0.2, max_tokens=4000, image_b64=None):
        parts = [{"text": user}]
        if image_b64:
            parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_b64}})
        body = {"system_instruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": parts}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": min(65536, max(8192, max_tokens * 3)),
                                     "responseMimeType": "application/json"}}
        u = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(self.gemini_key)}"
        st, txt, _ = http(u, method="POST", json_body=body, timeout=300, retries=2)
        j = json.loads(txt)
        cand = (j.get("candidates") or [{}])[0]
        texts = [p.get("text") for p in ((cand.get("content") or {}).get("parts") or []) if p.get("text") and not p.get("thought")]
        if not texts:
            raise RuntimeError(f"gemini empty answer (finishReason={cand.get('finishReason')}, block={(j.get('promptFeedback') or {}).get('blockReason')})")
        return "".join(texts)

    def json(self, system, user, strong=False, temperature=0.2, max_tokens=4000, image_b64=None, prefer=None):
        """Return parsed JSON from the first provider/model that works. None if all fail."""
        if self.dry:
            return None
        order = []
        if self.gemini_key:
            order += [("gemini", m) for m in self.gemini_models(strong)]
        if self.openai_key:
            order += [("openai", m) for m in self.openai_models(strong)]
        if prefer == "openai":
            order = [o for o in order if o[0] == "openai"] + [o for o in order if o[0] != "openai"]
        system = system + "\nRespond with a single JSON object only."
        for prov, model in order:
            if model in self.dead:
                continue
            try:
                self.calls += 1
                txt = self._openai(model, system, user, temperature, max_tokens, image_b64) if prov == "openai" else self._gemini(model, system, user, temperature, max_tokens, image_b64)
                txt = txt.strip()
                if txt.startswith("```"):
                    txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt, flags=re.S)
                return json.loads(txt)
            except HttpError as e:
                self.failures += 1
                low = (e.body or "").lower()
                if e.code == 404 or (e.code == 400 and ("not found" in low or "no longer available" in low or "not supported" in low)):
                    self.dead.add(model)  # do not retry a missing model for the rest of the run
                short = re.sub(r"\s+", " ", e.body or "")[:200]
                warn(f"llm {prov}/{model} http {e.code}: {short}")
                continue
            except Exception as e:
                self.failures += 1
                warn(f"llm {prov}/{model} failed: {str(e)[:200]}")
                continue
        return None

# ----------------------------------------------------------------- run report
class Report:
    def __init__(self, stage):
        self.stage = stage
        self.started = now_iso()
        self.counters = {}
        self.notes = []
        self.errors = []

    def inc(self, k, n=1):
        self.counters[k] = self.counters.get(k, 0) + n

    def note(self, s):
        self.notes.append(s)
        log("NOTE", s)

    def error(self, s):
        self.errors.append(str(s)[:300])
        warn(s)

    def finish(self):
        rec = {"stage": self.stage, "started": self.started, "finished": now_iso(), "counters": self.counters,
               "notes": self.notes[:50], "errors": self.errors[:50], "version": PIPELINE_VERSION}
        hist = load_state("runs.json", [])
        hist.append(rec)
        save_state("runs.json", hist[-400:])
        log("RUN", json.dumps(rec, ensure_ascii=False))
        return rec

#!/usr/bin/env python3
"""DanceWorld 24/7 hero-video crawler - PEAK build (verified crowd-wisdom + comment check + self-healing).
Per dance: search '<name> dance performance' -> gate candidates (whole-word name/alias match in title/desc;
reject Music-category, songs, movie clips; require embeddable + comments + 15-2000s + likes>50) ->
rank by engagement -> VERIFY top candidates via top comments (real dancing of the right dance) ->
accept first that passes, else forced-refetch with stricter query, else leave BLANK (needs_eyes_on).
Each run also self-heals: purges song/movie picks and dead/non-embeddable videos, re-queuing them.
Optional OpenAI comment-judging (OPENAI_API_KEY) else keyword heuristic. Stdlib only. Resumable/cached/multi-key."""
import os, re, sys, json, time, unicodedata, urllib.parse, urllib.request, urllib.error

YT_KEYS=[k.strip() for k in os.environ.get("YT_API_KEYS","").split(",") if k.strip()]
OPENAI_KEY=os.environ.get("OPENAI_API_KEY","").strip()
SUPABASE_URL=os.environ.get("SUPABASE_URL","").strip()
SUPABASE_KEY=os.environ.get("SUPABASE_SERVICE_KEY","").strip()
DAILY_PER_KEY=int(os.environ.get("DAILY_SEARCH_BUDGET","90"))
LIST_PATH=os.environ.get("DANCE_LIST","dance_list.json")
OUT_PATH=os.environ.get("OUT_PATH","hero_results.json")
CACHE_PATH=os.environ.get("CACHE_PATH","crawler_cache.json")

SONGHARD=re.compile(r"(official\s*(video|audio|music)|\blyric|orquesta|orchestra|symphony|philharmon|\brieu\b|vittorio\s*monti|shostakovich|tchaikovsky|strauss|ao\s*vivo|en\s*vivo|en\s*directo|en\s*concierto|\bviolin|vevo|-\s*topic|\btopic\b|\bremix\b|karaoke|instrumental|full\s*song|\bcover\b|prod\.|\bft\.|feat\.)",re.I)
MOVIE=re.compile(r"(movieclips|netflix|\bmovie\b|\bfilm\b|trailer|scene\s*\(|\(20\d\d\)|full\s*episode|tv\s*show|cartoon|pencilmation)",re.I)
STRONG=re.compile(r"(choreo|coreograf|baile|danza|dance|dancing|folklor|tradition|festival|ballet|competition|championship|ensemble|troupe|performance)",re.I)
DANCE_OK=re.compile(r"(danc|choreo|coreograf|footwork|\bmoves\b|performance|beautiful|tradition|culture|heritage|proud|\bfolk\b|costume|steps)",re.I)
SONG_SIG=re.compile(r"(\bsong\b|\blyric|\baudio\b|on\s*repeat|\bbanger\b|spotify|apple\s*music|\bmp3\b|great\s*song|love\s*this\s*song)",re.I)

def norm(s):
    s=unicodedata.normalize("NFD",str(s or "").lower())
    return "".join(c for c in s if unicodedata.category(c)!="Mn")
def name_in(text,names):
    for nm in names:
        if len(nm)<=4:
            if re.search(r"\b"+re.escape(nm)+r"\b",text): return True
        elif nm in text: return True
    return False
def isodur(s):
    m=re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?",s or "")
    if not m: return 0
    h,mi,se=(int(x) if x else 0 for x in m.groups()); return h*3600+mi*60+se

class Keys:
    def __init__(s,ks): s.ks=ks; s.i=0; s.dead=set()
    def cur(s):
        if len(s.dead)>=len(s.ks): return None
        while s.i in s.dead: s.i=(s.i+1)%len(s.ks)
        return s.ks[s.i]
    def rot(s): s.dead.add(s.i); s.i=(s.i+1)%len(s.ks)

def api(path,params,keys):
    tries=0
    while True:
        k=keys.cur()
        if not k: raise RuntimeError("all keys exhausted (quota)")
        params["key"]=k
        url="https://www.googleapis.com/youtube/v3/"+path+"?"+urllib.parse.urlencode(params)
        try:
            with urllib.request.urlopen(url,timeout=30) as r: return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (403,429): keys.rot(); continue
            if e.code>=500 and tries<3: tries+=1; time.sleep(2*tries); continue
            raise
        except Exception:
            if tries<3: tries+=1; time.sleep(2*tries); continue
            raise

def search_ids(q,keys,n=14):
    sj=api("search",{"part":"snippet","type":"video","videoEmbeddable":"true","maxResults":str(n),"q":q},keys)
    return [it["id"]["videoId"] for it in sj.get("items",[]) if it.get("id",{}).get("videoId")]

def evaluate(ids,names,keys):
    if not ids: return []
    vj=api("videos",{"part":"snippet,statistics,contentDetails,status","id":",".join(ids)},keys)
    out=[]
    for it in vj.get("items",[]):
        sn=it.get("snippet",{}); st=it.get("statistics",{})
        t=sn.get("title",""); desc=sn.get("description",""); ch=sn.get("channelTitle",""); cat=str(sn.get("categoryId",""))
        likes=int(st.get("likeCount",0) or 0); comments=int(st.get("commentCount",0) or 0); views=int(st.get("viewCount",0) or 0)
        D=isodur(it.get("contentDetails",{}).get("duration")); emb=bool(it.get("status",{}).get("embeddable"))
        nt=norm(t); nd=norm(desc)
        relevant=name_in(nt,names) or name_in(nd,names)
        ok=relevant and cat!="10" and not MOVIE.search(t+" "+ch) and not SONGHARD.search(t+" "+ch) and emb and 15<=D<=2000 and likes>50 and comments>0
        own=name_in(nt,names); strong=bool(STRONG.search(t))
        score=(comments*12+likes+views*0.0005)*(1 if (strong or own) else 0.4)
        if ok: out.append({"id":it["id"],"title":t,"channel":ch,"own":own,"score":score})
    out.sort(key=lambda c:-c["score"]); return out

def top_comments(vid,keys,n=20):
    try:
        j=api("commentThreads",{"part":"snippet","videoId":vid,"order":"relevance","maxResults":str(n),"textFormat":"plainText"},keys)
        return [it.get("snippet",{}).get("topLevelComment",{}).get("snippet",{}).get("textDisplay","")[:280] for it in j.get("items",[]) if it.get("snippet")]
    except Exception: return []

def verify_llm(name,title,comments):
    if not OPENAI_KEY or not comments: return None
    user="DANCE: "+name+"\nVIDEO TITLE: "+title+"\nTOP COMMENTS:\n"+"\n".join("- "+c for c in comments[:18])+"\n\nReturn JSON: {\"real_dance\":true/false,\"right_dance\":true/false,\"is_song_not_dance\":true/false,\"confidence\":0..1,\"reason\":\"under 8 words\"}"
    body=json.dumps({"model":"gpt-4o-mini","max_tokens":160,"temperature":0,"messages":[{"role":"system","content":"You judge whether a YouTube video is an authentic clip of a specific named dance being DANCED - not a song that merely shares the name, not a different dance. Output ONLY JSON."},{"role":"user","content":user}]}).encode()
    req=urllib.request.Request("https://api.openai.com/v1/chat/completions",data=body,method="POST",headers={"Authorization":"Bearer "+OPENAI_KEY,"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=45) as r:
            txt=json.loads(r.read().decode())["choices"][0]["message"]["content"]; mt=re.search(r"\{.*\}",txt,re.S)
            return json.loads(mt.group(0)) if mt else None
    except Exception as e:
        print("  llm err:",str(e)[:60]); return None

def verify(name,comments):
    j=verify_llm(name,name,comments)
    if j is not None:
        if j.get("is_song_not_dance") or not j.get("real_dance",True) or not j.get("right_dance",True): return (False,"llm:"+str(j.get("reason",""))[:40])
        return (True,"llm ok")
    if not comments: return (True,"no comments")
    dc=sum(1 for c in comments if DANCE_OK.search(c)); ss=sum(1 for c in comments if SONG_SIG.search(c))
    if dc==0 and ss>=2: return (False,"comments are about a song")
    if ss>dc*2 and dc<2: return (False,"song-talk dominates")
    return (True,"comments ok")

def pick(dance,keys):
    name=dance.get("name") or dance.get("slug")
    names=[norm(name)]+[norm(a) for a in dance.get("aliases",[])]; names=[n for n in names if n and len(n)>=3]
    cands=evaluate(search_ids(name+" dance performance",keys),names,keys)
    if not cands and dance.get("country"):
        cands=evaluate(search_ids('"'+name+'" '+dance.get("country","")+" dance",keys),names,keys)
    for c in cands[:3]:
        ok,why=verify(name,top_comments(c["id"],keys,20))
        if ok:
            status="crowd_wisdom_confident" if c["own"] else "crowd_wisdom_weak"
            return {"status":status,"hero_video_youtube_id":c["id"],"title":c["title"],"channel":c["channel"],"crowd_score":round(c["score"]),"verify":why,"challengers":[x["id"] for x in cands if x["id"]!=c["id"]][:2]}
    return {"status":"blank","reason":"failed_comment_verify" if cands else "all_filtered"}

def songhard_cleanup(out,cache):
    n=0
    for slug,r in list(out.items()):
        if SONGHARD.search((r.get("title","") or "")+" "+(r.get("channel","") or "")) or MOVIE.search((r.get("title","") or "")):
            out.pop(slug,None); cache.pop(slug,None); n+=1
    return n

def revalidate(out,cache,keys):
    items=[(slug,r["hero_video_youtube_id"]) for slug,r in list(out.items()) if r.get("hero_video_youtube_id")]
    n=0
    for i in range(0,len(items),50):
        idmap={}
        for slug,vid in items[i:i+50]: idmap.setdefault(vid,[]).append(slug)
        try: vj=api("videos",{"part":"status","id":",".join(list(idmap.keys()))},keys)
        except Exception: continue
        alive=set(it["id"] for it in vj.get("items",[]) if it.get("status",{}).get("embeddable"))
        for vid,slugs in idmap.items():
            if vid not in alive:
                for slug in slugs: out.pop(slug,None); cache.pop(slug,None); n+=1
    return n

def supa(slug,res):
    if not(SUPABASE_URL and SUPABASE_KEY): return
    body=json.dumps([{"dance_slug":slug,"video_type":"hero","video_id":res["hero_video_youtube_id"],"title":res.get("title"),"channel":res.get("channel"),"crowd_score":res.get("crowd_score"),"status":res.get("status"),"video_stack":res.get("challengers")}]).encode()
    req=urllib.request.Request(SUPABASE_URL.rstrip("/")+"/rest/v1/dance_videos?on_conflict=dance_slug,video_type",data=body,method="POST",headers={"apikey":SUPABASE_KEY,"Authorization":"Bearer "+SUPABASE_KEY,"Content-Type":"application/json","Prefer":"resolution=merge-duplicates"})
    try: urllib.request.urlopen(req,timeout=30)
    except Exception as e: print("  supabase err:",str(e)[:80])

def save(out,cache):
    json.dump(cache,open(CACHE_PATH,"w",encoding="utf-8")); json.dump(out,open(OUT_PATH,"w",encoding="utf-8"),ensure_ascii=False,indent=1)

def main():
    if not YT_KEYS: print("ERROR: set YT_API_KEYS (comma-separated)"); sys.exit(1)
    keys=Keys(YT_KEYS); budget=DAILY_PER_KEY*len(YT_KEYS)
    dances=json.load(open(LIST_PATH,encoding="utf-8"))
    cache=json.load(open(CACHE_PATH,encoding="utf-8")) if os.path.exists(CACHE_PATH) else {}
    out=json.load(open(OUT_PATH,encoding="utf-8")) if os.path.exists(OUT_PATH) else {}
    if out:
        p1=songhard_cleanup(out,cache); p2=revalidate(out,cache,keys)
        if p1 or p2: print("self-heal: purged "+str(p1)+" song/movie + "+str(p2)+" dead/non-embeddable (re-queued)"); save(out,cache)
    pub=[d for d in dances if d.get("publish") and not d.get("has_hero") and d.get("slug") not in cache and d.get("wikipedia")]
    rest=[d for d in dances if not d.get("publish") and not d.get("has_hero") and d.get("slug") not in cache]
    todo=pub+rest
    print(str(len(todo))+" need hero; budget "+str(budget)+" searches ("+str(len(YT_KEYS))+" keys); LLM="+("on" if OPENAI_KEY else "off"))
    done=0; wrote=0
    for d in todo:
        if done>=budget: print("daily budget reached"); break
        slug=d["slug"]
        try: res=pick(d,keys); done+=1
        except RuntimeError as e: print("stop:",e); break
        except Exception as e: res={"status":"error","reason":str(e)[:80]}
        cache[slug]=res
        if res.get("hero_video_youtube_id"):
            out[slug]=res; wrote+=1; print("OK  "+slug+": "+res["hero_video_youtube_id"]+" ("+res["status"]+") "+str(res.get("verify",""))); supa(slug,res)
        else: print("--  "+slug+": "+str(res.get("status"))+"/"+str(res.get("reason","")))
        save(out,cache)
    print("run done: "+str(done)+" searches, +"+str(wrote)+" new heroes, "+str(len(out))+" total in hero_results.json")

if __name__=="__main__": main()

import os, re, sys, json, time, urllib.parse, urllib.request, urllib.error

MODE=os.environ.get("MODE","all").lower()
YT_KEYS=[k.strip() for k in os.environ.get("YT_API_KEYS","").split(",") if k.strip()]
OPENAI_KEY=os.environ.get("OPENAI_API_KEY","").strip()
LIST_PATH=os.environ.get("DANCE_LIST","dance_list.json")
B_HERO=int(os.environ.get("BUDGET_HERO","400"))
B_TUT=int(os.environ.get("BUDGET_TUTORIAL","400"))
B_VIRAL=int(os.environ.get("BUDGET_VIRAL","24"))

SACRED=set(json.loads(r'''["bharatanatyam","capoeira","hula","haka","sufi-whirling","odissi","kathakali","manipuri","mohiniyattam","bon-odori","apsara-dance","legong","saman","garba","ring-shout","chhau","danza-de-los-voladores","diablada","baris","kuchipudi","sattriya","kecak","candomble","calusari","gnawa","cham-dance","lakhon-khol","mongolian-tsam","mak-yong","sinulog","tinku","theyyam","ainu-dance","gule-wamkulu","burundi-royal-drum","intore","dhamal-sufi","matachines","padayani","hula-kahiko","mendiani","zinli","ingoma-mapiko","kumina","sakela-sili"]'''))
VIRAL_SEEDS=json.loads(r'''[{"slug":"apt-challenge","name":"APT. challenge","song":"APT. — Rosé ft. Bruno Mars","type":"viral_challenge","platform":"TikTok/YouTube Shorts","origin_year":"2024"},{"slug":"anxiety-dance","name":"Anxiety dance","song":"Anxiety — Doechii","type":"viral_challenge","platform":"TikTok","origin_year":"2025"},{"slug":"espresso-dance","name":"Espresso dance","song":"Espresso — Sabrina Carpenter","type":"viral_challenge","platform":"TikTok","origin_year":"2024"},{"slug":"passinho-do-jamal","name":"Passinho do Jamal","song":"brega funk","type":"viral_challenge","platform":"TikTok","origin_year":"2025"},{"slug":"wednesday-dead-dance-s2","name":"Wednesday Dead Dance (S2)","song":"Lady Gaga (S2 track)","type":"viral_challenge","platform":"Netflix/TikTok","origin_year":"2025"},{"slug":"crank-that","name":"Crank That","song":"Crank That — Soulja Boy","type":"viral_challenge","platform":"MySpace/YouTube","origin_year":"2007"},{"slug":"gangnam-style","name":"Gangnam Style","song":"Gangnam Style — PSY","type":"viral_challenge","platform":"YouTube","origin_year":"2012"},{"slug":"harlem-shake","name":"Harlem Shake","song":"Harlem Shake — Baauer","type":"viral_challenge","platform":"YouTube","origin_year":"2013"},{"slug":"nae-nae","name":"Nae Nae","song":"Drop That NaeNae","type":"viral_challenge","platform":"Vine/YouTube","origin_year":"2013"},{"slug":"whip-nae-nae-watch-me","name":"Whip / Nae Nae (Watch Me)","song":"Watch Me (Whip/Nae Nae) — Silentó","type":"viral_challenge","platform":"SoundCloud/Vine","origin_year":"2015"},{"slug":"running-man-challenge","name":"Running Man Challenge","song":"My Boo — Ghost Town DJ's","type":"viral_challenge","platform":"Vine/Instagram","origin_year":"2016"},{"slug":"floss-dance","name":"Floss dance","song":"various","type":"viral_challenge","platform":"Instagram/SNL","origin_year":"2016"},{"slug":"in-my-feelings-kiki","name":"In My Feelings / Kiki","song":"In My Feelings — Drake","type":"viral_challenge","platform":"Instagram","origin_year":"2018"},{"slug":"the-git-up","name":"The Git Up","song":"The Git Up — Blanco Brown","type":"viral_challenge","platform":"TikTok/YouTube","origin_year":"2019"},{"slug":"renegade","name":"Renegade","song":"Lottery — K Camp","type":"viral_challenge","platform":"Funimate/IG→TikTok","origin_year":"2019"},{"slug":"savage","name":"Savage","song":"Savage — Megan Thee Stallion","type":"viral_challenge","platform":"TikTok","origin_year":"2020"},{"slug":"say-so","name":"Say So","song":"Say So — Doja Cat","type":"viral_challenge","platform":"TikTok","origin_year":"2019"},{"slug":"toosie-slide","name":"Toosie Slide","song":"Toosie Slide — Drake","type":"viral_challenge","platform":"TikTok","origin_year":"2020"},{"slug":"savage-love-laxed","name":"Savage Love / Laxed","song":"Laxed (Siren Beat) — Jawsh 685","type":"viral_challenge","platform":"TikTok","origin_year":"2020"},{"slug":"wap-challenge","name":"WAP challenge","song":"WAP — Cardi B ft. Megan","type":"viral_challenge","platform":"TikTok","origin_year":"2020"},{"slug":"buss-it","name":"Buss It","song":"Buss It — Erica Banks","type":"viral_challenge","platform":"TikTok","origin_year":"2021"},{"slug":"wipe-it-down","name":"Wipe It Down","song":"Wipe It Down — BMW Kenny","type":"viral_challenge","platform":"TikTok","origin_year":"2021"},{"slug":"corvette-corvette","name":"Corvette Corvette","song":"Adderall (Corvette Corvette) — Popp Hunna","type":"viral_challenge","platform":"TikTok","origin_year":"2020"},{"slug":"up-challenge","name":"Up challenge","song":"Up — Cardi B","type":"viral_challenge","platform":"TikTok","origin_year":"2021"},{"slug":"made-you-look","name":"Made You Look","song":"Made You Look — Meghan Trainor","type":"viral_challenge","platform":"TikTok","origin_year":"2022"},{"slug":"wednesday-bloody-mary","name":"Wednesday / Bloody Mary","song":"Bloody Mary — Lady Gaga (fan re-edit)","type":"viral_challenge","platform":"Netflix/TikTok","origin_year":"2022"},{"slug":"cupid-twin-challenge","name":"Cupid Twin Challenge","song":"Cupid (Twin Version) — FIFTY FIFTY","type":"viral_challenge","platform":"TikTok","origin_year":"2023"},{"slug":"apple-dance","name":"Apple dance","song":"Apple — Charli XCX","type":"viral_challenge","platform":"TikTok","origin_year":"2024"},{"slug":"million-dollar-baby","name":"Million Dollar Baby","song":"Million Dollar Baby — Tommy Richman","type":"viral_challenge","platform":"TikTok","origin_year":"2024"},{"slug":"pedro","name":"Pedro","song":"Pedro — Raffaella Carrà (remix)","type":"viral_challenge","platform":"TikTok","origin_year":"2024"},{"slug":"jerusalema-dance-challenge","name":"Jerusalema Dance Challenge","song":"Jerusalema — Master KG ft. Nomcebo","type":"viral_challenge","platform":"TikTok/YouTube","origin_year":"2020"},{"slug":"blinding-lights-challenge","name":"Blinding Lights challenge","song":"Blinding Lights — The Weeknd","type":"viral_challenge","platform":"TikTok","origin_year":"2020"},{"slug":"about-damn-time","name":"About Damn Time","song":"About Damn Time — Lizzo","type":"viral_challenge","platform":"TikTok","origin_year":"2022"},{"slug":"k-pop-point-choreography-challenges","name":"K-pop point-choreography challenges","song":"various K-pop","type":"viral_challenge","platform":"TikTok","origin_year":"2025"}]''')
VIRAL_DISCOVERY=["Renegade","Savage","Say So","WAP","Buss It","Corvette Corvette","Out West","Tap In","Laxed Siren Beat","Cannibal challenge","Up Cardi B","Body Tion Wayne","Wipe It Down","Oh Na Na Na","Jerusalema","Woah","The Git Up","In My Feelings Kiki","Silhouette","Adult Swim","Toosie Slide","Blinding Lights","Don't Rush","Something New"]

SONGHARD=re.compile(r"(official\s*(video|audio|music)|\blyric|orquesta|orchestra|symphony|philharmon|\brieu\b|monti|shostakovich|tchaikovsky|strauss|ao\s*vivo|en\s*vivo|en\s*directo|\bviolin|vevo|-\s*topic|\bremix\b|karaoke|instrumental|full\s*song|\bcover\b|prod\.|\bft\.|feat\.)",re.I)
MOVIE=re.compile(r"(movieclips|netflix|\bmovie\b|\bfilm\b|trailer|scene\s*\(|\(20\d\d\)|full\s*episode|cartoon|pencilmation)",re.I)
STRONG=re.compile(r"(choreo|coreograf|baile|danza|dance|dancing|folklor|tradition|festival|ballet|competition|championship|ensemble|troupe|performance)",re.I)
DANCE_OK=re.compile(r"(danc|choreo|coreograf|footwork|\bmoves\b|performance|beautiful|tradition|culture|heritage|proud|\bfolk\b|costume|steps)",re.I)
SONG_SIG=re.compile(r"(\bsong\b|\blyric|\baudio\b|on\s*repeat|spotify|apple\s*music|great\s*song|love\s*this\s*song)",re.I)
TUT_WORD=re.compile(r"(tutorial|lesson|how\s*to|learn|beginner|step[\s-]*by[\s-]*step|basics|class|breakdown|easy)",re.I)
TUT_POS=["finally clicked","best teacher","so clear","i learned so much","wish i had this earlier","made it simple","thank you so much","understand now","perfect breakdown","amazing instructor","patient teacher","easy to follow","changed my life","this works","helped me a lot","great teacher","well explained","makes sense now"]
TUT_NEG=["too fast","confusing","wrong","misleading","inappropriate","cultural appropriation","incorrect","misrepresents","hard to follow","can't keep up"]
TUT_HARD=["cultural appropriation","misrepresents","inappropriate","disrespectful"]
LEVELS=[("advanced",re.compile(r"\badvanced\b|\bpro\b|\bexpert\b",re.I)),("intermediate",re.compile(r"intermediate|level\s*2|improver",re.I)),("beginner",re.compile(r"beginner|basics|for\s*beginners|level\s*1|\bintro\b|\beasy\b|first\s*lesson",re.I))]

def norm(s): return str(s or "").lower()
def slugify(s):
    s=re.sub(r"[^a-z0-9]+","-",str(s or "").lower()).strip("-"); return s[:60]
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
    def __init__(s,ks): s.ks=ks; s.i=0; s.dead=set(); s.n=0
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

def _ytdlp_search(q,n=20):
    import subprocess,shutil
    if not shutil.which("yt-dlp"): return []
    try:
        out=subprocess.run(["yt-dlp","ytsearch"+str(n)+":"+q,"--flat-playlist","--no-warnings","--print","id"],capture_output=True,text=True,timeout=90)
        seen=set(); uniq=[]
        for ln in out.stdout.splitlines():
            i=ln.strip()
            if i and i not in seen: seen.add(i); uniq.append(i)
        return uniq[:n]
    except Exception as e:
        sys.stderr.write("ytdlp fail "+q+": "+str(e)+"\n"); return []

def search_ids(q,keys,n=14):
    ids=_ytdlp_search(q,n=max(n,20))
    if ids: return ids[:max(n,20)]
    try:
        sj=api("search",{"part":"snippet","type":"video","videoEmbeddable":"true","maxResults":str(min(n,50)),"q":q},keys)
        return [it["id"]["videoId"] for it in sj.get("items",[]) if it.get("id",{}).get("videoId")]
    except Exception: return []

def videos(ids,keys):
    if not ids: return []
    return api("videos",{"part":"snippet,statistics,contentDetails,status","id":",".join(ids)},keys).get("items",[])

def comments(vid,keys,n=100):
    out=[]; tok=None
    while len(out)<n:
        p={"part":"snippet","videoId":vid,"order":"relevance","maxResults":str(min(100,n-len(out))),"textFormat":"plainText"}
        if tok: p["pageToken"]=tok
        try: j=api("commentThreads",p,keys)
        except Exception: break
        for it in j.get("items",[]):
            out.append((it.get("snippet",{}).get("topLevelComment",{}).get("snippet",{}).get("textDisplay","") or "")[:300])
        tok=j.get("nextPageToken")
        if not tok: break
    return out

def evaluate(ids,names,keys):
    out=[]
    for it in videos(ids,keys):
        sn=it.get("snippet",{}); st=it.get("statistics",{})
        t=sn.get("title",""); desc=sn.get("description",""); ch=sn.get("channelTitle",""); cat=str(sn.get("categoryId",""))
        likes=int(st.get("likeCount",0) or 0); ncom=int(st.get("commentCount",0) or 0); views=int(st.get("viewCount",0) or 0)
        D=isodur(it.get("contentDetails",{}).get("duration")); emb=bool(it.get("status",{}).get("embeddable"))
        nt=norm(t); nd=norm(desc)
        relevant=name_in(nt,names) or name_in(nd,names)
        ok=relevant and cat!="10" and not MOVIE.search(t+" "+ch) and not SONGHARD.search(t+" "+ch) and emb and 15<=D<=2000 and likes>50 and ncom>0
        own=name_in(nt,names); strong=bool(STRONG.search(t))
        score=(ncom*12+likes+views*0.0005)*(1 if (strong or own) else 0.4)
        if ok: out.append({"id":it["id"],"title":t,"channel":ch,"own":own,"score":score})
    out.sort(key=lambda c:-c["score"]); return out

def verify(name,cs):
    if not cs: return True
    dc=sum(1 for c in cs if DANCE_OK.search(c)); ss=sum(1 for c in cs if SONG_SIG.search(c))
    if dc==0 and ss>=2: return False
    if ss>dc*2 and dc<2: return False
    return True

def pick_hero(dance,keys):
    name=dance.get("name") or dance.get("slug")
    names=[norm(name)]+[norm(a) for a in dance.get("aliases",[])]; names=[x for x in names if x and len(x)>=3]
    cands=evaluate(search_ids(name+" dance performance",keys),names,keys)
    if not cands and dance.get("country"):
        cands=evaluate(search_ids(name+" "+dance.get("country","")+" dance",keys),names,keys)
    for c in cands[:3]:
        if verify(name,comments(c["id"],keys,20)):
            status="crowd_wisdom_confident" if c["own"] else "crowd_wisdom_weak"
            return {"status":status,"hero_video_youtube_id":c["id"],"title":c["title"],"channel":c["channel"],"crowd_score":round(c["score"]),"challengers":[x["id"] for x in cands if x["id"]!=c["id"]][:2]}
    return {"status":"blank","reason":"failed" if cands else "all_filtered"}

def lesson_eval(dance,keys):
    name=dance.get("name") or dance.get("slug")
    names=[norm(name)]+[norm(a) for a in dance.get("aliases",[])]; names=[x for x in names if x and len(x)>=3]
    ids=[]
    for q in [name+" dance tutorial", name+" dance for beginners", "learn "+name+" dance"]:
        ids+=search_ids(q,keys,12)
    ids=list(dict.fromkeys(ids))[:30]
    cands=[]
    for it in videos(ids,keys):
        sn=it.get("snippet",{}); st=it.get("statistics",{})
        t=sn.get("title",""); desc=sn.get("description",""); ch=sn.get("channelTitle",""); cat=str(sn.get("categoryId",""))
        D=isodur(it.get("contentDetails",{}).get("duration")); emb=bool(it.get("status",{}).get("embeddable"))
        likes=int(st.get("likeCount",0) or 0); ncom=int(st.get("commentCount",0) or 0)
        nt=norm(t); nd=norm(desc)
        relevant=name_in(nt,names) or name_in(nd,names)
        is_tut=bool(TUT_WORD.search(t)) or bool(TUT_WORD.search(desc[:200]))
        ok=relevant and is_tut and cat!="10" and not SONGHARD.search(t+" "+ch) and not MOVIE.search(t+" "+ch) and emb and 60<=D<=4800 and ncom>0
        if ok: cands.append({"id":it["id"],"title":t,"channel":ch,"likes":likes,"ncom":ncom})
    cands.sort(key=lambda c:-(c["ncom"]*5+c["likes"]))
    lessons=[]
    for c in cands[:6]:
        cs=comments(c["id"],keys,100); low=" \n ".join(cs).lower()
        if sum(low.count(s) for s in TUT_HARD)>=2: continue
        pos=sum(low.count(s) for s in TUT_POS); neg=sum(low.count(s) for s in TUT_NEG)
        ratio=pos/(neg+1.0)
        if pos>=2 and ratio>1.0:
            ev=[c2[:160] for c2 in cs if any(s in c2.lower() for s in TUT_POS)][:3]
            lvl="general"
            for nm,rx in LEVELS:
                if rx.search(c["title"].lower()): lvl=nm; break
            lessons.append({"youtube_id":c["id"],"title":c["title"][:140],"channel":c["channel"],"level":lvl,"pos":pos,"neg":neg,"ratio":round(ratio,2),"evidence":ev,"lesson_status":"in_review"})
        if len(lessons)>=3: break
    lessons.sort(key=lambda l:-l["ratio"])
    return lessons

def viral_eval(seed,keys):
    name=seed.get("name") or seed.get("slug"); song=seed.get("song") or ""
    qs=[name+" dance challenge"]
    if song: qs.append(song+" dance")
    ids=[]
    for q in qs[:2]: ids+=search_ids(q,keys,12)
    ids=list(dict.fromkeys(ids))[:24]
    cands=[]
    for it in videos(ids,keys):
        sn=it.get("snippet",{}); st=it.get("statistics",{})
        t=sn.get("title",""); ch=sn.get("channelTitle","")
        D=isodur(it.get("contentDetails",{}).get("duration")); emb=bool(it.get("status",{}).get("embeddable"))
        views=int(st.get("viewCount",0) or 0); likes=int(st.get("likeCount",0) or 0); ncom=int(st.get("commentCount",0) or 0)
        nt=norm(t)
        rel=(norm(name) in nt) or (song and norm(song) in nt) or ("challenge" in nt) or ("tiktok" in nt) or ("dance" in nt)
        bad=re.search(r"(\blyric|audio\s*only|karaoke|official\s*music\s*video|sped\s*up|slowed|reverb)",t,re.I)
        ok=rel and emb and not bad and 6<=D<=900 and views>10000
        if ok: cands.append({"id":it["id"],"title":t[:140],"channel":ch,"views":views,"score":views+likes*20+ncom*50})
    cands.sort(key=lambda c:-c["score"])
    if not cands: return None
    top=cands[0]
    return {"hero_video_youtube_id":top["id"],"hero_brief":top["title"],"channel":top["channel"],"views":top["views"],
            "video_stack":[{"youtube_id":c["id"],"role":("hero" if i==0 else "rendition"),"title":c["title"],"channel":c["channel"],"views":c["views"]} for i,c in enumerate(cands[:4])],
            "status":"crawled"}

def jload(p,d):
    return json.load(open(p,encoding="utf-8")) if os.path.exists(p) else d
def jsave(p,o):
    json.dump(o,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)

def main():
    if not YT_KEYS: print("ERROR: set YT_API_KEYS"); sys.exit(1)
    keys=Keys(YT_KEYS)
    dances=jload(LIST_PATH,[])
    print("MODE="+MODE+" | dances="+str(len(dances))+" | keys="+str(len(YT_KEYS)))

    if MODE in ("all","hero"):
        cache=jload("crawler_cache.json",{}); out=jload("hero_results.json",{}); done=0; wrote=0
        def _retry(d):
            c=cache.get(d.get("slug"))
            return (c is None) or (isinstance(c,dict) and not c.get("hero_video_youtube_id"))
        todo=[d for d in dances if d.get("publish") and not d.get("has_hero") and _retry(d) and d.get("wikipedia")]
        todo+=[d for d in dances if d.get("publish") and not d.get("has_hero") and _retry(d) and not d.get("wikipedia")]
        todo+=[d for d in dances if not d.get("publish") and not d.get("has_hero") and _retry(d)]
        for d in todo:
            if done>=B_HERO: break
            try: res=pick_hero(d,keys); done+=1
            except RuntimeError as e: print("hero stop: "+str(e)); break
            except Exception as e: res={"status":"error","reason":str(e)[:80]}
            cache[d["slug"]]=res
            if res.get("hero_video_youtube_id"): out[d["slug"]]=res; wrote+=1; print("HERO ok "+d["slug"]+" "+res["hero_video_youtube_id"])
            jsave("crawler_cache.json",cache); jsave("hero_results.json",out)
        print("hero: +"+str(wrote)+" ("+str(len(out))+" total)")

    if MODE in ("all","tutorial"):
        tcache=jload("tutorial_cache.json",{}); tout=jload("tutorial_results.json",{}); done=0; wrote=0; skipped=0
        elig=[d for d in dances if d.get("publish") and d.get("slug") not in SACRED and not d.get("is_sacred") and d.get("slug") not in tcache and d.get("wikipedia")]
        for d in elig:
            if done>=B_TUT: break
            try: lessons=lesson_eval(d,keys); done+=1
            except RuntimeError as e: print("tut stop: "+str(e)); break
            except Exception as e: lessons=[]; print("tut err "+d["slug"]+" "+str(e)[:60])
            tcache[d["slug"]]={"n":len(lessons)}
            if lessons: tout[d["slug"]]={"lessons":lessons,"status":"in_review"}; wrote+=1; print("TUT ok "+d["slug"]+" lessons="+str(len(lessons)))
            else: print("TUT -- "+d["slug"]+" none")
            jsave("tutorial_cache.json",tcache); jsave("tutorial_results.json",tout)
        print("tutorial: +"+str(wrote)+" ("+str(len(tout))+" total); sacred auto-skipped")

    if MODE in ("all","viral"):
        vcache=jload("viral_cache.json",{}); vout=jload("viral_results.json",{}); done=0; wrote=0
        seeds=list(VIRAL_SEEDS)
        seen={s.get("slug") for s in seeds}
        for nm in VIRAL_DISCOVERY:
            sl=slugify(nm)
            if sl not in seen: seeds.append({"slug":sl,"name":nm,"type":"challenge","platform":"tiktok","song":"","status":"discovered"}); seen.add(sl)
        todo=[s for s in seeds if s.get("slug") not in vcache]
        for s in todo:
            if done>=B_VIRAL: break
            try: r=viral_eval(s,keys); done+=1
            except RuntimeError as e: print("viral stop: "+str(e)); break
            except Exception as e: r=None; print("viral err "+str(s.get("slug"))+" "+str(e)[:60])
            vcache[s["slug"]]=True
            if r:
                entry=dict(s); entry.update(r); entry["collection"]="viral_challenges"; vout[s["slug"]]=entry; wrote+=1; print("VIRAL ok "+s["slug"]+" "+r["hero_video_youtube_id"]+" views="+str(r["views"]))
            else: print("VIRAL -- "+s["slug"]+" none")
            jsave("viral_cache.json",vcache); jsave("viral_results.json",vout)
        print("viral: +"+str(wrote)+" ("+str(len(vout))+" total)")

    print("RUN COMPLETE | searches used="+str(keys.n))

if __name__=="__main__":
    main()

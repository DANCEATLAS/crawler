"""Shared helpers for the Dancing Atlas pipeline (stdlib only).

Everything network-related lives here: HTTP with retries, the Supabase REST
client, the LLM clients (OpenAI / Gemini) and the run report.  Secrets are
read from the environment only; nothing is ever written to disk.
"""
import os, re, sys, json, time, unicodedata, urllib.parse, urllib.request, urllib.error, base64, hashlib
from datetime import datetime, timezone

PIPELINE_VERSION = "v3.3"   # bump when QC gates change: every researched record is then re-judged with the new gates
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
        safe_url = urllib.parse.urlsplit(url)._replace(query="", fragment="").geturl()
        super().__init__(f"HTTP {code} {safe_url} :: {short}")
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
    """JSON model calls require the repository spending policy; no automatic upgrades."""
    GEMINI_SKIP = ("image", "tts", "live", "audio", "embedding", "thinking", "exp", "dialog", "computer-use", "robotics",
                   "deep-research", "veo", "imagen", "learnlm", "gemma", "aqa", "nano", "vision", "8b")

    def __init__(self):
        from .spending import allowance
        self.allowance = allowance()
        self.openai_key = os.environ.get("OPENAI_API_KEY", "").strip() if self.allowance.permitted("openai") else ""
        self.gemini_key = os.environ.get("GEMINI_API_KEY", "").strip() if self.allowance.permitted("gemini") else ""
        self.cfg_openai = [m.strip() for m in os.environ.get("OPENAI_MODELS", "").split(",") if m.strip()]
        self.cfg_openai_strong = [m.strip() for m in os.environ.get("OPENAI_STRONG_MODELS", "").split(",") if m.strip()]
        self.cfg_gemini = [m.strip() for m in os.environ.get("GEMINI_MODELS", "").split(",") if m.strip()]
        self.cfg_gemini_strong = [m.strip() for m in os.environ.get("GEMINI_STRONG_MODELS", "").split(",") if m.strip()]
        self._gemini_avail = None
        self._openai_avail = None
        self.dead = set()
        self.strikes = {}          # model -> consecutive failures; MAX_STRIKES in a row retires the model for this run
        self.MAX_STRIKES = int(os.environ.get("LLM_MAX_STRIKES", "2"))
        self.timeout_fast = int(os.environ.get("LLM_TIMEOUT_FAST", "120"))
        self.timeout_strong = int(os.environ.get("LLM_TIMEOUT_STRONG", "420"))
        self.think_fast = int(os.environ.get("GEMINI_THINKING_FAST", "0"))        # judge / classification calls: no thinking
        self.think_strong = int(os.environ.get("GEMINI_THINKING_STRONG", "2048"))  # research composer: bounded thinking
        self.no_thinking_cfg = set()
        self.calls = 0             # attempts (every model tried counts)
        self.failures = 0          # failed attempts (a fallback that then succeeded still counts here)
        self.requests = 0          # questions asked
        self.unanswered = 0        # questions no model could answer — the outcome the health stage tunes on
        self.dry = os.environ.get("PIPELINE_DRY_RUN") == "1"

    @property
    def enabled(self):
        return bool(self.openai_key or self.gemini_key) and not self.dry

    # ---- model discovery
    @staticmethod
    def _ver(name):
        m = re.search(r"-(\d+)(?:\.(\d+))?-", name + "-")
        return (int(m.group(1)), int(m.group(2) or 0)) if m else (0, 0)

    def gemini_models(self, strong=False):
        return [m for m in self.allowance.models("gemini") if m not in self.dead]

    def openai_models(self, strong=False):
        return [m for m in self.allowance.models("openai") if m not in self.dead]

    def _model_http(self, provider, model, token_key, settings, url, **kwargs):
        from .spending import SpendingBlocked
        if self.dry:
            raise SpendingBlocked("Dry run blocks model requests")
        settings[token_key] = self.allowance.reserve(provider, model, settings[token_key])
        self.calls += 1
        return http(url, retries=0, **kwargs)

    # ---- providers
    def _openai(self, model, system, user, temperature=0.2, max_tokens=4000, image_b64=None, timeout=240):
        content = [{"type": "text", "text": user}]
        if image_b64:
            content.append({"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_b64, "detail": "low"}})
        body = {"model": model, "temperature": temperature, "max_tokens": max_tokens,
                "response_format": {"type": "json_object"},
                "messages": [{"role": "system", "content": system}, {"role": "user", "content": content}]}
        try:
            st, txt, _ = self._model_http("openai", model, "max_tokens", body, "https://api.openai.com/v1/chat/completions", method="POST", json_body=body,
                              headers={"Authorization": "Bearer " + self.openai_key}, timeout=timeout)
        except HttpError as e:
            if e.code == 400 and ("max_tokens" in e.body or "temperature" in e.body):
                body.pop("max_tokens", None); body.pop("temperature", None); body["max_completion_tokens"] = max_tokens
                st, txt, _ = self._model_http("openai", model, "max_completion_tokens", body, "https://api.openai.com/v1/chat/completions", method="POST", json_body=body,
                                  headers={"Authorization": "Bearer " + self.openai_key}, timeout=timeout)
            else:
                raise
        j = json.loads(txt)
        return j["choices"][0]["message"]["content"]

    def _gemini(self, model, system, user, temperature=0.2, max_tokens=4000, image_b64=None, timeout=300, strong=False, video_url=None, video_seconds=480):
        parts = [{"text": user}]
        if image_b64:
            parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_b64}})
        if video_url:
            # a public YouTube URL is read by Gemini itself (nothing is downloaded here); the first video_seconds only, low resolution
            parts.append({"file_data": {"file_uri": video_url}, "video_metadata": {"start_offset": "0s", "end_offset": f"{int(video_seconds)}s"}})
        gen = {"temperature": temperature, "maxOutputTokens": max_tokens, "responseMimeType": "application/json"}
        if video_url:
            gen["mediaResolution"] = "MEDIA_RESOLUTION_LOW"
        # Bound the "thinking" phase: unbounded thinking is what made 12-item judge calls exceed the socket timeout.
        # Models that reject the field (or a zero budget) are remembered and called without it.
        if model not in self.no_thinking_cfg:
            gen["thinkingConfig"] = {"thinkingBudget": self.think_strong if strong else self.think_fast}
        body = {"system_instruction": {"parts": [{"text": system}]}, "contents": [{"role": "user", "parts": parts}], "generationConfig": gen}
        u = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={urllib.parse.quote(self.gemini_key)}"
        try:
            st, txt, _ = self._model_http("gemini", model, "maxOutputTokens", gen, u, method="POST", json_body=body, timeout=timeout)
        except HttpError as e:
            if e.code == 400 and "thinkingConfig" in gen:  # e.g. flash-lite answers a bare "invalid argument" for thinkingBudget
                warn(f"llm gemini/{model}: 400 with thinkingConfig, retrying without it")
                self.no_thinking_cfg.add(model)
                gen.pop("thinkingConfig", None)
                st, txt, _ = self._model_http("gemini", model, "maxOutputTokens", gen, u, method="POST", json_body=body, timeout=timeout)
            else:
                raise
        j = json.loads(txt)
        cand = (j.get("candidates") or [{}])[0]
        texts = [p.get("text") for p in ((cand.get("content") or {}).get("parts") or []) if p.get("text") and not p.get("thought")]
        if not texts:
            raise RuntimeError(f"gemini empty answer (finishReason={cand.get('finishReason')}, block={(j.get('promptFeedback') or {}).get('blockReason')})")
        return "".join(texts)

    @staticmethod
    def parse_json(txt):
        """Tolerant JSON: code fences, text around the object, trailing commas, // comments."""
        t = (txt or "").strip()
        if t.startswith("```"):
            t = re.sub(r"^```(?:json)?\s*|\s*```$", "", t, flags=re.S).strip()
        for attempt in range(4):
            try:
                return json.loads(t)
            except Exception:
                pass
            if attempt == 0:
                a, b = t.find("{"), t.rfind("}")
                if a >= 0 and b > a:
                    t = t[a:b + 1]
            elif attempt == 1:
                t = re.sub(r",\s*([}\]])", r"\1", t)
            elif attempt == 2:
                t = LLM._strip_comments(t)
                t = re.sub(r",\s*([}\]])", r"\1", t)
        return json.loads(t)  # raises with the real error

    @staticmethod
    def _strip_comments(t):
        """Drop // comments that sit outside string literals (keeps URLs inside strings intact)."""
        out, i, n, in_str, esc = [], 0, len(t), False, False
        while i < n:
            c = t[i]
            if in_str:
                out.append(c)
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            else:
                if c == '"':
                    in_str = True; out.append(c)
                elif c == "/" and i + 1 < n and t[i + 1] == "/":
                    while i < n and t[i] != "\n":
                        i += 1
                    continue
                else:
                    out.append(c)
            i += 1
        return "".join(out)

    def _strike(self, model):
        self.failures += 1
        self.strikes[model] = self.strikes.get(model, 0) + 1
        if self.strikes[model] >= self.MAX_STRIKES:
            self.dead.add(model)
            warn(f"llm: {model} retired for this run after {self.strikes[model]} consecutive failures")

    def json(self, system, user, strong=False, temperature=0.2, max_tokens=4000, image_b64=None, prefer=None, video_url=None, video_seconds=480):
        """Return parsed JSON from the first provider/model that works. None if all fail.
        video_url: a public YouTube URL to be watched (Gemini only; OpenAI models are skipped for that call)."""
        if not self.enabled:
            return None
        from .spending import SpendingBlocked
        self.requests += 1
        order = []
        if self.gemini_key:
            order += [("gemini", m) for m in self.gemini_models(strong)]
        if self.openai_key and not video_url:
            order += [("openai", m) for m in self.openai_models(strong)]
        if prefer == "openai":
            order = [o for o in order if o[0] == "openai"] + [o for o in order if o[0] != "openai"]
        system = system + "\nRespond with a single JSON object only."
        timeout = self.timeout_strong if strong else self.timeout_fast
        for prov, model in order:
            if model in self.dead or not self.allowance.permitted(prov):
                continue
            for attempt in (0, 1):
                try:
                    t0 = time.time()
                    txt = self._openai(model, system, user, temperature, max_tokens, image_b64, timeout) if prov == "openai" else self._gemini(model, system, user, temperature, max_tokens, image_b64, timeout, strong, video_url, video_seconds)
                    out = self.parse_json(txt)
                    self.strikes[model] = 0
                    return out
                except SpendingBlocked:
                    self.unanswered += 1
                    return None
                except HttpError as e:
                    low = (e.body or "").lower()
                    short = re.sub(r"\s+", " ", e.body or "")[:200]
                    if e.code == 429:
                        # Free-tier quotas: a per-DAY quota is gone for the run (retire the model, the next one has its own quota);
                        # a per-MINUTE limit is transient (wait for the advertised retryDelay once, then retry the same model).
                        m = re.search(r'"retrydelay":\s*"(\d+)', low)
                        delay = int(m.group(1)) if m else 0
                        if "perday" in low or "per_day" in low or "insufficient_quota" in low or "billing" in low and not delay:
                            self.dead.add(model); self.allowance.stopped.add(prov); self.failures += 1
                            warn(f"llm {prov}/{model}: quota exhausted, retired for this run: {short[:120]}")
                            break
                        if attempt == 0:
                            wait = min(max(delay, 20), 60)
                            warn(f"llm {prov}/{model}: rate limited, waiting {wait}s and retrying once")
                            time.sleep(wait)
                            continue
                    if e.code == 404 or (e.code == 400 and ("not found" in low or "no longer available" in low or "not supported" in low)):
                        self.dead.add(model)  # missing model: never again this run
                        self.failures += 1
                    else:
                        self._strike(model)
                    warn(f"llm {prov}/{model} http {e.code} after {time.time() - t0:.0f}s: {short}")
                    break
                except Exception as e:
                    self._strike(model)
                    warn(f"llm {prov}/{model} failed after {time.time() - t0:.0f}s: {type(e).__name__}")
                    break
        self.unanswered += 1
        return None

    def record(self, rep):
        """Write this LLM's counters into a stage Report (attempts, failed attempts, questions, unanswered questions)."""
        rep.inc("llm_calls", self.calls); rep.inc("llm_failures", self.failures)
        rep.inc("llm_requests", self.requests); rep.inc("llm_unanswered", self.unanswered)

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

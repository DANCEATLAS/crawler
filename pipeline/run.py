"""CLI entry point.

  python -m pipeline.run discover [--max-new N]
  python -m pipeline.run research [--new N] [--enrich N] [--only slug,slug]
  python -m pipeline.run qc [--only slug,slug]
  python -m pipeline.run hero_qc [--budget N] [--no-vision]
  python -m pipeline.run sync [--only slug,slug]
  python -m pipeline.run report
  python -m pipeline.run bootstrap    # download app_catalog.json if missing (APP_CATALOG_URL)
  python -m pipeline.run build        # publish public/catalog/* (QC-gated) + regenerate dance_list.json
  python -m pipeline.run pedagogy [--budget N]   # study N tutorial videos: how the best teachers teach (pedagogy/, ULTIMATE_TEACHER.md)
  python -m pipeline.run episodes [--only slug]  # episode packs for every published profile (episodes/, public/catalog/episodes.json)
  python -m pipeline.run translate [--budget N]  # narration of gap-free packs into TRANSLATE_LANGS (episodes/i18n/<lang>/)
  python -m pipeline.run health       # self-tuning (pipeline_state/tuning.json) and lessons learned from QC (pipeline_state/lessons_learned.json)
  python -m pipeline.run daily        # bootstrap → health → audit → discover → research → qc → hero_qc → build → pedagogy → episodes → translate → sync → report
  python -m pipeline.run selftest     # offline checks, no network
"""
import sys, os, argparse, json, traceback

def _env_int(k, d):
    try:
        return int(os.environ.get(k, d))
    except Exception:
        return d

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("stage")
    ap.add_argument("--max-new", type=int, default=_env_int("DISCOVER_MAX_NEW", 40))
    ap.add_argument("--new", type=int, default=_env_int("RESEARCH_NEW", 15))
    ap.add_argument("--enrich", type=int, default=_env_int("RESEARCH_ENRICH", 15))
    ap.add_argument("--budget", type=int, default=_env_int("HERO_QC_BUDGET", 60))
    ap.add_argument("--no-vision", action="store_true")
    ap.add_argument("--only", type=str, default="")
    a = ap.parse_args(argv)
    only = [s.strip() for s in a.only.split(",") if s.strip()] or None
    results = {}
    stages = ["bootstrap", "health", "audit", "discover", "research", "qc", "hero_qc", "build", "pedagogy", "episodes", "translate", "sync", "report"] if a.stage == "daily" else [a.stage]
    daily = a.stage == "daily"
    def budget(name, value):
        """In the daily run the budgets follow pipeline_state/tuning.json (health stage): less when the models were failing, never more than set."""
        if not daily:
            return value
        from .health import scaled
        return scaled(name, value)
    for st in stages:
        try:
            if st == "bootstrap":
                from . import build_catalog; results[st] = {"ok": build_catalog.bootstrap()}
            elif st == "audit":
                from . import audit; results[st] = audit.run(llm_budget=_env_int("AUDIT_LLM_BUDGET", 300))
            elif st == "build":
                from . import build_catalog; results[st] = build_catalog.run(include_review=os.environ.get("INCLUDE_REVIEW") == "true"); build_catalog.regen_dance_list()
            elif st == "discover":
                from . import discover; results[st] = discover.run(max_new=a.max_new)
            elif st == "health":
                from . import health; results[st] = health.run()
            elif st == "research":
                from . import research; results[st] = research.run(budget_new=budget("RESEARCH_NEW", a.new), budget_enrich=budget("RESEARCH_ENRICH", a.enrich), only=only)
            elif st == "qc":
                from . import qc; results[st] = qc.run(only=only)
            elif st == "hero_qc":
                from . import hero_qc; results[st] = hero_qc.run(budget=budget("HERO_QC_BUDGET", a.budget), use_vision=not a.no_vision, only=only)
            elif st == "pedagogy":
                from . import pedagogy; results[st] = pedagogy.run(budget=budget("PEDAGOGY_BUDGET", _env_int("PEDAGOGY_BUDGET", 6)) if daily else min(a.budget, 12), only=only)
            elif st == "episodes":
                from . import episodes; results[st] = episodes.run(polish_budget=budget("EPISODE_POLISH", _env_int("EPISODE_POLISH", 0)), only=only)
            elif st == "translate":
                from . import translate; results[st] = translate.run(budget=budget("TRANSLATE_BUDGET", _env_int("TRANSLATE_BUDGET", 6)) if daily else min(a.budget, 12), only=only)
            elif st == "sync":
                from . import sync; results[st] = sync.run(only=only)
            elif st == "report":
                from . import report; results[st] = report.run()
            elif st == "selftest":
                from . import selftest; results[st] = selftest.run()
            else:
                print("unknown stage", st); return 2
        except Exception as e:
            traceback.print_exc()
            results[st] = {"error": str(e)}
            if a.stage != "daily":
                return 1
    print("SUMMARY", json.dumps({k: (v.get("counters") if isinstance(v, dict) else v) for k, v in results.items()}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())

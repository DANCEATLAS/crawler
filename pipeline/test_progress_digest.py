"""Offline safeguards for honest, accessible weekly reporting."""
import datetime as dt
import json
import re
import tempfile
import unittest
from pathlib import Path
from . import weekly_report as w
from . import progress_digest as d

WHEN = dt.datetime(2026, 11, 10, 4, 0, tzinfo=dt.timezone.utc)

class ProgressDigestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def put(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))

    def fixture(self):
        self.put('public/catalog/dances.app.json', {'styles': {'live': {'research_gate':'publish'}}})
        self.put('pipeline_state/qc_index.json', {s: {'publish_gate':'publish'} for s in ('live','removed')})
        self.put('pipeline_state/research_index.json', {s: {'status':'researched'} for s in ('live','removed')})
        for slug in ('live','removed'):
            self.put(f'research_results/{slug}.json', {'status':'researched','profile':{'name':slug},'citation':{}})
        self.put('public/catalog/episodes.json', {'packs':{s:{'status':'complete','built_at':'2026-11-09T10:00:00Z','polished':False} for s in ('live','removed')},'languages':['es','fr','de'],'translations':99})
        self.put('episodes/i18n/es/live.json', {'slug':'live','lang':'es','master_built_at':'2026-11-09T10:00:00Z','reviewed_by_native_speaker':True,'scenes_master_kept':1})
        self.put('episodes/i18n/fr/live.json', {'slug':'live','lang':'fr','master_built_at':'2026-11-08T10:00:00Z','reviewed_by_native_speaker':True})
        self.put('episodes/i18n/es/removed.json', {'slug':'removed','lang':'es','master_built_at':'2026-11-09T10:00:00Z'})
        return w.measure(str(self.root))

    def test_removed_profiles_and_scripts_are_not_growth(self):
        m=self.fixture()
        self.assertEqual((m['published'],m['episode_packs'],m['episode_stored']), (1,1,2))

    def test_languages_measure_files_and_current_review_not_targets(self):
        m=self.fixture()
        self.assertEqual((m['translations'],m['languages'],m['languages_configured']), (2,2,3))
        self.assertEqual((m['translations_current'],m['translations_reviewed']), (1,0))
        self.assertIsNone(m['viral_entries'])

    def test_zero_and_unknown_are_distinct(self):
        self.put('viral_challenges_verified.json', [])
        self.assertEqual(w.measure(str(self.root))['viral_entries'],0)
        self.assertEqual(d.change(0,None),'earlier comparison unavailable')

    def test_active_readiness_missing_and_stale_are_explicit(self):
        self.assertIn("unavailable", d.readiness_summary({}, WHEN))
        old = {"activation": {"count": 50, "evaluated_on": "2026-10-01", "states": {"ready_for_activation": 1}}}
        self.assertIn("Needs recheck", d.readiness_summary(old, WHEN))

    def test_missing_stale_or_future_action_does_not_request_login(self):
        for day in ('2026-01-01','2027-01-01','bad',None):
            m={'vision':{'owner_action':{'status':'open','verified_at':day,'title':'Sign in'}}}
            self.assertEqual(d.owner_action(m,WHEN)['title'],'No current request for you')

    def test_resolved_action_removes_signin(self):
        m={'vision':{'owner_action':{'status':'resolved','verified_at':'2026-11-10'}}}
        self.assertEqual(d.owner_action(m,WHEN)['title'],'Nothing needs you this week')

    def test_equal_database_totals_do_not_claim_a_sync_gap(self):
        m=self.fixture(); m.update(database_dances=1, database_at='2026-11-10')
        text=' '.join(d.operating_notes(m,w.health([], '2026-11-03'),WHEN))
        self.assertIn('counts match',text)
        self.assertNotIn('counts differ',text)

    def test_platform_observation_is_dated_and_expires(self):
        m=self.fixture(); m['vision']={'platform_observation':{'text':'Storage needs review.','verified_at':'2026-10-01','valid_days':14}}
        text=' '.join(d.operating_notes(m,w.health([], '2026-11-03'),WHEN))
        self.assertIn('Platform check (2026-10-01)',text)
        self.assertIn('Needs recheck',text)

    def test_outdated_capabilities_never_presented_as_current(self):
        m=self.fixture(); m['vision']={'reviewed_at':'2026-01-01','areas':[{'id':'bdf','title':'BDF','status':'Implemented','text':'Old claim'}]}
        self.assertEqual(d.vision_rows(m,WHEN)[0]['status'],'Needs recheck')

    def test_empty_register_never_implies_vision_complete(self):
        self.assertEqual(d.vision_rows(self.fixture(),WHEN)[0]['status'],'Not recorded')

    def test_health_time_window_and_model_failures(self):
        runs=[{'stage':'report','finished':day,'counters':{'llm_failures':3,'llm_unanswered':1},'errors':[]} for day in ('2026-10-01T00:00:00Z','2026-11-09T00:00:00Z','2026-12-01T00:00:00Z')]
        h=w.health(runs,'2026-11-03T04:00:00Z','2026-11-10T04:00:00Z')
        self.assertEqual((h['days'],h['retries'],h['unanswered']),(1,3,1))

    def test_no_errors_is_not_claim_of_free_cost_or_validated_release(self):
        m=self.fixture(); h=w.health([], '2026-11-03')
        text=' '.join(d.operating_notes(m,h,WHEN))
        self.assertIn('Actual spending and remaining balance are not measured',text)
        self.assertIn('No recent completed report',text)

    def test_html_escapes_content_and_unsafe_action_url(self):
        m=self.fixture(); m['vision']={'reviewed_at':'2026-11-10','areas':[{'id':'x','title':'<script>bad</script>','text':'A & B','status':'Draft'}], 'owner_action':{'status':'open','verified_at':'2026-11-10','title':'Sign in','url':'javascript:alert(1)'}}
        page=w.render_email_html(m,None,None,None,{},[],WHEN)
        self.assertNotIn('<script>',page); self.assertNotIn('javascript:',page)
        self.assertIn('&lt;script&gt;',page); self.assertIn("font-size:34px",page)
        self.assertLess(len(page.encode()),90000)

    def test_summary_retains_weekly_duplicate_guard_stamp(self):
        m=self.fixture(); md=w.render_md(m,None,None,None,{},[],WHEN)
        self.assertRegex(md,r'weekly report · [A-Za-z]{3} [0-9]{2} [A-Za-z]{3} [0-9]{4}')
        self.assertIn('not validated classes',md)
        self.assertNotIn('Movie-ready',w.email_subject(m,None,WHEN))

    def test_register_covers_every_vision_requirement(self):
        v=json.loads((Path(__file__).resolve().parents[1]/'pipeline_state/vision_status.json').read_text())
        ids={i for a in v['areas'] for i in a['vision_ids']}
        self.assertEqual(ids,{f'V{i:02}' for i in range(1,19)})
        self.assertEqual(len({a['id'] for a in v['areas']}),len(v['areas']))

if __name__=='__main__':
    unittest.main()

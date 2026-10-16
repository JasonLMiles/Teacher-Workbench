import importlib.util,json,tempfile,unittest,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[2];paths={p.name:str(p) for p in (BASE/'skills').iterdir() if p.is_dir()}
def mod(name,file):
 p=Path(paths['tw-'+name])/'scripts'/file;s=importlib.util.spec_from_file_location(name.replace('-','_'),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
kg=mod('learning-commons','knowledge_graph.py');wf=mod('recurring-workflows','workflow_plan.py');rv=mod('pedagogical-review','review_report.py')
class Helpers(unittest.TestCase):
 def test_api_pagination_preserves_records(self):
  seen=[]
  def transport(url,key):
   seen.append(url);return {'data':[{'identifier':str(len(seen)),'license':'retained'}],'pagination':{'hasMore':len(seen)==1,'nextCursor':'next' if len(seen)==1 else None}}
  r=kg.api('standards-frameworks',{'jurisdiction':'California'},key='synthetic',transport=transport)
  self.assertTrue(r['complete']);self.assertEqual(len(r['data']),2);self.assertIn('cursor=next',seen[1]);self.assertEqual(r['data'][0]['license'],'retained')
 def test_api_partial_is_explicit(self):
  r=kg.api('courses',max_pages=1,key='synthetic',transport=lambda u,k:{'data':[],'pagination':{'hasMore':True,'nextCursor':'more'}})
  self.assertFalse(r['complete']);self.assertEqual(r['next_cursor'],'more')
 def test_api_cycle_rejected(self):
  with self.assertRaises(kg.ReadError):kg.api('courses',key='synthetic',transport=lambda u,k:{'data':[],'pagination':{'hasMore':True,'nextCursor':'same'}})
 def test_api_arbitrary_host_rejected(self):
  with self.assertRaises(kg.ReadError):kg.api('https://other.invalid/',key='synthetic')
 def test_api_secret_query_rejected(self):
  with self.assertRaises(kg.ReadError):kg.api('courses',{'apiKey':'example'},key='synthetic')
 def test_redirect_rejected(self):
  with self.assertRaises(kg.ReadError):kg.NoRedirect().redirect_request(None,None,None,None,None,None)
 def test_api_bad_schema_rejected(self):
  with self.assertRaises(kg.ReadError):kg.api('courses',key='synthetic',transport=lambda u,k:{'items':[]})
 def test_local_distinguishes_jurisdiction(self):
  r=kg.local(Path(__file__).resolve().parent/'cases/nodes.jsonl',{'statementCode':'SYN.3.A','jurisdiction':'California'})
  self.assertEqual(len(r['data']),1);self.assertEqual(r['data'][0]['line'],1);self.assertTrue(r['complete'])
 def test_local_partial(self):
  r=kg.local(Path(__file__).resolve().parent/'cases/nodes.jsonl',{'statementCode':'SYN.3.A'},max_records=1)
  self.assertFalse(r['complete'])
 def brief(self):return json.loads((Path(paths['tw-recurring-workflows'])/'assets/workflow-brief.json').read_text())
 def test_schedule_is_draft_timezone_count(self):
  r=wf.plan(self.brief());self.assertEqual(r['status'],'draft_not_scheduled');self.assertIn('DTSTART;TZID=America/Los_Angeles:20261002T153000',r['payload']['schedule']);self.assertIn('COUNT=4',r['payload']['schedule']);self.assertEqual(r['first_occurrence_utc'],'2026-10-02T22:30:00+00:00')
 def test_bad_timezone(self):
  b=self.brief();b['timezone']='Made/Up'
  with self.assertRaises(ValueError):wf.plan(b)
 def test_dst_nonexistent(self):
  b=self.brief();b.update(start_local='2027-03-14T02:30:00',weekdays=['SU'])
  with self.assertRaises(ValueError):wf.plan(b)
 def test_dst_ambiguous(self):
  b=self.brief();b.update(start_local='2026-11-01T01:30:00',weekdays=['SU'])
  with self.assertRaises(ValueError):wf.plan(b)
 def test_weekday_mismatch(self):
  b=self.brief();b['weekdays']=['MO']
  with self.assertRaises(ValueError):wf.plan(b)
 def test_holiday_invocation_disclosed(self):
  b=self.brief();b['excluded_dates']=['2026-10-09'];r=wf.plan(b)
  self.assertIn('2026-10-09',r['payload']['prompt']);self.assertIn('still occur',r['exclusion_behavior'])
 def review(self):return {'artifact':'synthetic','reviewer':'test','sets':['common','math','formative'],'ratings':[]}
 def test_omissions_not_passed(self):
  r=rv.report(self.review());self.assertEqual(r['disposition'],'incomplete_review');self.assertEqual(r['counts']['unreviewed'],10)
 def test_blocker_overrides(self):
  b=self.review();b['ratings']=[{'id':'C2','status':'fail','locator':'item1/key','reason':'Wrong answer'}];r=rv.report(b)
  self.assertEqual(r['disposition'],'revise_before_use');self.assertEqual(r['blockers'],['C2']);self.assertEqual(len(r['unresolved']),9)
 def test_pass_needs_locator(self):
  b=self.review();b['ratings']=[{'id':'C2','status':'pass','reason':'okay'}]
  with self.assertRaises(ValueError):rv.report(b)
 def test_required_not_omittable(self):
  b=self.review();b['ratings']=[{'id':'C2','status':'not_applicable','reason':'Not convenient'}]
  with self.assertRaises(ValueError):rv.report(b)
 def test_duplicate_rejected(self):
  b=self.review();r={'id':'C2','status':'pass','locator':'item1','reason':'checked'};b['ratings']=[r,r]
  with self.assertRaises(ValueError):rv.report(b)
if __name__=='__main__':unittest.main(verbosity=2)

"""Synthetic numerical and policy-edge checks; no student records or network."""
import copy, importlib.util, json, math, os, sys, unittest
from decimal import Decimal
from pathlib import Path
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
MAP=json.loads(Path(os.environ['TEACHER_WORKBENCH_SKILL_MAP']).read_text()) if os.getenv('TEACHER_WORKBENCH_SKILL_MAP') else {}
def skill(n):return Path(MAP[n]) if n in MAP else ROOT/'skills'/n
def load(n,f):
 p=skill(n)/'scripts'/f;spec=importlib.util.spec_from_file_location(p.stem,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
G='tw-grade-calculations';S='tw-standards-progress-analysis';P='tw-pre-post-growth-analysis'
grade=load(G,'grade_engine.py');stand=load(S,'standards_analysis.py');growth=load(P,'growth_analysis.py')
def fixture(n,f):return json.loads((skill(n)/'assets'/f).read_text())
def gf():return fixture(G,'grade-input.example.json')
def sf():return fixture(S,'standards-input.example.json')
def pf():return fixture(P,'growth-input.example.json')
def student(d):return grade.calculate(d)['students'][0]
def profile(d,sid='A',std='S1'):return next(r for r in stand.analyze(d)['profiles'] if r['student_code']==sid and r['standard_id']==std)
def simple_grade(scores):
 d=gf();d['policy'].update(category_weights=None,drop_lowest=0,extra_credit='forbid',attempts='latest',missing='exclude')
 d['records']=[{'student_code':'X','assignment_id':str(i),'attempt_order':1,'category':'Work','earned':v,'possible':m,'status':'observed'} for i,(v,m) in enumerate(scores)]
 return d
class GrowthChecks(unittest.TestCase):
 def test_pair_ids_not_row_order_and_attrition(self):
  r=growth.analyze(pf());self.assertEqual(r['summary']['matched_n'],3);self.assertEqual([x['student_code'] for x in r['pairs']],['A','B','C']);self.assertEqual(r['audit']['excluded_n'],2)
  self.assertAlmostEqual(r['summary']['mean_change'],4);self.assertAlmostEqual(r['summary']['sd_change'],2);self.assertAlmostEqual(r['summary']['standardized_change']['d_z_change_over_sd_change'],2)
 def test_distinct_standardizers(self):
  r=growth.analyze(pf())['summary']['standardized_change'];sx=10;sy=math.sqrt(84)
  self.assertAlmostEqual(r['d_av_change_over_mean_pre_post_sd'],4/((sx+sy)/2));self.assertAlmostEqual(r['change_over_baseline_sd'],.4)
 def test_missing_not_zero_and_zero_baseline(self):
  d=pf();r=growth.analyze(d);self.assertIsNone(next(x for x in r['pairs'] if x['student_code']=='C')['relative_percent_change'])
  d['pre'][0].update(status='absent',score=None);self.assertEqual(growth.analyze(d)['summary']['matched_n'],2)
 def test_percentage_points_and_direction(self):
  d=pf();d['policy'].update(analysis_scale='percentage',pre_max=40,post_max=50,direction='lower');d['pre']=[{'student_code':'X','score':20,'status':'observed'}];d['post']=[{'student_code':'X','score':20,'status':'observed'}]
  r=growth.analyze(d);self.assertEqual(r['units'],'percentage points');self.assertEqual(r['summary']['mean_change'],-10);self.assertEqual(r['summary']['improved'],1)
 def test_ceiling_normalized_and_undefined_sd(self):
  d=pf();d['policy']['normalized_gain']=True;d['pre']=[{'student_code':'X','score':100,'status':'observed'}];d['post']=copy.deepcopy(d['pre']);r=growth.analyze(d)
  self.assertIsNone(r['pairs'][0]['normalized_gain']);self.assertEqual(r['summary']['normalized_gain']['ceiling_excluded_n'],1);self.assertIsNone(r['summary']['standardized_change']['d_z_change_over_sd_change'])
 def test_empty_pairs(self):
  d=pf();d['post']=[];r=growth.analyze(d);self.assertEqual(r['summary']['matched_n'],0);self.assertIsNone(r['summary']['mean_change'])
 def test_paired_interval(self):
  d=pf();d['policy'].update(inference=True,confidence=.95);r=growth.analyze(d)['inference']
  if r['status']=='unavailable':self.skipTest(r['reason'])
  self.assertEqual(r['df'],2);self.assertAlmostEqual(r['t'],math.sqrt(12));self.assertAlmostEqual(r['mean_change_ci'][0],4-4.302652729911275*2/math.sqrt(3),places=8);self.assertGreater(r['two_sided_p'],.05)
 def test_invalid_inputs_rejected(self):
  for patch in ({'comparable':False},{'score_min':100},{'inference':'yes'},{'normalized_gain':'no'}):
   d=pf();d['policy'].update(patch)
   with self.assertRaises(ValueError):growth.analyze(d)
  d=pf();d['pre'].append(d['pre'][0])
  with self.assertRaises(ValueError):growth.analyze(d)
class StandardsChecks(unittest.TestCase):
 def test_latest_median_and_missing_coverage(self):
  d=sf();self.assertEqual(profile(d)['summary'],3);d['policy']['method']='median_low';self.assertEqual(profile(d)['summary'],2)
  r=stand.analyze(d)['rollups'][0];self.assertIsNone(r['value']);self.assertEqual(r['coverage'],.5);self.assertEqual(r['essential_missing'],['S2'])
 def test_ordinal_lower_median_mode_tie_and_consistency(self):
  d=sf();d['policy'].update(method='median_low',window=2);self.assertEqual(profile(d)['summary'],2)
  d['policy']['method']='mode_recent';self.assertEqual(profile(d)['summary'],3)
  d['policy']['method']='recent_consistent_min';self.assertEqual(profile(d)['summary'],2)
 def test_zero_remains_observed(self):
  d=sf();d['records'][0]['value']=0;r=profile(d);self.assertEqual(r['observed_n'],3);self.assertEqual(r['observed_range'][0],0);self.assertEqual(r['missing_states'],{'missing':1})
 def test_ordinal_numeric_aggregation_blocked(self):
  d=sf();d['policy']['method']='mean'
  with self.assertRaises(ValueError):stand.analyze(d)
 def test_interval_decay_and_irregular_time_slope(self):
  d=sf();d['policy'].update(scale_type='interval',interval_assumption=True,scale_min=0,scale_max=4,method='decaying_mean',decay=.5)
  observed=[r for r in d['records'] if r['student_code']=='A' and r['standard_id']=='S1' and r['status']=='observed']
  for r,date,val in zip(observed,['2026-09-01','2026-09-03','2026-09-07'],[1,2,4]):r.update(date=date,value=val)
  r=profile(d);self.assertAlmostEqual(r['summary'],(1*.25+2*.5+4)/1.75);self.assertAlmostEqual(r['descriptive_slope_per_day'],.5)
 def test_weighted_rollup_with_explicit_partial_coverage(self):
  d=sf();d['policy'].update(scale_type='interval',interval_assumption=True,scale_min=0,scale_max=4);d['rollups'][0].update(method='weighted_mean',min_coverage=.5,weights={'S1':.7,'S2':.3})
  r=stand.analyze(d)['rollups'][0];self.assertAlmostEqual(r['value'],3);self.assertTrue(r['weight_renormalization']);self.assertFalse(r['essential_gate_met']);self.assertEqual(r['meeting_rate_all_required'],.5)
 def test_future_exclusion_and_staleness(self):
  d=sf();future=copy.deepcopy(d['records'][0]);future.update(task_id='future',date='2027-01-01');d['records'].append(future);d['policy']['stale_days']=0
  r=stand.analyze(d);self.assertEqual(len(r['audit']['excluded']),1);self.assertTrue(profile(d)['stale'])
 def test_duplicate_ambiguous_and_nested_evidence_rejected(self):
  for kind in ('duplicate','ambiguous','nested'):
   d=sf()
   if kind=='duplicate':d['records'].append(copy.deepcopy(d['records'][0]))
   elif kind=='ambiguous':r=copy.deepcopy(d['records'][0]);r['task_id']='another';d['records'].append(r)
   else:d['rollups'][0]['members']=['nested-domain']
   with self.assertRaises(ValueError):stand.analyze(d)
class GradeChecks(unittest.TestCase):
 def test_weighted_retake_drop_and_bonus(self):
  r=student(gf());self.assertEqual(r['percent_rounded'],'91.33');self.assertEqual(r['threshold_label'],'A');self.assertEqual(r['categories'][0]['possible_regular'],'30')
 def test_missing_zero_changes_denominator(self):
  d=gf();d['policy']['missing']='zero';r=student(d);self.assertEqual(r['percent_rounded'],'82.00');self.assertEqual(r['categories'][0]['possible_regular'],'40')
 def test_equal_items_differs_from_points(self):
  d=simple_grade([(8,10),(18,20)]);self.assertAlmostEqual(float(student(d)['percent_unrounded']),100*26/30);d['policy']['aggregation']='equal_items';self.assertEqual(Decimal(student(d)['percent_unrounded']),85)
 def test_rounding_threshold_basis_and_ties(self):
  d=simple_grade([('89.995',100)]);d['policy'].update(threshold_basis='raw',round_digits=2,rounding='half_up');self.assertEqual(student(d)['threshold_label'],'B');d['policy']['threshold_basis']='rounded';self.assertEqual(student(d)['threshold_label'],'A')
  d['records'][0]['earned']='89.985';self.assertEqual(student(d)['percent_rounded'],'89.99');d['policy']['rounding']='half_even';self.assertEqual(student(d)['percent_rounded'],'89.98')
 def test_empty_category_rules(self):
  d=gf();d['records']=[r for r in d['records'] if r['category']=='Tests'];d['policy']['empty_categories']='error';self.assertIsNone(student(d)['percent_unrounded']);d['policy']['empty_categories']='renormalize';r=student(d);self.assertEqual(Decimal(r['percent_unrounded']),90);self.assertTrue(r['weights_renormalized'])
 def test_latest_and_highest_differ(self):
  d=simple_grade([(9,10)]);r=copy.deepcopy(d['records'][0]);r.update(attempt_order=2,earned=5);d['records'].append(r);self.assertEqual(Decimal(student(d)['percent_unrounded']),50);d['policy']['attempts']='highest';self.assertEqual(Decimal(student(d)['percent_unrounded']),90)
 def test_latest_missing_not_silently_previous(self):
  d=simple_grade([(9,10)]);r=copy.deepcopy(d['records'][0]);r.update(attempt_order=2,status='missing',earned=None);d['records'].append(r);self.assertIsNone(student(d)['percent_unrounded'])
 def test_minimum_kept_cap_floor_and_all_missing(self):
  d=simple_grade([(4,10),(8,10)]);d['policy'].update(drop_lowest=9,drop_min_keep=1,cap_pct=75);r=student(d);self.assertEqual(r['categories'][0]['actual_drops'],1);self.assertEqual(Decimal(r['percent_unrounded']),75)
  d['policy'].update(cap_pct=None,floor_pct=85);self.assertEqual(Decimal(student(d)['percent_unrounded']),85)
  for r in d['records']:r.update(status='missing',earned=None)
  self.assertIsNone(student(d)['percent_unrounded'])
 def test_bonus_without_denominator(self):
  d=gf();d['records']=[r for r in d['records'] if r.get('extra_credit')];self.assertIsNone(student(d)['percent_unrounded'])
 def test_unsupported_or_invalid_policy_rejected(self):
  for patch in ({'category_weights':{'Practice':.4,'Tests':.5}},{'aggregation':'mystery'},{'unknown_rule':1}):
   d=gf();d['policy'].update(patch)
   with self.assertRaises(ValueError):grade.calculate(d)
  d=simple_grade([('NaN',10)])
  with self.assertRaises(ValueError):grade.calculate(d)
if __name__=='__main__':unittest.main(verbosity=2)

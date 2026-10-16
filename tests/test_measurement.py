from pathlib import Path
import importlib.util, json, math, tempfile, unittest

ROOT=Path(__file__).resolve().parents[1]/'skills'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
C=module('ctt',ROOT/'tw-classical-test-theory/scripts/ctt_analyze.py')
I=module('irt',ROOT/'tw-item-response-theory/scripts/irt_known_parameter_demo.py')

class Measurement(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.p=Path(self.temp.name)
        self.cfg={'mode':'scored','omitted_policy':'zero','items':{'a':{'max_score':1},'b':{'max_score':1},'c':{'max_score':1}}}
    def tearDown(self):self.temp.cleanup()
    def run_data(self,text,cfg=None):
        (self.p/'data.csv').write_text(text)
        (self.p/'cfg.json').write_text(json.dumps(cfg or self.cfg))
        return C.analyze(self.p/'data.csv',self.p/'cfg.json')
    def test_hand_computed(self):
        r=self.run_data('anonymous_id,a,b,c\nx,1,1,1\ny,1,1,0\nz,1,0,0\nw,0,0,0\n')
        self.assertEqual(r['n_complete_cases'],4)
        self.assertEqual([i['facility_mean_over_max'] for i in r['items']],[.75,.5,.25])
        self.assertAlmostEqual(r['alpha_complete_cases'],.75)
        self.assertAlmostEqual(r['total_score_complete_cases']['sample_sd'],math.sqrt(5/3))
        self.assertAlmostEqual(r['conventional_sem_complete_cases'],math.sqrt(5/12))
        self.assertAlmostEqual(r['items'][0]['corrected_item_total_complete_cases'],3/math.sqrt(33))
    def test_raw_and_scored_agree(self):
        a=ROOT/'tw-classical-test-theory/assets'
        r=C.analyze(a/'synthetic-responses.csv',a/'scoring-config.json')
        self.assertAlmostEqual(r['alpha_complete_cases'],.75)
        self.assertEqual(r['items'][0]['option_counts_observed_valid'],{'A':1,'B':3,'C':0})
    def test_missing_distinctions(self):
        cfg=self.cfg|{'invalid_policy':'missing'}
        r=self.run_data('anonymous_id,a,b,c\nx,1,OM,1\ny,NA,1,0\nz,1,INV,0\n',cfg)
        self.assertEqual(r['n_complete_cases'],1)
        self.assertEqual(r['items'][1]['n_omitted'],1)
        self.assertEqual(r['items'][0]['n_not_administered'],1)
        self.assertEqual(r['items'][1]['n_invalid'],1)
        self.assertEqual(r['items'][1]['n_scored'],2)
        cfg['omitted_policy']='missing'
        r=self.run_data('anonymous_id,a,b,c\nx,1,OM,1\ny,NA,1,0\nz,1,INV,0\n',cfg)
        self.assertEqual(r['n_complete_cases'],0)
        self.assertEqual(r['items'][1]['n_scored'],1)
        self.assertIsNone(r['alpha_complete_cases'])
    def test_constant_and_one_case(self):
        for data in ['anonymous_id,a,b,c\nx,1,1,1\ny,1,1,1\n','anonymous_id,a,b,c\nx,1,0,1\n']:
            r=self.run_data(data)
            self.assertIsNone(r['alpha_complete_cases']);self.assertIsNone(r['conventional_sem_complete_cases'])
    def test_negative_alpha_not_hidden(self):
        cfg={'mode':'scored','omitted_policy':'zero','items':{'a':{'max_score':1},'b':{'max_score':1}}}
        r=self.run_data('anonymous_id,a,b\nx,1,0\ny,1,0\nz,0,1\nw,0,0\n',cfg)
        self.assertLess(r['alpha_complete_cases'],0);self.assertIsNone(r['conventional_sem_complete_cases'])
    def test_bad_data_rejected(self):
        bad=['anonymous_id,a,b,c\nx,1,1,1\nx,0,0,0\n','anonymous_id,a,b,c\nx,1,,1\n','anonymous_id,a,b,c\nx,2,1,1\n','anonymous_id,a,b,c\nx,nan,1,1\n','anonymous_id,a,b,c,student_name\nx,1,1,1,Name\n']
        for data in bad:
            with self.assertRaises(ValueError):self.run_data(data)
    def test_key_is_not_changed(self):
        a=ROOT/'tw-classical-test-theory/assets'
        cfg=json.loads((a/'scoring-config.json').read_text());cfg['items']['Q3']['key']='A'
        (self.p/'cfg.json').write_text(json.dumps(cfg))
        r=C.analyze(a/'synthetic-responses.csv',self.p/'cfg.json')
        self.assertEqual(r['items'][2]['key'],'A')
        self.assertLess(r['items'][2]['corrected_item_total_complete_cases'],0)
    def test_irt_known_points_and_information(self):
        p,info=I.curve(0,1,0,0,1)
        self.assertEqual(p,.5);self.assertEqual(info,.25)
        p,info=I.curve(.5,1.2,.5,.2,1)
        self.assertAlmostEqual(p,.6);self.assertAlmostEqual(info,.24)
        # independent numerical derivative check of information
        h=1e-5;t=.7;a=1.4;b=-.2;c=.15;d=1.7
        p,info=I.curve(t,a,b,c,d)
        derivative=(I.curve(t+h,a,b,c,d)[0]-I.curve(t-h,a,b,c,d)[0])/(2*h)
        self.assertAlmostEqual(info,derivative**2/(p*(1-p)),places=8)
        for t in (-1000,1000):
            p,info=I.curve(t,1,0)
            self.assertTrue(0<=p<=1);self.assertTrue(math.isfinite(info))
    def test_irt_demo_sum_and_invalid_config(self):
        f=ROOT/'tw-item-response-theory/assets/demo-parameters.json'
        r=I.demo(f)
        for row in r['rows']:
            self.assertAlmostEqual(row['test_information_assuming_local_independence'],sum(x['information'] for x in row['items']))
        cfg=json.loads(f.read_text());cfg['items'][0]['a']=-1
        (self.p/'invalid.json').write_text(json.dumps(cfg))
        with self.assertRaises(ValueError):I.demo(self.p/'invalid.json')

if __name__=='__main__':unittest.main(verbosity=2)

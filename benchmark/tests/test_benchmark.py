import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from core import CASES, ci_bootstrap_by_task, parse_codex_usage
from graders.code_oracles import TESTS

class BenchmarkTests(unittest.TestCase):
    def test_manifest(self):
        self.assertEqual(len(CASES),30)
        self.assertEqual(len(set(c['id'] for c in CASES)),30)
        self.assertEqual(sum(c['kind']=='code' for c in CASES),20)
        self.assertEqual(sum(c['kind']=='decision' for c in CASES),10)
        self.assertEqual(set(TESTS),{c['id'] for c in CASES if c['kind']=='code'})
        self.assertTrue(all(len(v)>=3 for v in TESTS.values()))
    def test_bootstrap_clusters(self):
        ci=ci_bootstrap_by_task({'task1':[1,1],'task2':[.5,.5],'task3':[1,1]},seed=8)
        self.assertGreater(ci[0],0)
    def test_codex_usage_absent_not_zero(self):
        self.assertIsNone(parse_codex_usage('invalid')['total_tokens'])
    def test_harness_smoke_never_claims_effect(self):
        with tempfile.TemporaryDirectory() as d:
            run=Path(d)/'smoke'
            subprocess.run([sys.executable,str(ROOT/'run.py'),'--adapter','mock','--repeats','1','--case','c01-normalize','--case','d01-onboarding','--out',str(run)],check=True,capture_output=True,text=True)
            subprocess.run([sys.executable,str(ROOT/'report.py'),'--run',str(run)],check=True,capture_output=True,text=True)
            summary=json.loads((run/'summary.json').read_text())
            self.assertEqual(summary['verdict'],'SMOKE_TEST_ONLY')
            self.assertEqual(summary['trial_count'],4)
            self.assertTrue((run/'report.html').is_file())
            self.assertTrue(list((run/'trials').rglob('trace.jsonl')))
    def test_oracle_is_independent(self):
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/'solution.py'
            f.write_text('def solve(payload):\n    return sorted(set(x.strip().lower() for x in payload if x.strip()))\n')
            # Correct on some inputs but wrong on insertion order; detect via negative test
            p=subprocess.run([sys.executable,'-I',str(ROOT/'graders'/'grade_code.py'),'c01-normalize',d],capture_output=True,text=True,check=True)
            self.assertLess(json.loads(p.stdout)['passed'],json.loads(p.stdout)['total'])

if __name__=='__main__':unittest.main()

class BlindJudgingTests(unittest.TestCase):
    def test_export_hides_arm_identities_and_import_validates(self):
        from judge import prepare, import_grades
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            run=p/'experiment'
            packet=p/'reviewer'/'blind.json'
            subprocess.run([sys.executable,str(ROOT/'run.py'),'--adapter','mock','--repeats','1','--case','d01-onboarding','--out',str(run)],capture_output=True,text=True,check=True)
            prepare(run,packet,seed=21)
            packet_data=json.loads(packet.read_text())
            self.assertEqual(len(packet_data['pairs']),1)
            pid=packet_data['pairs'][0]['id']
            self.assertNotIn('vanilla',pid)
            self.assertNotIn('pareto',pid)
            score=p/'reviewer'/'judgments.json'
            score.write_text(json.dumps({'judge':'mock-human-schema-test','judgments':[{'id':pid,'winner':'tie','hard_violation_A':False,'hard_violation_B':False,'usable_A':False,'usable_B':False,'reason':'both mock'}]}))
            import_grades(run,score)
            result=json.loads((run/'blind_grades.json').read_text())
            self.assertEqual(result['n_valid'],1)
            subprocess.run([sys.executable,str(ROOT/'report.py'),'--run',str(run)],capture_output=True,text=True,check=True)
            self.assertEqual(json.loads((run/'summary.json').read_text())['verdict'],'SMOKE_TEST_ONLY')

class EfficiencyFirstTests(unittest.TestCase):
    """The report must never reward speed from unusable or unobserved outputs."""
    def test_quality_gate_excludes_failed_runs(self):
        from report import efficiency_ratio
        by={
            ('c01-normalize',1,'vanilla'):{'grade':{'pass':True},'wall_seconds':10,'usage':{'total_tokens':1000}},
            ('c01-normalize',1,'pareto'):{'grade':{'pass':False},'wall_seconds':1,'usage':{'total_tokens':100}},
        }
        def usable(cid,rep,op,p,a,b):return a['grade']['pass'] and b['grade']['pass']
        r=efficiency_ratio(by,['c01-normalize'],1,'pareto','vanilla','wall_seconds',usable)
        self.assertEqual(r['paired_trials'],0)
        self.assertIsNone(r['pareto_to_baseline_ratio'])

    def test_missing_tokens_are_not_zero_or_a_saving(self):
        from report import efficiency_ratio
        by={
            ('c01-normalize',1,'vanilla'):{'grade':{'pass':True},'wall_seconds':5,'usage':{'total_tokens':900}},
            ('c01-normalize',1,'pareto'):{'grade':{'pass':True},'wall_seconds':3,'usage':{'total_tokens':None}},
        }
        r=efficiency_ratio(by,['c01-normalize'],1,'pareto','vanilla','total_tokens',lambda *args:True)
        self.assertIsNone(r['pareto_to_baseline_ratio'])
        self.assertEqual(r['paired_trials'],0)

    def test_time_ratio_only_for_two_usable_runs(self):
        from report import efficiency_ratio
        by={}
        for task in ('c01-normalize','c02-count','c03-pagination'):
            by[(task,1,'vanilla')]={'wall_seconds':10,'usage':{'total_tokens':1000}}
            by[(task,1,'pareto')]={'wall_seconds':5,'usage':{'total_tokens':700}}
        r=efficiency_ratio(by,list(('c01-normalize','c02-count','c03-pagination')),1,'pareto','vanilla','wall_seconds',lambda *args:True)
        self.assertEqual(r['distinct_tasks'],3)
        self.assertAlmostEqual(r['pareto_to_baseline_ratio'],0.5)
        self.assertLess(r['task_bootstrap_95_ci_ratio'][1],0.9)

    def test_blind_grade_requires_independent_usability_flags(self):
        from judge import prepare, import_grades
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);run=p/'run';packet=p/'packet.json'
            subprocess.run([sys.executable,str(ROOT/'run.py'),'--adapter','mock','--repeats','1','--case','d01-onboarding','--out',str(run)],check=True,capture_output=True)
            prepare(run,packet,seed=12)
            token=json.loads(packet.read_text())['pairs'][0]['id']
            grades=p/'grades.json'
            grades.write_text(json.dumps({'judge':'test','judgments':[{'id':token,'winner':'A','hard_violation_A':False,'hard_violation_B':False,'reason':'not scored for usability'}]}))
            import_grades(run,grades)
            data=json.loads((run/'blind_grades.json').read_text())
            self.assertEqual(data['n_valid'],0)

    def test_contradictory_usable_and_veto_is_invalid(self):
        from judge import prepare, import_grades
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);run=p/'run';packet=p/'packet.json'
            subprocess.run([sys.executable,str(ROOT/'run.py'),'--adapter','mock','--repeats','1','--case','d01-onboarding','--out',str(run)],check=True,capture_output=True)
            prepare(run,packet,seed=42)
            token=json.loads(packet.read_text())['pairs'][0]['id']
            grades=p/'grades.json'
            grades.write_text(json.dumps({'judge':'test','judgments':[{'id':token,'winner':'A','usable_A':True,'usable_B':False,'hard_violation_A':True,'hard_violation_B':False,'reason':'contradiction'}]}))
            import_grades(run,grades)
            self.assertEqual(json.loads((run/'blind_grades.json').read_text())['n_valid'],0)

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
            score.write_text(json.dumps({'judge':'mock-human-schema-test','judgments':[{'id':pid,'winner':'tie','hard_violation_A':False,'hard_violation_B':False,'reason':'both mock'}]}))
            import_grades(run,score)
            result=json.loads((run/'blind_grades.json').read_text())
            self.assertEqual(result['n_valid'],1)
            subprocess.run([sys.executable,str(ROOT/'report.py'),'--run',str(run)],capture_output=True,text=True,check=True)
            self.assertEqual(json.loads((run/'summary.json').read_text())['verdict'],'SMOKE_TEST_ONLY')

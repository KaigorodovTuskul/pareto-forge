#!/usr/bin/env python3
"""Independent functional oracle. Run ONLY in an isolated/ephemeral sandbox.

The agent sees `solution.py`, never this script or its oracle corpus.
"""
import argparse
import importlib.util
import json
import traceback
from pathlib import Path
_oracle_spec = importlib.util.spec_from_file_location("code_oracles", str(Path(__file__).with_name("code_oracles.py")))
_oracles = importlib.util.module_from_spec(_oracle_spec)
_oracle_spec.loader.exec_module(_oracles)
TESTS = _oracles.TESTS


def grade(case_id, workspace):
    result = {'kind': 'code', 'case_id': case_id, 'passed': 0, 'total': len(TESTS[case_id]), 'errors': []}
    file = Path(workspace) / 'solution.py'
    if not file.is_file():
        result['errors'].append('solution.py not found')
        return result
    try:
        spec = importlib.util.spec_from_file_location('bench_solution', str(file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        solve = getattr(module, 'solve')
    except Exception as e:
        result['errors'].append('could not import solve: ' + repr(e))
        return result
    for i, test in enumerate(TESTS[case_id], 1):
        try:
            got = solve(test['input'])
            if got == test['expected'] and type(got) is type(test['expected']):
                result['passed'] += 1
            else:
                result['errors'].append(f'assertion {i}: returned {str(got)[:100]!r} instead of expected result')
        except Exception as e:
            result['errors'].append(f'assertion {i}: {type(e).__name__}: {str(e)[:100]}')
    if case_id == 'c20-webhook':
        # This is only a static *hint*, not proof of timing security.
        content = file.read_text(encoding='utf8',errors='replace')
        result['timing_safe_source_check'] = 'compare_digest' in content
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('case_id', choices=sorted(TESTS))
    parser.add_argument('workspace')
    args = parser.parse_args()
    print(json.dumps(grade(args.case_id, args.workspace)))

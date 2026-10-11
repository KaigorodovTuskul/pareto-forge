"""Shared benchmark I/O, no network and no third-party dependencies."""
import hashlib
import json
import random
import re
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parent
CASES = json.loads((ROOT / 'tasks.json').read_text(encoding='utf8'))['cases']
CASE_BY_ID = {case['id']: case for case in CASES}


def atomic_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf8')
    tmp.replace(path)


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def mean(values):
    return statistics.mean(values) if values else None


def ci_bootstrap_by_task(deltas_by_task, seed=71, draws=2500):
    """Paired cluster bootstrap: resample task IDs, preserving runs within each task."""
    keys = sorted(k for k, values in deltas_by_task.items() if values)
    if len(keys) < 2:
        return None
    local = random.Random(seed)
    vals = [mean(deltas_by_task[k]) for k in keys]
    sims = []
    for _ in range(draws):
        sims.append(mean([vals[local.randrange(len(vals))] for _ in vals]))
    sims.sort()
    return [round(sims[int(.025 * draws)], 4), round(sims[int(.975 * draws)], 4)]


def wilson_lower(wins, n, z=1.96):
    if n == 0:
        return None
    p = wins/n
    return ((p + z*z/(2*n)) - z*((p*(1-p)/n + z*z/(4*n*n))**0.5))/(1+z*z/n)


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_codex_usage(lines):
    """Use the final turn.completed cumulative usage, not per-turn summation."""
    usage = None
    for line in lines.splitlines():
        try:
            obj = json.loads(line)
        except (ValueError, TypeError):
            continue
        if obj.get('type') == 'turn.completed' and isinstance(obj.get('usage'), dict):
            usage = obj['usage']
    if not usage:
        return {'input_tokens': None,'output_tokens': None,'total_tokens': None,'cost_usd': None}
    inp = usage.get('input_tokens')
    out = usage.get('output_tokens')
    total = usage.get('total_tokens')
    return {'input_tokens': inp, 'output_tokens': out,
            'total_tokens': total if isinstance(total,int) else (inp + out if isinstance(inp,int) and isinstance(out,int) else None),
            'cost_usd': None}


def parse_claude_usage(text):
    try:
        d = json.loads(text)
    except ValueError:
        return {'input_tokens': None,'output_tokens': None,'total_tokens': None,'cost_usd': None}
    u = d.get('usage', {})
    if not isinstance(u,dict): u={}
    inp = u.get('input_tokens'); out = u.get('output_tokens')
    # Claude's top-level usage may count input/output differently than total_cost_usd
    return {'input_tokens': inp,'output_tokens':out,
            'total_tokens': (inp+out) if isinstance(inp,int) and isinstance(out,int) else None,
            'cost_usd': d.get('total_cost_usd') if isinstance(d.get('total_cost_usd'),(int,float)) else None}


def read_response(run_dir):
    run_dir = Path(run_dir)
    output = run_dir / 'workspace' / 'DECISION.md'
    if output.exists():
        return output.read_text(encoding='utf8', errors='replace')[:50000]
    return '[REQUIRED DECISION.md NOT CREATED]' # Missing deliverable is not a valid answer.

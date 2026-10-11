#!/usr/bin/env python3
"""Efficiency-first, quality-gated benchmark report from recorded CLI evidence only."""
import argparse
import csv
import html
import json
import math
from collections import defaultdict
from pathlib import Path
from core import CASE_BY_ID, atomic_json, ci_bootstrap_by_task, load_json, mean


def efficiency_ratio(by, cases, repeats, arm, opponent, field, usable):
    """Geometric ratio (Pareto/opponent), CI clustered by task. Only eligible successful pairs.

    Conditional comparisons may suffer selection bias; show paired count and report quality
    separately. No extrapolation from missing telemetry, and do not pool repeats as tasks.
    """
    logs = defaultdict(list)
    for case in cases:
        for rep in range(1, repeats + 1):
            a = by.get((case, rep, opponent)); b = by.get((case, rep, arm))
            if not a or not b or not usable(case, rep, opponent, arm, a, b):
                continue
            def val(record):
                if field == 'wall_seconds':
                    return record.get('wall_seconds')
                return record.get('usage', {}).get(field)
            av, bv = val(a), val(b)
            if not all(isinstance(v, (float, int)) and not isinstance(v, bool) and v > 0 for v in (av, bv)):
                continue
            logs[case].append(math.log(bv / av))
    seq = [x for xs in logs.values() for x in xs]
    ci = ci_bootstrap_by_task(logs) if len(logs) >= 2 else None
    return {'paired_trials':len(seq), 'distinct_tasks':len(logs),
            'pareto_to_baseline_ratio':round(math.exp(mean(seq)),4) if seq else None,
            'task_bootstrap_95_ci_ratio':[round(math.exp(x),4) for x in ci] if ci else None,
            'interpretation':'ratio < 1 means less consumed by Pareto; only both-usable paired runs'}


def text(value, digits=3):
    return 'N/A' if value is None else f'{value:.{digits}f}'


def bars(label, metrics, key):
    palette=['#22d3ee','#aab5c5','#ffd377']
    mx=max((metrics[a][key] for a in metrics if metrics[a][key] is not None), default=1) or 1
    lines=[f'<h3>{html.escape(label)}</h3>']
    for i,(arm,m) in enumerate(metrics.items()):
        v=m[key]
        w=(v/mx*100) if v is not None else 0
        lines.append(f'<div class="bar-label"><span>{html.escape(arm)}</span><strong>{text(v,2)}</strong></div><div class="track"><div class="fill" style="width:{w:.2f}%;background:{palette[i%3]}"></div></div>')
    return ''.join(lines)


def build(run):
    run=Path(run).resolve()
    meta=load_json(run/'meta.json')
    recs=[json.loads(line) for line in (run/'events.jsonl').read_text(encoding='utf8').splitlines() if line.strip()]
    by={(r['case_id'],r['repeat'],r['arm']):r for r in recs}
    judgments=load_json(run/'blind_grades.json') if (run/'blind_grades.json').exists() else {'n_valid':0,'n_expected':0,'judgments':[]}
    judged={(j['case_id'],j['repeat'],tuple(sorted((j['A'],j['B'])))):j for j in judgments['judgments']}
    all_arms=meta['arms']; comps=[a for a in all_arms if a!='pareto']
    metrics={}
    for arm in all_arms:
        rs=[r for r in recs if r['arm']==arm]
        code=[r for r in rs if r['kind']=='code']
        decision=[r for r in rs if r['kind']=='decision']
        tok=[r['usage'].get('total_tokens') for r in rs]
        cost=[r['usage'].get('cost_usd') for r in rs]
        metrics[arm]={
            'trials':len(rs), 'code_trials':len(code), 'decision_trials':len(decision),
            'code_pass_rate':mean([int(bool(r['grade'].get('pass'))) for r in code]),
            'mean_wall_seconds':mean([r['wall_seconds'] for r in rs]),
            'mean_total_tokens':mean(tok) if rs and all(isinstance(v,int) and not isinstance(v,bool) for v in tok) else None,
            'mean_cost_usd':mean(cost) if rs and all(isinstance(v,(int,float)) and not isinstance(v,bool) for v in cost) else None,
            'tokens_observed':sum(isinstance(v,int) for v in tok),
            'cost_observed':sum(isinstance(v,(int,float)) for v in cost),
        }

    comparisons={}
    for opponent in comps:
        quality_code=defaultdict(list)
        quality_decision=defaultdict(list)
        hard_veto=0
        for c in meta['case_ids']:
            for rep in range(1,meta['repeats']+1):
                a=by.get((c,rep,opponent));b=by.get((c,rep,'pareto'))
                if not a or not b:continue
                if CASE_BY_ID[c]['kind']=='code':
                    quality_code[c].append(int(bool(b['grade'].get('pass')))-int(bool(a['grade'].get('pass'))))
                else:
                    j=judged.get((c,rep,tuple(sorted(('pareto',opponent)))))
                    if not j:continue
                    ua='pareto' in j.get('usable_arms',[])
                    ub=opponent in j.get('usable_arms',[])
                    quality_decision[c].append(int(ua)-int(ub))
                    if 'pareto' in j['hard_violation_arms']:hard_veto+=1
        code_ci=ci_bootstrap_by_task(quality_code)
        dec_ci=ci_bootstrap_by_task(quality_decision)
        def usable(case,rep,op,p,a,b):
            if CASE_BY_ID[case]['kind']=='code':
                return bool(a['grade'].get('pass')) and bool(b['grade'].get('pass'))
            j=judged.get((case,rep,tuple(sorted((op,p)))))
            return bool(j and op in j.get('usable_arms',[]) and p in j.get('usable_arms',[]) and not j.get('hard_violation_arms'))
        speed=efficiency_ratio(by,meta['case_ids'],meta['repeats'],'pareto',opponent,'wall_seconds',usable)
        tokens=efficiency_ratio(by,meta['case_ids'],meta['repeats'],'pareto',opponent,'total_tokens',usable)
        costs=efficiency_ratio(by,meta['case_ids'],meta['repeats'],'pareto',opponent,'cost_usd',usable)
        comparisons[opponent]={
            'code_success_delta':mean([v for seq in quality_code.values() for v in seq]),
            'code_success_delta_95_ci':code_ci,
            'decision_usable_delta':mean([v for seq in quality_decision.values() for v in seq]),
            'decision_usable_delta_95_ci':dec_ci,
            'decision_judged_pairs':sum(map(len,quality_decision.values())),
            'pareto_decision_hard_vetoes':hard_veto,
            'time':speed,'tokens':tokens,'cost_usd':costs,
        }

    total_expected=meta['expected_runs']
    full=(len(recs)==total_expected and len(by)==total_expected and all(r['exit_code']==0 for r in recs))
    judge_expected=sum(CASE_BY_ID[c]['kind']=='decision' for c in meta['case_ids'])*meta['repeats']*len(comps)
    complete_judging=(judge_expected>0 and judgments.get('n_valid')==judge_expected and len(judgments['judgments'])==judge_expected)
    pareto_hard_flags=sum(bool(r['grade'].get('hard_requirement_violation')) for r in recs if r['arm']=='pareto')
    preset=meta['cases']==30 and len(meta['case_ids'])==30 and meta['repeats']>=3
    strict=(preset and full and complete_judging and meta['adapter']!='mock' and not pareto_hard_flags)
    quality_ok=True;efficiency_ok=True
    for op,c in comparisons.items():
        code_low=(c['code_success_delta_95_ci'] or [None])[0]
        dec_low=(c['decision_usable_delta_95_ci'] or [None])[0]
        quality_ok &= (code_low is not None and code_low>=-0.05 and dec_low is not None and dec_low>=-0.05 and not c['pareto_decision_hard_vetoes'])
        t_ci=c['time']['task_bootstrap_95_ci_ratio']
        tok_ci=c['tokens']['task_bootstrap_95_ci_ratio']
        wins=(bool(t_ci and t_ci[1]<0.90) or bool(tok_ci and tok_ci[1]<0.90))
        # Do not count success if the other available resource metric regresses >10%.
        not_harming=(not t_ci or t_ci[1]<=1.10) and (not tok_ci or tok_ci[1]<=1.10)
        efficiency_ok &= wins and not_harming
    verdict=('EFFICIENCY_SUPPORTED_WITHIN_SUITE' if strict and quality_ok and efficiency_ok else
             'NOT_DEMONSTRATED' if strict else 'INSUFFICIENT_EVIDENCE')
    if meta['adapter']=='mock':verdict='SMOKE_TEST_ONLY'
    report={'verdict':verdict,'run':str(run),'meta':meta,'trial_count':len(recs),'expected_count':total_expected,
            'quality_gate_passed':bool(quality_ok and strict),'efficiency_gate_passed':bool(efficiency_ok and strict),
            'blind_judgments_complete':complete_judging,'expected_blind_judgments':judge_expected,
            'pareto_hard_flags':pareto_hard_flags,'metrics':metrics,'comparisons':comparisons,
            'caveats':['Speed is end-to-end wall-clock, NOT time-to-first-usable artifact.',
                       'Efficiency ratios condition on both arms producing usable results; selection bias is possible.',
                       'Task-level bootstrap, not independent counting of repeated seeds; 30 tasks are not representative of all agent work.',
                       'No model judge substitutes for an independent human audit; numeric gate is not publication approval.',
                       'Missing usage/cost telemetry is N/A, never zero.',
                       'These 20 tiny code tasks and 10 decisions do not establish 80% utility or 20% effort for full applications.']}
    atomic_json(run/'summary.json',report)
    h='<h1>Efficiency-first A/B/C benchmark</h1><p>Verified outcomes first · End-to-end time · Tokens · No simulated results</p>'
    h+=f'<div class="panel"><h2>{html.escape(verdict)}</h2><p>{len(recs)} / {total_expected} runs · Blind reviews {judgments.get("n_valid",0)} / {judge_expected} · Model {html.escape(str(meta["model"]))}</p></div>'
    h+='<section class="panel">'+bars('Functional code success rate',metrics,'code_pass_rate')+'</section>'
    h+='<section class="panel">'+bars('Mean elapsed seconds (all trials)',metrics,'mean_wall_seconds')+'</section>'
    h+='<section class="panel">'+bars('Mean total tokens (all trials; N/A if incomplete)',metrics,'mean_total_tokens')+'</section>'
    h+='<h2>Quality-gated efficiency</h2><table><thead><tr><th>Comparator</th><th>Code quality Δ / 95% CI</th><th>Decision usable Δ / 95% CI</th><th>Time ratio / 95% CI</th><th>Token ratio / 95% CI</th></tr></thead><tbody>'
    for op,c in comparisons.items():
        def ratio(x):return text(x['pareto_to_baseline_ratio'])+' '+html.escape(str(x['task_bootstrap_95_ci_ratio']))+f' (n={x["paired_trials"]})'
        h+='<tr><td>'+html.escape(op)+'</td><td>'+text(c['code_success_delta'])+' '+html.escape(str(c['code_success_delta_95_ci']))+'</td><td>'+text(c['decision_usable_delta'])+' '+html.escape(str(c['decision_usable_delta_95_ci']))+'</td><td>'+ratio(c['time'])+'</td><td>'+ratio(c['tokens'])+'</td></tr>'
    h+='</tbody></table><h2>Interpretation safeguards</h2><ul>'+''.join('<li>'+html.escape(x)+'</li>' for x in report['caveats'])+'</ul>'
    h+='<p>Inspect the raw run files and <code>benchmark/PROTOCOL.md</code>. Automated positive labels must pass independent review before publication.</p>'
    page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pareto Forge | Efficiency Benchmark</title><style>
:root{color-scheme:dark}body{margin:0;background:#10171c;color:#f4f8fa;font:15px/1.6 system-ui,sans-serif}main{margin:auto;max-width:1040px;padding:40px 25px}h1{font-size:31px}h2{font-size:21px}h3{font-size:16px}p,li{color:#bac7ce}.panel{padding:22px;margin:20px 0;background:#19252b;border-radius:15px;border:1px solid #31454d}.panel h2{color:#4fe0e8}table{width:100%;border-collapse:collapse;font-size:13px}th,td{padding:12px;border-bottom:1px solid #31454d;text-align:left;vertical-align:top}.track{background:#33434a;border-radius:7px;height:15px;overflow:hidden}.fill{height:100%;border-radius:7px}.bar-label{display:flex;justify-content:space-between;margin:14px 0 4px}code{color:#7fe4ed}</style></head><body><main>'''+h+'</main></body></html>'
    (run/'report.html').write_text(page,encoding='utf8')
    with (run/'metrics.csv').open('w',encoding='utf8',newline='') as f:
        w=csv.writer(f);w.writerow(['case','repeat','arm','kind','exit_code','functional_pass','seconds','tokens','cost_usd'])
        for r in recs:w.writerow([r['case_id'],r['repeat'],r['arm'],r['kind'],r['exit_code'],r['grade'].get('pass'),r['wall_seconds'],r['usage'].get('total_tokens'),r['usage'].get('cost_usd')])
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True,type=Path);a=p.parse_args()
    result=build(a.run)
    print(json.dumps({'verdict':result['verdict'],'trials':result['trial_count'],'expected':result['expected_count'],'report':str(a.run/'report.html')},indent=2))

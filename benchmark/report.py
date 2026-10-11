#!/usr/bin/env python3
"""Honest offline HTML report; never invents absent telemetry or evaluations."""
import argparse
import csv
import html
import json
from collections import defaultdict
from pathlib import Path
from core import ROOT, CASE_BY_ID, atomic_json, ci_bootstrap_by_task, load_json, mean, wilson_lower


def svg_bars(title, rows, vmax=1, percent=True):
    width=720; line=52
    parts=[f'<svg viewBox="0 0 {width} {80+line*len(rows)}" role="img" aria-label="{html.escape(title,quote=True)}" xmlns="http://www.w3.org/2000/svg">',f'<text x="16" y="26" font-size="18" fill="#f4f6f8">{html.escape(title)}</text>']
    for i,(label,val,color) in enumerate(rows):
        y=50+i*line
        parts.append(f'<text x="16" y="{y+15}" font-size="13" fill="#bcc5cd">{html.escape(label)}</text>')
        parts.append(f'<rect x="156" y="{y}" width="440" height="22" rx="5" fill="#27343d"/>')
        if val is not None:
            bar=max(0,min(440,440*val/max(vmax,0.001)))
            parts.append(f'<rect x="156" y="{y}" width="{bar:.1f}" height="22" rx="5" fill="{color}"/>')
            labelval=f'{val*100:.1f}%' if percent else f'{val:,.1f}'
        else: labelval='not available'
        parts.append(f'<text x="610" y="{y+16}" font-size="13" fill="#f4f6f8">{labelval}</text>')
    return ''.join(parts)+'</svg>'


def build(run):
    run=Path(run).resolve();meta=load_json(run/'meta.json')
    recs=[json.loads(line) for line in (run/'events.jsonl').read_text().splitlines() if line.strip()]
    by={(r['case_id'],r['repeat'],r['arm']):r for r in recs}
    total_expected=meta['expected_runs']
    processed=len(recs)
    code=[r for r in recs if r['kind']=='code']
    groups={a:[r for r in code if r['arm']==a] for a in meta['arms']}
    metrics={}
    for arm,arr in groups.items():
        toks=[r['usage']['total_tokens'] for r in arr if isinstance(r['usage']['total_tokens'],int)]
        costs=[r['usage']['cost_usd'] for r in arr if isinstance(r['usage']['cost_usd'],(int,float))]
        metrics[arm]={'code_trials':len(arr),'code_pass_rate':mean([1 if r['grade'].get('pass') else 0 for r in arr]),
                      'mean_code_wall_seconds':mean([r['wall_seconds'] for r in arr]),
                      'mean_code_tokens':mean(toks) if len(toks)==len(arr) and arr else None,
                      'mean_code_cost_usd':mean(costs) if len(costs)==len(arr) and arr else None,
                      'code_trials_with_token_usage':len(toks),'code_trials_with_cost':len(costs)}
    contrasts={}
    for opposite in ('vanilla','ponytail'):
        if opposite not in meta['arms']:continue
        deltas=defaultdict(list)
        for case_id in meta['case_ids']:
            if CASE_BY_ID[case_id]['kind']!='code':continue
            for rep in range(1,meta['repeats']+1):
                a=by.get((case_id,rep,opposite));b=by.get((case_id,rep,'pareto'))
                if not a or not b:continue
                deltas[case_id].append((1 if b['grade'].get('pass') else 0)-(1 if a['grade'].get('pass') else 0))
        pairs=sum(map(len,deltas.values()))
        contrasts[opposite]={'paired_code_trials':pairs,'mean_code_success_delta':mean([v for seq in deltas.values() for v in seq]),
                             'bootstrap_95_ci':ci_bootstrap_by_task(deltas)}
    blind_path=run/'blind_grades.json'
    judgments=load_json(blind_path) if blind_path.exists() else {'n_valid':0,'n_expected':0,'judgments':[]}
    decision_summary={}
    for opposite in ('vanilla','ponytail'):
        if opposite not in meta['arms']:continue
        matches=[j for j in judgments['judgments'] if CASE_BY_ID[j['case_id']]['kind']=='decision' and opposite in (j['A'],j['B'])]
        wins=sum(j['winner_arm']=='pareto' for j in matches)
        ties=sum(j['winner_arm']=='tie' for j in matches)
        violates=sum('pareto' in j['hard_violation_arms'] for j in matches)
        blind_task_deltas=defaultdict(list)
        for j in matches:
            blind_task_deltas[j['case_id']].append(1 if j['winner_arm']=='pareto' else 0)
        decision_ci=ci_bootstrap_by_task(blind_task_deltas)
        decision_summary[opposite]={'judged_pairs':len(matches),'wins':wins,'ties':ties,'hard_requirement_flags':violates,
                                    'pareto_win_rate':wins/len(matches) if matches else None,
                                    'wilson_95_lower':wilson_lower(wins,len(matches)), 'task_bootstrap_95_ci':decision_ci}
    failures=[r for r in recs if r['exit_code']!=0]
    complete=(processed==total_expected and not failures)
    hard_violations=[r for r in recs if r['grade'].get('hard_requirement_violation')]
    judge_count_expected=sum(CASE_BY_ID[c]['kind']=='decision' for c in meta['case_ids'])*meta['repeats']*(len(meta['arms'])-1)
    judge_complete=(judgments.get('n_valid')==judge_count_expected and judge_count_expected>0)
    controls=('d08-simple','d09-simple-fact')
    control_flags=sum('pareto' in j['hard_violation_arms'] for j in judgments['judgments'] if j['case_id'] in controls)
    required_suite=meta['cases']==30 and len(meta['case_ids'])==30
    strict=(complete and required_suite and meta['repeats']>=3 and judge_complete and meta['adapter']!='mock' and not hard_violations and not control_flags)
    supported=strict
    for opposite,contrast in contrasts.items():
        lower=(contrast['bootstrap_95_ci'] or [None])[0]
        quality=decision_summary.get(opposite,{})
        supported = supported and (lower is not None and lower>0 and quality.get('wilson_95_lower') is not None and quality['wilson_95_lower']>.5 and (quality.get('task_bootstrap_95_ci') or [0])[0]>.5 and quality['hard_requirement_flags']==0)
    verdict=('SUPPORTED_WITHIN_SUITE' if supported else 'INSUFFICIENT_EVIDENCE' if not strict else 'NOT_DEMONSTRATED')
    if meta['adapter']=='mock': verdict='SMOKE_TEST_ONLY'
    notes=['A supported result applies only to this preregistered benchmark/model/agent and is not proof of universal or causal generalization.',
           'Deterministic code tests assess functional outputs, not full security or maintainability; LLM judges are fallible.',
           'Costs/tokens are missing unless the chosen CLI reports them; do not infer zero usage from null.']
    report={'verdict':verdict,'run':str(run),'meta':meta,'trial_count':processed,'expected_count':total_expected,'exit_failures':len(failures),
            'code_metrics':metrics,'code_comparisons':contrasts,'decision_judgments':decision_summary,
            'blind_judgments_complete':judge_complete,'expected_blind_judgments':judge_count_expected,
            'hard_requirement_flags':len(hard_violations),'control_flags':control_flags,'caveats':notes}
    atomic_json(run/'summary.json',report)
    colors=['#14d8e5','#91a4ae','#f1c46b']
    barrows=[(a,metrics[a]['code_pass_rate'],colors[i]) for i,a in enumerate(meta['arms'])]
    tokenrows=[(a,metrics[a]['mean_code_tokens'],colors[i]) for i,a in enumerate(meta['arms'])]
    max_tokens=max([r[1] for r in tokenrows if r[1] is not None] or [1])
    comparison=''.join(f'<tr><td>{html.escape(name)}</td><td>{c["paired_code_trials"]}</td><td>{c["mean_code_success_delta"] if c["mean_code_success_delta"] is not None else "N/A"}</td><td>{html.escape(str(c["bootstrap_95_ci"]))}</td><td>{decision_summary[name]["pareto_win_rate"] if decision_summary[name]["pareto_win_rate"] is not None else "Pending"}</td></tr>' for name,c in contrasts.items())
    def fmt(value, pattern):
        return format(value, pattern) if value is not None else 'N/A'
    table=''.join(
        '<tr><td>'+html.escape(a)+'</td><td>'+str(m['code_trials'])+'</td><td>'+
        fmt(m['code_pass_rate'],'.3f')+'</td><td>'+fmt(m['mean_code_wall_seconds'],'.2f')+
        '</td><td>'+fmt(m['mean_code_tokens'],'.0f')+'</td><td>'+
        ('$'+fmt(m['mean_code_cost_usd'],'.4f') if m['mean_code_cost_usd'] is not None else 'N/A')+'</td></tr>'
        for a,m in metrics.items()
    )
    # Text, numbers and plots come exclusively from actual event/grading files.
    page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Pareto Forge | Benchmark Report</title><style>
:root{{color-scheme:dark}}body{{margin:0;background:#0f171c;color:#edf1f4;font:15px/1.6 system-ui, sans-serif}}main{{margin:auto;max-width:940px;padding:36px 24px 60px}}h1{{font-size:30px;margin:5px 0}}h2{{margin-top:40px}}p,li{{color:#c0cbd0}}header{{border-bottom:1px solid #31424b;padding-bottom:22px}}code{{color:#70e4ee}}.tag{{color:#19dbe6;letter-spacing:2px;font-size:11px;font-weight:700}}.panel{{margin-top:20px;padding:22px;background:#17232a;border:1px solid #2a3b44;border-radius:16px}}.warning{{border-left:4px solid #f1c46b;padding:14px 18px;background:#2a281d}}table{{border-collapse:collapse;width:100%;font-size:13px}}td,th{{text-align:left;border-bottom:1px solid #2d3e47;padding:12px 9px}}th{{color:#89a5b3}}a{{color:#1bdae8}}.foot{{font-size:12px;color:#7e9aa8;margin-top:36px}}svg{{width:100%;height:auto}}
</style></head><body><main><header><div class="tag">PARETO FORGE / EVIDENCE LAB</div><h1>Reproducible benchmark</h1><p>Agent: <code>{html.escape(str(meta['adapter']))}</code> · Model: <code>{html.escape(str(meta['model']))}</code> · Activator: {html.escape(str(meta['activation']))}</p><p>Case runs: <strong>{processed}/{total_expected}</strong>. Repetitions: <strong>{meta['repeats']}</strong>. Blind judgments: <strong>{judgments.get('n_valid',0)}/{judge_count_expected}</strong>.</p></header>
<section class="panel"><h2>Evidence verdict</h2><h1>{html.escape(verdict)}</h1><p>This label is computed from preregistered rules; it does not mean the skill is universally better.</p></section>
<div class="panel">{svg_bars('Independent coding test pass rate',barrows)}</div>
<div class="panel">{svg_bars('Reported mean total tokens per coding run',tokenrows,max_tokens,False)}</div>
<h2>Raw descriptive metrics</h2><table><thead><tr><th>Arm</th><th>Code trials</th><th>Pass rate</th><th>Mean seconds</th><th>Mean tokens</th><th>Mean cost USD</th></tr></thead><tbody>{table}</tbody></table>
<h2>Paired comparisons vs Pareto</h2><table><thead><tr><th>Opponent</th><th>Paired code trials</th><th>Code pass delta</th><th>95% task-bootstrap CI</th><th>Blind win fraction</th></tr></thead><tbody>{comparison}</tbody></table>
<div class="warning"><strong>Interpret with care.</strong><p>Decision tasks require blind human or independent-model review; text length and keywords are not an accuracy metric. CI resamples tasks, not tokens. Missing telemetry is never a zero.</p></div>
<h2>Integrity</h2><p>Failed agent commands: {len(failures)} · Oracle hard-requirement flags: {len(hard_violations)} · Control task hard flags: {control_flags} · Complete blinded reviews: {judge_complete}.</p>
<h2>Method</h2><p>Every task begins from a new workspace with the same fixture and base user request. Treatment adds the selected skill, and forced-mode explicitly instructs its use. The experiment therefore measures skill-assisted prompting, not passive discovery. Avoid benchmarking within privileged or sensitive host environments.</p>
<p class="foot">Audit sources: meta.json · events.jsonl · individual trace.jsonl · grading.json · blind_grades.json · summary.json. This report never contains synthetic improvement claims.</p></main></body></html>'''
    (run/'report.html').write_text(page,encoding='utf8')
    with (run/'metrics.csv').open('w',encoding='utf8',newline='') as f:
        writer=csv.writer(f);writer.writerow(['case','repeat','arm','kind','exit_code','pass','wall_seconds','tokens','cost_usd'])
        for r in recs:writer.writerow([r['case_id'],r['repeat'],r['arm'],r['kind'],r['exit_code'],r['grade'].get('pass'),r['wall_seconds'],r['usage'].get('total_tokens'),r['usage'].get('cost_usd')])
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);args=p.parse_args()
    result=build(args.run)
    print(json.dumps({'verdict':result['verdict'],'trials':result['trial_count'],'expected':result['expected_count'],'report':str(args.run/'report.html')},indent=2))

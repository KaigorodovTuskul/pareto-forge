#!/usr/bin/env python3
"""Run isolated real agent trials; no performance numbers are simulated."""
import argparse
import json
import os
import platform
import random
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from core import ROOT, PROJECT, CASES, atomic_json, file_hash, load_json, parse_codex_usage, parse_claude_usage, parse_agy_usage


def prepare_workspace(path, case, arm, ponytail_path=None):
    path.mkdir(parents=True, exist_ok=False)
    if case['kind'] == 'code':
        (path/'solution.py').write_text('''"""Complete this module as requested; stdlib only."""\n\ndef solve(payload):\n    raise NotImplementedError("Implement the requested behavior")\n''')
    else:
        (path/'TASK.md').write_text('Complete the request in DECISION.md. Do not change TASK.md.\n')
    if arm == 'pareto':
        for prefix in ('.agents', '.claude'):
            dest=path/prefix/'skills'/'pareto-forge'
            shutil.copytree(PROJECT/'skills'/'pareto-forge',dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    elif arm == 'ponytail':
        if ponytail_path is None:
            raise ValueError('Ponytail requires --ponytail-skill')
        src=Path(ponytail_path).resolve()
        if not (src/'SKILL.md').is_file():
            raise ValueError('Ponytail path must contain SKILL.md')
        for prefix in ('.agents','.claude'):
            dest=path/prefix/'skills'/'ponytail'
            shutil.copytree(src,dest,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))


def make_prompt(case, arm, activation):
    base = case['prompt']
    prefix = 'Work only within the current workspace. Use the standard library if possible. Do not access any external network or modify files outside this workspace.\n\n'
    # Natural-mode host discovery vs forced-mode skill adherence are distinct estimands.
    if activation == 'forced' and arm == 'pareto':
        prefix += 'For this task, read .agents/skills/pareto-forge/SKILL.md and apply it when appropriate. Follow its referenced files only when useful.\n\n'
    elif activation == 'forced' and arm == 'ponytail':
        prefix += 'For this task, read .agents/skills/ponytail/SKILL.md and apply it when appropriate.\n\n'
    return prefix+base


def invoke(adapter, model, workspace, prompt, timeout, max_turns, reasoning_effort='high'):
    if adapter=='mock':
        # Deliberately incapable of producing a valid solution. Never call this an efficacy run.
        return {'returncode':0, 'stdout':json.dumps({'type':'mock','result':'NOT A MODEL OUTPUT'})+'\n',
                'stderr':'MOCK ADAPTER: transport smoke test only', 'last_message':'NOT A MODEL OUTPUT'}
    exe=shutil.which(adapter)
    if not exe and adapter!='mock':
        raise RuntimeError(f'Agent executable not found: {adapter}')
    if adapter=='codex':
        sandbox_mode='danger-full-access' if sys.platform=='win32' else 'workspace-write'
        command=[exe,'exec','--json','--sandbox',sandbox_mode,'--ignore-user-config','--skip-git-repo-check','--ephemeral','--model',model,'-c',f'model_reasoning_effort="{reasoning_effort}"','--output-last-message',str(workspace.parent/'last_message.txt'),'-']
        inp=prompt
    elif adapter=='claude':
        command=[exe,'-p','--output-format','json','--model',model,'--max-turns',str(max_turns),'--permission-mode','acceptEdits',prompt]
        inp=None
    elif adapter=='agy':
        command=[exe,'-p',prompt,'--model',model,'--effort',reasoning_effort,'--dangerously-skip-permissions','--output-format','json']
        inp=None
    else:
        raise ValueError(adapter)
    try:
        p=subprocess.run(command,input=inp,text=True,cwd=workspace,capture_output=True,timeout=timeout,check=False)
        if adapter=='claude':
            try:
                last=json.loads(p.stdout).get('result','')
            except (ValueError,AttributeError):
                last=''
        elif adapter=='agy':
            try:
                last=json.loads(p.stdout).get('response','')
            except (ValueError,AttributeError):
                last=''
        else:
            last=(workspace.parent/'last_message.txt').read_text(errors='replace') if (workspace.parent/'last_message.txt').exists() else ''
        return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'last_message':last}
    except subprocess.TimeoutExpired as e:
        return {'returncode':124,'stdout':e.stdout.decode('utf8','replace') if isinstance(e.stdout,bytes) else (e.stdout or ''),
                'stderr':e.stderr.decode('utf8','replace') if isinstance(e.stderr,bytes) else (e.stderr or '')+'\nTIMEOUT', 'last_message':''}


def grade(run_dir, case):
    if case['kind']!='code':
        artifact=run_dir/'workspace'/'DECISION.md'
        present=artifact.is_file() and bool(artifact.read_text(encoding='utf8',errors='replace').strip())
        return {'kind':'decision','artifact_present':present, 'quality_status':'PENDING_BLIND_JUDGMENT', 'objective_rate':None, 'pass':None}
    command=[sys.executable,'-I',str(ROOT/'graders'/'grade_code.py'),case['id'],str(run_dir/'workspace')]
    clean_env={k:os.environ[k] for k in ('PATH','LANG','LC_ALL','SYSTEMROOT','WINDIR') if k in os.environ}
    try:
        p=subprocess.run(command,cwd=run_dir,capture_output=True,text=True,timeout=12,env=clean_env,check=False)
        if p.returncode:
            return {'kind':'code','objective_rate':0.0,'pass':False,'grader_error':p.stderr[-500:]}
        d=json.loads(p.stdout)
        rate=d['passed']/d['total'] if d['total'] else 0
        d.update({'objective_rate':rate,'pass':rate==1.0})
        if case['id']=='c20-webhook' and not d.get('timing_safe_source_check'):
            d['pass']=False
            d['hard_requirement_violation']='No constant-time compare_digest source evidence'
        return d
    except (subprocess.TimeoutExpired,ValueError,KeyError) as e:
        return {'kind':'code','objective_rate':0.0,'pass':False,'grader_error':str(e)[:300]}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--adapter',choices=['codex','claude','agy','mock'],default='codex')
    ap.add_argument('--model',help='Pin a concrete model ID for real agent runs')
    ap.add_argument('--reasoning-effort',choices=['low','medium','high','xhigh','max'],default='high')
    ap.add_argument('--repeats',type=int,default=3)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--ponytail-skill',type=Path,help='Locally reviewed, pinned Ponytail skill dir containing SKILL.md')
    ap.add_argument('--activation',choices=['forced','natural'],default='forced')
    ap.add_argument('--max-seconds',type=int,default=240)
    ap.add_argument('--max-turns',type=int,default=12)
    ap.add_argument('--seed',type=int,default=1729)
    ap.add_argument('--case',action='append',dest='only_cases',help='Optional task ID(s) for debugging')
    ap.add_argument('--max-runs',type=int,default=0,help='Limit for harness smoke testing; incomplete runs not publishable')
    args=ap.parse_args()
    if args.repeats<1 or args.max_seconds<1: ap.error('repeats and max-seconds must be positive')
    if args.adapter!='mock' and not args.model: ap.error('--model is required for real trials')
    if args.out.resolve()==PROJECT or PROJECT in args.out.resolve().parents:
        ap.error('Store run outputs outside the source repository (e.g. ../pareto-bench-runs/first)')
    if args.out.exists() and any(args.out.iterdir()): ap.error('--out must be a new or empty directory')
    if args.only_cases:
        unknown=set(args.only_cases)-{c['id'] for c in CASES}
        if unknown: ap.error('Unknown case IDs: '+','.join(sorted(unknown)))
    cases=[c for c in CASES if not args.only_cases or c['id'] in args.only_cases]
    arms=['vanilla','pareto']+(['ponytail'] if args.ponytail_skill else [])
    out=args.out.resolve();out.mkdir(parents=True,exist_ok=True)
    plan=[(case,repeat,arm) for case in cases for repeat in range(1,args.repeats+1) for arm in arms]
    random.Random(args.seed).shuffle(plan)
    if args.max_runs: plan=plan[:args.max_runs]
    try:
        exe=shutil.which(args.adapter) or args.adapter
        v=subprocess.run([exe,'--version'],capture_output=True,text=True,timeout=8,check=False) if args.adapter!='mock' else None
        cli_version=(v.stdout or v.stderr).strip()[:200] if v else 'mock (not real)'
    except Exception as exc:
        cli_version='unavailable: '+str(exc)[:100]
    meta={'runtime':{'python':platform.python_version(),'os':platform.platform(),'cli_version':cli_version},
          'created_at':datetime.now(timezone.utc).isoformat(),'suite_sha256':file_hash(ROOT/'tasks.json'),
          'pareto_skill_sha256':file_hash(PROJECT/'skills'/'pareto-forge'/'SKILL.md'),
          'pony_tail_skill_sha256':file_hash(args.ponytail_skill/'SKILL.md') if args.ponytail_skill else None,
          'adapter':args.adapter,'model':args.model,'reasoning_effort':args.reasoning_effort,'activation':args.activation,'repeats':args.repeats,
          'seed':args.seed,'cases':len(cases),'expected_runs':len(cases)*args.repeats*len(arms),
          'planned_runs':len(plan),'arms':arms,'case_ids':[c['id'] for c in cases],
          'max_seconds':args.max_seconds,'max_turns':args.max_turns,
          'warning':'These are real measurements only if adapter is codex or claude and processes actually ran. Mock is transport smoke test.'}
    atomic_json(out/'meta.json',meta)
    with (out/'events.jsonl').open('w',encoding='utf8') as log:
        for n,(case,repeat,arm) in enumerate(plan,1):
            trial=out/'trials'/case['id']/f'{repeat:02d}'/arm
            workspace=trial/'workspace'
            prepare_workspace(workspace,case,arm,args.ponytail_skill)
            prompt=make_prompt(case,arm,args.activation)
            (trial/'prompt.txt').write_text(prompt,encoding='utf8')
            print(f'[{n}/{len(plan)}] {case["id"]} rep {repeat} arm {arm}',flush=True)
            t=time.monotonic()
            try:
                obj=invoke(args.adapter,args.model,workspace,prompt,args.max_seconds,args.max_turns,args.reasoning_effort)
            except Exception as e:
                obj={'returncode':125,'stdout':'','stderr':f'INVOKE ERROR: {type(e).__name__}: {e}','last_message':''}
            seconds=round(time.monotonic()-t,3)
            (trial/'stdout.txt').write_text(obj['stdout'],encoding='utf8')
            (trial/'stderr.txt').write_text(obj['stderr'],encoding='utf8')
            # Original structured events: Codex JSONL, Claude JSON converted to a one-record JSONL stream.
            raw=obj['stdout']
            lines=[line for line in raw.splitlines() if line.strip().startswith('{')]
            with (trial/'trace.jsonl').open('w',encoding='utf8') as traces:
                for line in lines:
                    try: json.loads(line)
                    except ValueError: continue
                    traces.write(line+'\n')
            (trial/'last_message.txt').write_text(obj['last_message'],encoding='utf8')
            usage=parse_codex_usage(obj['stdout']) if args.adapter=='codex' else parse_claude_usage(obj['stdout']) if args.adapter=='claude' else parse_agy_usage(obj['stdout']) if args.adapter=='agy' else {'input_tokens':None,'output_tokens':None,'total_tokens':None,'cost_usd':None}
            grade_result=grade(trial,case)
            atomic_json(trial/'grading.json',grade_result)
            atomic_json(trial/'timing.json',{'wall_seconds':seconds,'usage':usage,'exit_code':obj['returncode']})
            rec={'case_id':case['id'],'kind':case['kind'],'arm':arm,'repeat':repeat,'trial_path':str(trial.relative_to(out)),
                  'exit_code':obj['returncode'],'wall_seconds':seconds,'usage':usage,'grade':grade_result,
                  'adapter':args.adapter,'mock':args.adapter=='mock'}
            log.write(json.dumps(rec,ensure_ascii=False)+'\n');log.flush()
    print('Finished raw trials. Generate report with: python benchmark/report.py --run '+str(out))

if __name__=='__main__': main()

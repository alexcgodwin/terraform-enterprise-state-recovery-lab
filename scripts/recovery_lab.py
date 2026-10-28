"""Disposable local-state exercises. No AWS, no remote state, no credentials.

Usage: python scripts/recovery_lab.py move | detach | drift
The tool copies only a known allowlisted lab into a new temporary directory.
"""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cwd: Path, *args: str, expected: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(['terraform', *args], cwd=cwd, capture_output=True, text=True)
    if proc.returncode not in expected:
        raise RuntimeError(f"terraform {' '.join(args)} failed (exit {proc.returncode}): {proc.stderr[-1200:]}")
    return proc


def ensure_initialized(path: Path) -> None:
    run(path, 'init', '-backend=false', '-input=false', '-no-color')


def exercise_move(path: Path) -> dict:
    before = ROOT/'labs/state-move/before/main.tf'
    after = ROOT/'labs/state-move/after/main.tf'
    shutil.copy2(before, path/'main.tf')
    ensure_initialized(path)
    run(path,'apply','-auto-approve','-input=false','-no-color')
    # Save a recovery snapshot inside disposable lab. Never publish raw state.
    backup = run(path,'state','pull').stdout
    (path/'pre-change.tfstate').write_text(backup,encoding='utf-8')
    shutil.copy2(after,path/'main.tf')
    run(path,'state','mv','terraform_data.legacy','terraform_data.service')
    post = run(path,'state','list').stdout.strip().splitlines()
    plan = run(path,'plan','-detailed-exitcode','-input=false','-no-color',expected=(0,2))
    if plan.returncode != 0 or post != ['terraform_data.service']:
        raise RuntimeError('Address migration produced unexpected plan or state')
    return {'scenario':'move','verified':True,'resource_addresses':post,'plan_exit_code':plan.returncode}


def exercise_detach(path: Path) -> dict:
    shutil.copy2(ROOT/'labs/state-move/after/main.tf',path/'main.tf')
    ensure_initialized(path)
    run(path,'apply','-auto-approve','-input=false','-no-color')
    initial=run(path,'state','list').stdout.strip()
    preview=run(path,'state','rm','-dry-run','terraform_data.service').stdout
    if 'terraform_data.service' not in preview:
        raise RuntimeError('Dry-run cannot find resource')
    run(path,'state','rm','terraform_data.service')
    final=run(path,'state','list').stdout.strip()
    # Resource removal from state does not destroy any underlying object.
    if initial!='terraform_data.service' or final:
        raise RuntimeError('Detach did not remove only requested address')
    return {'scenario':'detach','verified':True,'state_addresses_after':[],'underlying_object_deleted':False}


def exercise_drift(path: Path) -> dict:
    shutil.copy2(ROOT/'labs/drift/main.tf',path/'main.tf')
    ensure_initialized(path)
    run(path,'apply','-auto-approve','-input=false','-no-color')
    plan=run(path,'plan','-detailed-exitcode','-var=release=v2','-input=false','-no-color',expected=(0,2))
    if plan.returncode != 2:
        raise RuntimeError('Expected changed-input plan exit code 2')
    return {'scenario':'drift','verified':True,'plan_exit_code':2,'note':'Configuration drift demonstration; external infrastructure drift needs provider refresh'}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('scenario',choices=['move','detach','drift'])
    args=parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='terraform-state-sandbox-') as tmp:
        dest=Path(tmp)
        result={'move':exercise_move,'detach':exercise_detach,'drift':exercise_drift}[args.scenario](dest)
        print(json.dumps(result,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())

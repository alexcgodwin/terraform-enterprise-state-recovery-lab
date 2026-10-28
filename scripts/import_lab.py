"""Exercise Terraform import using an existing synthetic ID in a disposable workspace.

The random provider is logical and makes no cloud API calls. This verifies
CLI binding behavior; it is not a substitute for matching an actual AWS object.
"""
from __future__ import annotations
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / 'labs/import/main.tf'
IDENTIFIER = 'p-9hUg'

def tf(directory: Path, *args: str, expected: tuple[int, ...] = (0,)) -> str:
    command = ['terraform', *args]
    process = subprocess.run(command, cwd=directory, text=True, capture_output=True)
    if process.returncode not in expected:
        raise RuntimeError(f"Terraform {' '.join(args)} failed: {process.stderr[-900:]}")
    return process.stdout

def main() -> int:
    with tempfile.TemporaryDirectory(prefix='terraform-import-sandbox-') as temporary:
        path = Path(temporary)
        shutil.copy2(SOURCE, path / 'main.tf')
        tf(path, 'init', '-backend=false', '-input=false', '-no-color')
        tf(path, 'import', '-no-color', 'random_id.existing', IDENTIFIER)
        addresses = tf(path, 'state', 'list').strip().splitlines()
        if addresses != ['random_id.existing']:
            raise RuntimeError(f'Unexpected imported addresses: {addresses}')
        output = tf(path, 'plan', '-detailed-exitcode', '-no-color', '-input=false')
        if 'No changes.' not in output:
            raise RuntimeError('Import did not yield a no-change plan')
        print(json.dumps({'scenario': 'import', 'verified': True,
                          'resource_address': addresses[0], 'plan_exit_code': 0,
                          'cloud_resources_created': False}))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

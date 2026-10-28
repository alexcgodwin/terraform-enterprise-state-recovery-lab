from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DENIED = ('terraform.tfvars', 'backend.hcl', '.env', 'terraform.tfstate')

def main():
    result = subprocess.run(['git', 'ls-files', '-z'], cwd=ROOT, capture_output=True, check=True)
    paths = [x.decode('utf-8') for x in result.stdout.split(b'\0') if x]
    invalid = [p for p in paths if p.split('/')[-1] in DENIED or '/.terraform/' in '/' + p or p.endswith(('.tfstate', '.tfstate.backup', '.pem', '.key', '.tfplan'))]
    if invalid:
        print('Forbidden tracked artifacts:', *invalid, sep='\n', file=sys.stderr)
        return 1
    print(f'Repository hygiene verified for {len(paths)} tracked files')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

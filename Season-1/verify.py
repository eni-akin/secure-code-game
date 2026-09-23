"""Run from the repository root: python3 Season-1/verify.py."""
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def run(args, cwd):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    print(result.stdout + result.stderr, end='', flush=True)
    if result.returncode:
        raise SystemExit(result.returncode)
    return result.stdout

for level in (1, 2, 3, 4, 5):
    folder = ROOT / f'Level-{level}'
    print(f'\n=== LEVEL {level} ===', flush=True)
    if level == 2:
        with tempfile.TemporaryDirectory() as tmp:
            for name in ('tests', 'hack', 'security_checks'):
                exe = str(Path(tmp) / name)
                run(['cc', '-Wall', '-Wextra', '-Werror', '-fsanitize=address,undefined', '-g', f'{name}.c', '-o', exe], folder)
                output = run([exe], folder)
                if name == 'hack':
                    assert 'CONGRATULATIONS LEVEL 2 PASSED!' in output
    else:
        # Reset only the disposable exercise database for repeatable verification.
        if level == 4:
            (folder / 'level-4.db').unlink(missing_ok=True)
        for name in ('tests.py', 'hack.py'):
            if level == 5 and name == 'hack.py':
                print('Level 5 hack.py is intentionally inactive; use CodeQL and security_checks.py.')
                continue
            run([sys.executable, name, '-v'], folder)
    print(f'PASS: LEVEL {level}', flush=True)
run([sys.executable, str(ROOT / 'security_checks.py')], ROOT)
print('\nALL FIVE LEVELS: functional and active exploit checks PASS')

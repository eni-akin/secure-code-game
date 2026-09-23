"""Additional security properties beyond the upstream happy-path checks."""
import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load(level):
    spec = importlib.util.spec_from_file_location(f'level{level}', ROOT / f'Level-{level}' / 'code.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

c = load(1)
assert 'Full payment' not in c.validorder(c.Order('bad', [c.Item('product', '', 10, -1)]))
assert 'Full payment' not in c.validorder(c.Order('bad', [c.Item('payment', '', float('nan'), 1)]))
print('PASS: Level 1 invalid quantities and nonfinite amounts rejected')

c = load(3)
user = c.TaxPayer('test', 'test')
assert user.get_prof_picture() is None
assert user.get_prof_picture('/etc/passwd') is None
assert user.get_tax_form_attachment(str(ROOT / 'Level-3-evil' / 'file')) is None
with tempfile.TemporaryDirectory() as tmp:
    outside = Path(tmp) / 'outside.txt'
    outside.write_text('must not be read')
    link = ROOT / 'Level-3' / 'assets' / 'security-test-link'
    try:
        link.symlink_to(outside)
        assert user.get_prof_picture('assets/security-test-link') is None
        assert user.get_tax_form_attachment(str(link)) is None
    finally:
        link.unlink(missing_ok=True)
print('PASS: Level 3 absolute, sibling-prefix, and symlink escapes blocked')

c = load(4)
ops = c.DB_CRUD_ops()
original = ops.get_stock_price('MSFT')
for payload in ["MSFT'; DROP TABLE stocks--", "' OR 1=1--", "MSFT'; UPDATE stocks SET price=1--"]:
    assert '[RESULT]' not in ops.get_stock_price(payload)
    ops.get_stock_info(payload)
    ops.update_stock_price(payload, 1.0)
    assert ops.get_stock_price('MSFT') == original
for method in (ops.exec_multi_query, ops.exec_user_script):
    for payload in ['DROP TABLE stocks', "UPDATE stocks SET price=1", "SELECT * FROM stocks WHERE symbol='MSFT' OR 1=1", "SELECT load_extension('bad')"]:
        try:
            method(payload)
        except ValueError:
            pass
        else:
            raise AssertionError('Arbitrary SQL accepted')
assert ops.get_stock_price('MSFT') == original
print('PASS: Level 4 every database entry point preserves data under attack')

c = load(5)
legacy = c.MD5_hasher()
a = legacy.password_hash('correct horse battery staple')
b = legacy.password_hash('correct horse battery staple')
assert a.startswith('$2b$') and a != b
assert legacy.password_verification('correct horse battery staple', a)
assert not legacy.password_verification('wrong', a)
assert c.PASSWORD_HASHER == 'SHA256_hasher'
assert c.Random_generator().generate_salt().startswith(b'$2b$')
print('PASS: Level 5 salted bcrypt and incorrect-password rejection')

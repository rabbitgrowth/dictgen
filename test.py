import sys

from dictgen import gen

# TODO add stress to pronunciation

tests = [
    ('cat', 'kat', {'KAT'}),
    ('car', 'kar', {'KAR'}),
    ('cart', 'kart', {'KART'}),

    ('strap', 'strap', {'STRAP'}),

    ('ha', 'ha', {'HA'}),
    ('haha', 'haha', {'HA/HA'}),
    ('hahaha', 'hahaha', {'HA/HA/HA'}),

    ('Gwen', 'gwɛn', {'TKPWU/WEPB'}),
]

failures = []

for word, pron, expected in tests:
    result = {'/'.join(map(str, outline)) for outline in gen(pron)}
    if result != expected:
        failures.append((result, expected))

for result, expected in failures:
    result   = ', '.join(result)   or '-'
    expected = ', '.join(expected) or '-'
    print(f'{word} /{pron}/ → {result} ≠ {expected}')

if failures:
    sys.exit(1)

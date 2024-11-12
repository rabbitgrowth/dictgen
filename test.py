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

for word, pron, expected in tests:
    result = {'/'.join(map(str, outline)) for outline in gen(pron)}
    if result != expected:
        result   = ', '.join(result)
        expected = ', '.join(expected)
        print(f'{word} /{pron}/ → {result} ≠ {expected}')

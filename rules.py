from chords import LEFT_CHORDS, MID_CHORDS, RIGHT_CHORDS
from sound import Sound, BREAK
from stroke import Stroke

NON_RIGHT_CHORDS = LEFT_CHORDS | MID_CHORDS

SCHWI = Sound({'ə', 'ɪ'}, stressed=False)

NON_RIGHT_OPTIONAL_RULES = [
    (
        [...], [Sound('ʃ'), Sound('r')], [...],
        [Stroke('SKHR')]
    ), (
        [..., Sound()], [SCHWI, BREAK], [...],
        []
    ),
]

NON_RIGHT_RULES = [
    (
        [...], [Sound('', spelled='h')], [...],
        [Stroke('H')]
    ), (
        [...], [Sound({'w', 'h'}, spelled='wh')], [...],
        [Stroke('WH')]
    ), (
        [...], [Sound('ɪj')], [],
        [Stroke('AE')]
    ), (
        [...], [Sound('ɑj', spelled='igh'), Sound('t')], [...],
        [Stroke('OEUGT')]
    ), (
        [..., BREAK], [SCHWI], [Sound({'d', 'g', 'z'}), BREAK, ...],
        [Stroke('U')]
    ),
]

RIGHT_RULES = [
    (
        [...], [Sound('m'), Sound('p')], [...],
        [Stroke('-FPL')]
    ), (
        [...], [Sound('m', spelled='mb')], [...],
        [Stroke('-PL'), Stroke('-B')]
    ), (
        [...], [Sound('s'), Sound('t')], [...],
        [Stroke('*S')]
    ),
]

for chords, rules in [
    (NON_RIGHT_CHORDS, NON_RIGHT_RULES),
    (RIGHT_CHORDS, RIGHT_RULES)
]:
    for ipa, chord in chords.items():
        rules.append((
            [...], [Sound(ipa)], [...],
            [chord]
        ))

RULES = [
    [NON_RIGHT_OPTIONAL_RULES, NON_RIGHT_RULES],
    [RIGHT_RULES]
]

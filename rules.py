from sound import Sound
from stroke import Stroke

SCHWI = Sound({'ə', 'ɪ'}, stressed=False)

NON_RIGHT_OPTIONAL_RULES = [
    (
        [...], [Sound('ʃ'), Sound('r')], [...],
        [Stroke('SKHR')]
    ), (
        [..., Sound()], [SCHWI, Sound('.')], [...],
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
        [..., Sound('.')], [SCHWI], [Sound({'d', 'g', 'z'}), Sound('.'), ...],
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

RULES = [
    [NON_RIGHT_OPTIONAL_RULES, NON_RIGHT_RULES],
    [RIGHT_RULES]
]

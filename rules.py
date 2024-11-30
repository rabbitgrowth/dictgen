from chords import LEFT_CHORDS, MID_CHORDS, RIGHT_CHORDS
from sound import Sound, BREAK
from stroke import Stroke

class Rule:
    def __init__(
        self,
        pattern,
        chords,
        lookahead           = None,
        lookbehind          = None,
        negative_lookahead  = None,
        negative_lookbehind = None,
        stroke              = None,
        outline             = None,
    ):
        self.pattern             = pattern
        self.chords              = chords
        self.lookahead           = lookahead
        self.lookbehind          = lookbehind
        self.negative_lookahead  = negative_lookahead
        self.negative_lookbehind = negative_lookbehind
        self.stroke              = stroke
        self.outline             = outline

NON_RIGHT_CHORDS = LEFT_CHORDS | MID_CHORDS

SCHWI = Sound({'ə', 'ɪ'}, stressed=False)

NON_RIGHT_OPTIONAL_RULES = [
    Rule(
        [Sound('ʃ'), Sound('r')],
        [Stroke('SKHR')],
    ),
    Rule(
        [SCHWI, BREAK],
        [],
        lookbehind = [Sound()],
    ),
]

NON_RIGHT_RULES = [
    Rule(
        [Sound('', spelled='h')],
        [Stroke('H')],
    ),
    Rule(
        [Sound({'w', 'h'}, spelled='wh')],
        [Stroke('WH')],
    ),
    Rule(
        [Sound('ɪj')],
        [Stroke('AE')],
        lookahead = [BREAK],
    ),
    Rule(
        [Sound('ɑj', spelled='igh'), Sound('t')],
        [Stroke('OEUGT')],
    ),
    Rule(
        [SCHWI],
        [Stroke('U')],
        lookbehind = [BREAK],
        lookahead  = [Sound({'d', 'g', 'z'}), BREAK],
    ),
]

RIGHT_RULES = [
    Rule(
        [Sound('m'), Sound('p')],
        [Stroke('-FPL')],
    ),
    Rule(
        [Sound('m', spelled='mb')],
        [Stroke('-PL'), Stroke('-B')],
    ),
    Rule(
        [Sound('s'), Sound('t')],
        [Stroke('*S')],
    ),
]

for chords, rules in [
    (NON_RIGHT_CHORDS, NON_RIGHT_RULES),
    (RIGHT_CHORDS,     RIGHT_RULES),
]:
    for ipa, chord in chords.items():
        rules.append(Rule(
            [Sound(ipa)],
            [chord],
        ))

RULES = [
    [NON_RIGHT_OPTIONAL_RULES, NON_RIGHT_RULES],
    [RIGHT_RULES]
]

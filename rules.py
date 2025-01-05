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

    def match(self, sounds, pos, stroke, outline):
        end = pos + len(self.pattern)
        past    = sounds[:pos]
        present = sounds[pos:end]
        future  = sounds[end:]
        if self.pattern != present:
            return None
        for lookaround, ahead, negative in [
            (self.lookahead,           True,  False),
            (self.lookbehind,          False, False),
            (self.negative_lookahead,  True,  True),
            (self.negative_lookbehind, False, True),
        ]:
            if lookaround is not None:
                length = len(lookaround)
                sequence = future[:length] if ahead else past[-length:]
                condition = lookaround != sequence
                if negative:
                    condition = not(condition)
                if condition:
                    return None
        for test, obj in [(self.stroke, stroke), (self.outline, outline)]:
            if test is not None:
                if not test(obj):
                    return None
        return self.chords, len(self.pattern)

NON_RIGHT_CHORDS = LEFT_CHORDS | MID_CHORDS

SCHWA = Sound({'ə', 'ɪ', 'ʌ'}, stressed=False)

NON_RIGHT_OPTIONAL_RULES = [
    Rule(
        [Sound('ʃ'), Sound('r')],
        [Stroke('SKHR')],
    ),
    Rule(
        [SCHWA, BREAK],
        [],
        lookbehind = [Sound()],
    ),
]

NON_RIGHT_RULES = [
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
        [SCHWA, BREAK],
        [],
        lookbehind = [BREAK],
    ),
    Rule(
        [SCHWA],
        [Stroke('U')],
        lookbehind = [BREAK],
        lookahead = [Sound({'d', 'g', 'z'}), BREAK],
    ),
    Rule(
        [SCHWA],
        [Stroke('')],
        negative_lookahead = [BREAK],
        outline = lambda outline: bool(outline),
    ),
    Rule(
        [Sound('', spelled='h')],
        [Stroke('H')],
    ),
    Rule(
        [Sound('', spelled='w')],
        [Stroke('W')],
    ),
    Rule(
        [Sound('')],
        [],
    ),
]

RIGHT_RULES = [
    Rule(
        [Sound('m'), Sound('p')],
        [Stroke('-FPL')],
    ),
    Rule(
        [Sound('s'), Sound('t')],
        [Stroke('*S')],
    ),
    Rule(
        [Sound('ʃ'), BREAK, Sound('ə'), Sound('n')],
        [Stroke('-GZ')],
    ),
    Rule(
        [Sound('', spelled='b')],
        [Stroke('-B')],
    ),
    Rule(
        [Sound('')],
        [],
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

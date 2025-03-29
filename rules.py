from chords import LEFT_CHORDS, MID_CHORDS, RIGHT_CHORDS
from sound import Sound, START, BREAK, END
from stroke import Stroke, RIGHT_BANK

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

UNSTRESSED_SCHWA = Sound({'ə', 'ɪ', 'ʌ'}, stressed=False)

DIPHTHONG_OR_LONG_VOWEL = Sound({
    'ɪj', 'ɛj', 'ɑj', 'əw', 'oj', 'ʉw', 'aw',
    'ɪː', 'ɛː', 'ɑː', 'əː', 'oː', 'ɵː',
})

NON_RIGHT_OPTIONAL_RULES = [
    Rule(
        [UNSTRESSED_SCHWA, BREAK],
        [],
        negative_lookahead = [END],
        negative_lookbehind = [START],
    ),
    Rule(
        [Sound('j', ''), UNSTRESSED_SCHWA, BREAK],
        [],
        negative_lookahead = [END],
        lookbehind = [BREAK],
    ),
]

NON_RIGHT_RULES = [
    Rule(
        [Sound('ʃ'), Sound('r')],
        [Stroke('SKHR')],
    ),
    Rule(
        [Sound('g'), Sound('w')],
        [Stroke('TKPWU'), Stroke('W')],
        lookbehind = [START],
    ),
    Rule(
        [Sound('ɑj', 'i'), Sound('', 'gh'), Sound('t')],
        [Stroke('OEUGT')],
    ),
    Rule(
        [Sound('ə', 'r')],
        [Stroke('-R')],
    ),
    Rule(
        [Sound('m'), Sound('ə'), Sound('n'), Sound('t')],
        [Stroke('-PLT')],
    ),
    Rule(
        [Sound('ɪj')],
        [Stroke('AE')],
        lookahead = [BREAK, END],
        outline = lambda outline: outline,
    ),
    Rule(
        [Sound('ɪj'), Sound('z', 's')],
        [Stroke('AE'), Stroke('-Z')],
        lookahead = [BREAK, END],
        outline = lambda outline: outline,
    ),
    Rule(
        [UNSTRESSED_SCHWA],
        [Stroke('AU')],
        lookahead = [BREAK, END],
        lookbehind = [BREAK],
    ),
    Rule(
        [UNSTRESSED_SCHWA, Sound('z', 's')],
        [Stroke('AU'), Stroke('-Z')],
        lookahead = [BREAK, END],
        lookbehind = [BREAK],
        outline = lambda outline: outline,
    ),
    Rule(
        [UNSTRESSED_SCHWA, Sound('z', 's')],
        [Stroke('U'), Stroke('-Z')],
        lookahead = [BREAK, END],
        outline = lambda outline: outline,
    ),
    Rule(
        [UNSTRESSED_SCHWA],
        [Stroke('U')],
        lookahead = [Sound({'d', 'g', 'z'}), BREAK],
        lookbehind = [BREAK],
    ),
    Rule(
        [UNSTRESSED_SCHWA, BREAK],
        [],
        lookbehind = [BREAK],
    ),
    Rule(
        [UNSTRESSED_SCHWA],
        [Stroke('')],
        negative_lookahead = [BREAK],
        outline = lambda outline: outline,
    ),
    Rule(
        [Sound('j', '')],
        [],
        stroke = lambda stroke: stroke,
    ),
    Rule(
        [Sound('', 'h')],
        [Stroke('H')],
    ),
    Rule(
        [Sound('', 'w')],
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
        [Sound('n'), Sound('dʒ')],
        [Stroke('-FPG')],
    ),
    Rule(
        [Sound('ŋ'), Sound('g')],
        [Stroke('-PBG')],
    ),
    Rule(
        [Sound('m'), BREAK, Sound('ə'), Sound('n'), Sound('t')],
        [Stroke('-PLT')],
    ),
    Rule(
        [Sound('ŋ'), Sound('k'), BREAK, Sound('ʃ'), Sound('ə'), Sound('n')],
        [Stroke('-PGZ')],
    ),
    Rule(
        [Sound('ŋ'), Sound('k')],
        [Stroke('-PG')],
    ),
    Rule(
        [Sound('b'), BREAK, Sound('ə'), Sound('l')],
        [Stroke('-BL')],
    ),
    Rule(
        [Sound('k'), BREAK, Sound('ʃ'), Sound('ə'), Sound('n')],
        [Stroke('-BGZ')],
    ),
    Rule(
        [Sound('ʃ'), BREAK, Sound('ə'), Sound('n')],
        [Stroke('-GZ')],
    ),
    Rule(
        [Sound('s'), Sound('t')],
        [Stroke('*S')],
    ),
    Rule(
        [Sound('s', 'ss')],
        [Stroke('-FS')],
        lookahead = [BREAK, END],
        outline = lambda outline: not outline,
    ),
    Rule(
        [Sound('', 'r')],
        [Stroke('-R')],
    ),
    Rule(
        [BREAK, Sound('ə', 'r')],
        [Stroke('-R')],
    ),
    Rule(
        [Sound('', 'b')],
        [Stroke('-B')],
    ),
    Rule(
        [Sound('')],
        [],
    ),
    Rule(
        [Sound('z', 's')],
        [Stroke(''), Stroke('-Z')],
        lookahead = [BREAK, END],
        lookbehind = [DIPHTHONG_OR_LONG_VOWEL],
    ),
    Rule(
        [Sound({'s', 'z'}, 's')],
        [Stroke(''), Stroke('-Z')],
        lookahead = [BREAK, END],
        stroke = lambda stroke: stroke and stroke.last() == '-G',
    ),
    Rule(
        [Sound({'s', 'z'}, 's')],
        [Stroke('-Z')],
        lookahead = [BREAK, END],
        stroke = lambda stroke: stroke & RIGHT_BANK and stroke.last() != '-T',
    ),
]

for chords, rules in [
    (NON_RIGHT_CHORDS, NON_RIGHT_RULES),
    (RIGHT_CHORDS, RIGHT_RULES),
]:
    for ipa, chord in chords.items():
        rules.append(Rule([Sound(ipa)], [chord]))

RULES = [
    [NON_RIGHT_OPTIONAL_RULES, NON_RIGHT_RULES],
    [RIGHT_RULES]
]

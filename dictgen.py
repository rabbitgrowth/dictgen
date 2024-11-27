import re

from chords import NON_RIGHT_CHORDS, RIGHT_CHORDS
from clusters import ONSETS, CODAS
from stroke import Stroke

VOWEL = re.compile(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)')

class Sound:
    __match_args__ = 'sound',

    def __init__(self, sound, spelled=''):
        vowel = VOWEL.match(sound)
        if vowel:
            first, stress, second = vowel.groups()
            self.sound = first + second
            self.stressed = bool(stress)
            self.length = len(sound)
        else:
            self.sound = sound
            self.stressed = False
            self.length = 0
        self.spelled = spelled

    def is_vowel(self):
        return bool(self.length)

    def stronger_than(self, other):
        return self.stressed and not other.stressed

    def __eq__(self, other):
        return (
            self.sound == other.sound
            and self.stressed == other.stressed
            and self.length   == other.length
            and self.spelled  == other.spelled
        )

    def __repr__(self):
        sound = (
            self.sound[0] + '\u0301' + self.sound[1:]
            if self.stressed else self.sound
        )
        spelled = ':' + self.spelled if self.spelled else ''
        return sound + spelled

def parse_pron(pron):
    for word in pron.split():
        sound, _, spelled = word.partition(':')
        yield Sound(sound, spelled)

def group(sounds):
    consonant_clusters = []
    consonant_cluster  = []
    vowels = []
    for sound in sounds:
        if sound.is_vowel():
            consonant_clusters.append(consonant_cluster)
            consonant_cluster = []
            vowels.append(sound)
        else:
            consonant_cluster.append(sound)
    consonant_clusters.append(consonant_cluster)
    if not vowels:
        raise ValueError('no vowel')
    return consonant_clusters, vowels

def divide(sounds):
    return [(sounds[:i], sounds[i:]) for i in range(len(sounds)+1)]

def to_string(sounds):
    return ''.join(sound.sound for sound in sounds)

def is_possible_onset(sounds):
    return not sounds or to_string(sounds) in ONSETS

def is_possible_coda(sounds):
    return not sounds or to_string(sounds) in CODAS

def combine(parts):
    products = [[]]
    for part in parts:
        products = [product+branch for product in products for branch in part]
    return products

def syllabify(sounds):
    consonant_clusters, vowels = group(sounds)
    parts = [[consonant_clusters.pop(0)]]
    prev = None
    for vowel, consonant_cluster in zip(vowels, consonant_clusters, strict=True):
        if prev is not None:
            prev_vowel, prev_consonant_cluster = prev
            parts.append([[prev_vowel]])
            if Sound('.') in prev_consonant_cluster:
                parts.append([prev_consonant_cluster])
                continue
            divisions = divide(prev_consonant_cluster)
            if prev_vowel.stronger_than(vowel):
                divisions.pop(0) # stronger left vowel attracts at least one consonant
            elif vowel.stronger_than(prev_vowel):
                divisions.pop() # stronger right vowel attracts at least one consonant
            parts.append([
                [*coda, Sound('.'), *onset]
                for coda, onset in divisions
                if is_possible_coda(coda) and is_possible_onset(onset)
            ])
        prev = vowel, consonant_cluster
    parts.extend([[[vowel]], [consonant_cluster]])
    return combine(parts)

MID_AND_RIGHT = Stroke('AOEUFRPBLGTSDZ')

def crosses_boundary(chord):
    if not chord:
        return True
    last = Stroke(chord.last())
    return last & MID_AND_RIGHT

def in_steno_order(a, b):
    return not a or not b or Stroke(a.last()) < Stroke(b.first())

UNSTACKABLE = {
    (Stroke('SH'), Stroke('R')),
    # TODO add more cases like T + P and -P + -L?
}

STAR = Stroke('*')

def stackable(a, b):
    return (
        (a, b) not in UNSTACKABLE
        and not (STAR in a and STAR in b)
        and in_steno_order(a - STAR, b - STAR)
    )

def at_break(rest):
    return not rest or rest[0] == Sound('.')

def gen(sounds, right=False, stroke=Stroke(''), outline=()):
    if not sounds:
        yield outline+(stroke,)
        return

    if sounds[0] == Sound('.'):
        yield from gen(sounds[1:], False, Stroke(''), outline+(stroke,))
        return

    matches = []

    if not right:
        match sounds:
            case Sound('ʃ'), Sound('r'), *rest:
                chords = [Stroke('SKHR')]
            case _:
                chords = None
        if chords is not None:
            matches.append((chords, rest))

        match sounds:
            case Sound('', spelled='h'), *rest:
                chords = [Stroke('H')]
            case Sound('w'|'h', spelled='wh'), *rest:
                chords = [Stroke('WH')]
            case Sound('ə'|'ɪ', stressed=False), *rest if outline and not at_break(rest):
                chords = [Stroke('')]
            case Sound('ɑj', spelled='igh'), Sound('t'), *rest:
                chords = [Stroke('OEUGT')]
            case sound, *rest:
                chords = [NON_RIGHT_CHORDS.get(sound.sound)]
        matches.append((chords, rest))

    else:
        match sounds:
            case Sound('m'), Sound('p'), *rest:
                chords = [Stroke('-FPL')]
            case Sound('m', spelled='mb'), *rest:
                chords = [Stroke('-PL'), Stroke('-B')]
            case Sound('s'), Sound('t'), *rest:
                chords = [Stroke('*S')]
            case sound, *rest:
                chords = [RIGHT_CHORDS.get(sound.sound)]
        matches.append((chords, rest))

    for chords, rest in matches:
        new_right   = right
        new_stroke  = stroke
        new_outline = outline
        for i, chord in enumerate(chords):
            if crosses_boundary(chord):
                new_right = True
            if i:
                new_outline += (new_stroke,)
                new_stroke = Stroke('')
            if stackable(new_stroke, chord):
                new_stroke |= chord
            else:
                if not new_right:
                    new_stroke |= Stroke('U')
                new_outline += (new_stroke,)
                new_stroke = chord
        yield from gen(rest, new_right, new_stroke, new_outline)

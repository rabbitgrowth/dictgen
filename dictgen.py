import re

from chords import NON_RIGHT_CHORDS, RIGHT_CHORDS
from clusters import ONSETS, CODAS
from stroke import Stroke

VOWEL = re.compile(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)')

class Sound:
    __match_args__ = 'sound', 'spelling'

    def __init__(self, sound, spelling=''):
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
        self.spelling = spelling

    def is_vowel(self):
        return bool(self.length)

    def stronger_than(self, other):
        return self.stressed and not other.stressed

    def __eq__(self, other):
        return (
            self.sound == other.sound
            and self.stressed == other.stressed
            and self.length   == other.length
            and self.spelling == other.spelling
        )

    def __repr__(self):
        sound = (
            (self.sound[0] + '\u0301' + self.sound[1:])
            if self.stressed
            else self.sound
        )
        spelling = ':' + self.spelling if self.spelling else ''
        return sound + spelling

BREAK = Sound('.')

def parse_pron(pron):
    for word in pron.split():
        sound, _, spelling = word.partition(':')
        yield Sound(sound, spelling)

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
            if BREAK in prev_consonant_cluster:
                parts.append([prev_consonant_cluster])
                continue
            divisions = divide(prev_consonant_cluster)
            if prev_vowel.stronger_than(vowel):
                divisions.pop(0) # stronger left vowel attracts at least one consonant
            elif vowel.stronger_than(prev_vowel):
                divisions.pop() # stronger right vowel attracts at least one consonant
            parts.append([
                [*coda, BREAK, *onset]
                for coda, onset in divisions
                if is_possible_coda(coda) and is_possible_onset(onset)
            ])
        prev = vowel, consonant_cluster
    parts.extend([[[vowel]], [consonant_cluster]])
    return combine(parts)

NULL = Stroke('')

LEFT, MID, RIGHT = map(Stroke, ['STKPWHR', 'AOEU', 'FRPBLGTSDZ'])

ODD_CASES = {
    (Stroke('SH'), Stroke('R')),
    # TODO add more cases like T + P and -P + -L?
}

def in_steno_order(a, b):
    # Reject cases that are technically in steno order but cause conflicts
    # and don't feel right, like using SHR for shr-:
    # SHRED  "sled"
    # SKHRED "shred" (or SHU/RED)
    return (
        (not a or not b or Stroke(a.last()) < Stroke(b.first()))
        and (a, b) not in ODD_CASES
    )

def crosses_boundary(chord):
    # TODO handle null chord from VOP
    last = Stroke(chord.last())
    return last & MID or last & RIGHT

def gen(sounds, right=False, stroke=NULL, outline=[]):
    if not sounds:
        return {tuple(outline+[stroke])}

    sound, *rest = sounds

    if sound == BREAK:
        return gen(rest, False, NULL, outline+[stroke])

    matches = []

    if not right:
        match sounds:
            case [Sound('ʃ'), Sound('r'), *rest]:
                matches.append((Stroke('SKHR'), rest))
        match sounds:
            case [Sound('', 'h'), *rest]:
                matches.append((Stroke('H'), rest))
            case [Sound('w'|'h', 'wh'), *rest]:
                matches.append((Stroke('WH'), rest))
            case [Sound('ɑj', 'igh'), Sound('t'), *rest]:
                matches.append((Stroke('OEUGT'), rest))
            case [Sound(), *rest]:
                chord = NON_RIGHT_CHORDS.get(sound.sound)
                matches.append((chord, rest))
    else:
        match sounds:
            case [Sound('m'), Sound('p'), *rest]:
                matches.append((Stroke('-FPL'), rest))
            case [Sound('s'), Sound('t'), *rest]:
                matches.append((Stroke('-SZ'), rest)) # TODO change to *S
            case [Sound(), *rest]:
                chord = RIGHT_CHORDS.get(sound.sound)
                matches.append((chord, rest))

    results = set()

    for chord, rest in matches:
        if chord is None:
            return set()
        if crosses_boundary(chord):
            right = True
        if in_steno_order(stroke, chord):
            results |= gen(rest, right, stroke|chord, outline)
        else:
            if not right:
                stroke |= Stroke('U')
            results |= gen(rest, right, chord, outline+[stroke])

    return results

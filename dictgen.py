import re

from chords import NON_RIGHT_CHORDS, RIGHT_CHORDS
from clusters import ONSETS, CODAS
from stroke import Stroke

VOWEL = re.compile(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)')

class Sound:
    __match_args__ = ('ipa', 'spelling')

    def __init__(self, ipa, spelling):
        vowel = VOWEL.match(ipa)
        if vowel:
            first, stress, second = vowel.groups()
            self.ipa = first + second
            self.stressed = bool(stress)
            self.length = len(ipa)
        else:
            self.ipa = ipa
            self.stressed = False
            self.length = 0
        self.spelling = spelling

    def is_vowel(self):
        return bool(self.length)

    def stronger_than(self, other):
        return self.stressed and not other.stressed

    def __repr__(self):
        stress_mark = 'ˈ' if self.stressed else ''
        return stress_mark + self.ipa

def separate(sounds):
    consonant_clusters = []
    consonant_cluster = []
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
    return ''.join(sound.ipa for sound in sounds)

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
    consonant_clusters, vowels = separate(sounds)
    parts = [[consonant_clusters.pop(0)]]
    prev = None
    for vowel, consonant_cluster in zip(vowels, consonant_clusters, strict=True):
        if prev is not None:
            prev_vowel, prev_consonant_cluster = prev
            parts.append([[prev_vowel]])
            divisions = divide(prev_consonant_cluster)
            if prev_vowel.stronger_than(vowel):
                divisions.pop(0) # stronger left vowel attracts at least one consonant
            elif vowel.stronger_than(prev_vowel):
                divisions.pop() # stronger right vowel attracts at least one consonant
            parts.append([[*coda, None, *onset]
                          for coda, onset in divisions
                          if is_possible_coda(coda) and is_possible_onset(onset)])
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
    return ((not a or not b or Stroke(a.last()) < Stroke(b.first()))
            and (a, b) not in ODD_CASES)

def crosses_boundary(chord):
    # TODO handle null chord from VOP
    last = Stroke(chord.last())
    return last & MID or last & RIGHT

def gen(sounds, right=False, stroke=NULL, outline=[]):
    if not sounds:
        return {tuple(outline+[stroke])}

    sound, *rest = sounds
    if sound is None:
        return gen(rest, False, NULL, outline+[stroke])

    matches = []

    if not right:
        match sounds:
            case [Sound('ʃ'), Sound('r'), *rest]:
                matches.append((Stroke('SKHR'), rest))
        match sounds:
            case [Sound('ɑj', 'igh'), Sound('t', 't'), *rest]:
                matches.append((Stroke('OEUGT'), rest))
            case [Sound(), *rest]:
                chord = NON_RIGHT_CHORDS.get(sound.ipa)
                matches.append((chord, rest))
    else:
        match sounds:
            case [Sound('m'), Sound('p'), *rest]:
                matches.append((Stroke('-FPL'), rest))
            case [Sound('s'), Sound('t'), *rest]:
                matches.append((Stroke('-SZ'), rest)) # TODO change to *S
            case [Sound(), *rest]:
                chord = RIGHT_CHORDS.get(sound.ipa)
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

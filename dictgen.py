import re
from dataclasses import dataclass
from functools import total_ordering

from plover_stroke import BaseStroke

def divide(lst):
    return [(lst[:i], lst[i:]) for i in range(len(lst)+1)]

@dataclass
@total_ordering
class Sound:
    symbols: str
    stressed: bool
    length: int
    letters: str

    def is_consonant(self):
        return not(self.length)

    # TODO don't just check stress?
    def __eq__(self, other):
        if isinstance(other, Sound):
            return self.stressed == other.stressed
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Sound):
            return not self.stressed and other.stressed
        return NotImplemented

    def __repr__(self):
        stress_mark = "'" if self.stressed else ''
        return stress_mark + self.symbols

VOWEL = re.compile(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)')

def to_sounds(pairs):
    sounds = []
    for letters, symbols in pairs:
        match = VOWEL.match(symbols)
        if match: # vowel
            first, stress, second = match.groups()
            symbols = first + second
            stressed = bool(stress)
            length = len(symbols)
        else: # consonant
            stressed = False
            length = 0
        sounds.append(Sound(symbols, stressed, length, letters))
    return sounds

def separate(sounds):
    consonant_clusters = []
    consonant_cluster = []
    vowels = []
    for sound in sounds:
        if sound.is_consonant():
            consonant_cluster.append(sound)
        else: # vowel
            consonant_clusters.append(consonant_cluster)
            consonant_cluster = []
            vowels.append(sound)
    consonant_clusters.append(consonant_cluster)
    if not vowels:
        raise ValueError('no vowel')
    return consonant_clusters, vowels

def read_clusters(file):
    with open(file) as f:
        return set(map(str.strip, f))

ONSETS, CODAS = (read_clusters(f'clusters/{stem}.txt')
                 for stem in ['onsets', 'codas'])

def to_string(sounds):
    return ''.join(sound.symbols for sound in sounds)

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
            if prev_vowel > vowel:
                divisions.pop(0) # stronger left vowel attracts at least one consonant
            elif prev_vowel < vowel:
                divisions.pop() # stronger right vowel attracts at least one consonant
            parts.append([[*coda, None, *onset]
                          for coda, onset in divisions
                          if is_possible_coda(coda) and is_possible_onset(onset)])
        prev = vowel, consonant_cluster
    parts.extend([[[vowel]], [consonant_cluster]])
    return combine(parts)

class Stroke(BaseStroke):
    pass

Stroke.setup(
    '# S- T- K- P- W- H- R- A- O- * -E -U -F -R -P -B -L -G -T -S -D -Z'.split(),
    'A- O- * -E -U'.split(),
)

NULL = Stroke('')

LEFT, MID, RIGHT = map(Stroke, ['STKPWHR', 'AOEU', 'FRPBLGTSDZ'])

def read_chords(file):
    with open(file) as f:
        chords = {}
        for line in f:
            symbols, chord = line.strip().split()
            chords[symbols] = Stroke(chord)
    return chords

LEFT_CONSONANTS, VOWELS, RIGHT_CONSONANTS = (read_chords(f'chords/{stem}.txt')
                                             for stem in ['left', 'mid', 'right'])

NON_RIGHT_SOUNDS = LEFT_CONSONANTS | VOWELS

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
    last = Stroke(chord.last())
    return last & MID or last & RIGHT

def gen(sounds, right=False, stroke=NULL, outline=[]):
    if not sounds:
        return {tuple(outline+[stroke])}

    sound, *rest = sounds

    if sound is None:
        return gen(rest, False, NULL, outline+[stroke])

    matches = []

    match sounds:
        case [Sound('ʃ'), Sound('r'), *rest]:
            matches.append((Stroke('SKHR'), rest))
        # ...

    match sounds:
        # ...
        case [sound, *rest]:
            pool = [NON_RIGHT_SOUNDS, RIGHT_CONSONANTS][right]
            chord = pool.get(sound.symbols)
            if chord is None:
                return set()
            matches.append((chord, rest))

    results = set()

    for chord, rest in matches:
        if crosses_boundary(chord):
            right = True
        if in_steno_order(stroke, chord):
            results |= gen(rest, right, stroke|chord, outline)
        else:
            if not right:
                stroke |= Stroke('U')
            results |= gen(rest, right, chord, outline+[stroke])

    return results

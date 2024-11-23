import re
from dataclasses import dataclass
from functools import total_ordering
from itertools import pairwise

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
        return '/' + stress_mark + self.symbols + '/'

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

# TODO
def is_possible_onset(consonant_cluster):
    return True

def is_possible_coda(consonant_cluster):
    return True

def combine(parts):
    products = [[]]
    for part in parts:
        products = [product+branch for product in products for branch in part]
    return products

def syllabify(sounds):
    consonant_clusters, vowels = separate(sounds)
    assert len(consonant_clusters) >= 2
    assert len(vowels) >= 1
    consonant_clusters = iter(consonant_clusters)
    initial_consonant_cluster = next(consonant_clusters)
    parts = [[initial_consonant_cluster]]
    right_vowel = vowels[0] # default for the shortest case
                            # (consonant cluster, vowel, consonant cluster)
    for (left_vowel, right_vowel), consonant_cluster in zip(pairwise(vowels),
                                                            consonant_clusters):
        parts.append([[left_vowel]])
        divisions = divide(consonant_cluster)
        if left_vowel > right_vowel:
            divisions.pop(0) # stronger left vowel attracts at least one consonant
        elif left_vowel < right_vowel:
            divisions.pop() # stronger right vowel attracts at least one consonant
        parts.append([[*coda, None, *onset]
                      for coda, onset in divisions
                      if is_possible_coda(coda) and is_possible_onset(onset)])
    final_consonant_cluster = next(consonant_clusters)
    assert next(consonant_clusters, None) is None
    parts.extend([[[right_vowel]], [final_consonant_cluster]])
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

LEFT_CONSONANTS, VOWELS, RIGHT_CONSONANTS = (
    read_chords(f'chords/{basename}.txt')
    for basename in ['left', 'mid', 'right']
)

ODD_CASES = {
    (Stroke('SH'), Stroke('R')),
    (Stroke('-P'), Stroke('-L')),
}

def in_steno_order(a, b):
    # Reject cases that are technically in steno order but cause conflicts
    # and don't feel right, like using SHR for shr-:
    # SHRED  "sled"
    # SKHRED "shred" (or SHU/RED)
    return ((not a or not b or Stroke(a.last()) < Stroke(b.first()))
            and (a, b) not in ODD_CASES)

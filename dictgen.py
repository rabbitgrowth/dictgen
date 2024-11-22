import re
from dataclasses import dataclass

from plover_stroke import BaseStroke

@dataclass
class Sound:
    symbols: str
    stressed: bool
    length: int
    letters: str

VOWEL = re.compile(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)')

def parse_pairs(pairs):
    sounds = []
    for letters, symbols in pairs:
        match = VOWEL.match(symbols)
        if match:
            first, stress, second = match.groups()
            symbols = first + second
            stressed = bool(stress)
            length = len(symbols)
        else:
            stressed = False
            length = 0
        sounds.append(Sound(symbols, stressed, length, letters))
    return sounds

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

def prefixes(pairs):
    prefix = []
    for pair in pairs:
        prefix.append(pair)
        yield prefix, pairs[len(prefix):]

ODD_CASES = {
    (Stroke('SH'), Stroke('R')),
    (Stroke('-P'), Stroke('-L')),
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

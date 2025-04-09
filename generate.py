import re

from rules import RULES
from sound import START, BREAK, END
from stroke import Stroke, MID_BANK, RIGHT_BANK
from syllabify import syllabify

MID_AND_RIGHT_BANKS = MID_BANK | RIGHT_BANK

def crosses_boundary(chord):
    if not chord:
        return True
    return bool(Stroke(chord.last()) & MID_AND_RIGHT_BANKS)

STAR = Stroke('*')

UNSTACKABLE = {
    (Stroke('SH'), Stroke('R')),
    (Stroke('T'),  Stroke('P')),
}

def in_steno_order(a, b):
    return not a or not b or Stroke(a.last()) < Stroke(b.first())

def stackable(a, b):
    return (
        (a, b) not in UNSTACKABLE
        and not (STAR in a and STAR in b)
        and in_steno_order(a - STAR, b - STAR)
    )

def gen(sounds, pos=0, right=False, stroke=Stroke(''), outline=[]):
    sound = sounds[pos]
    if sound == START:
        yield from gen(sounds, pos + 1, right, stroke, outline)
    elif sound == BREAK:
        yield from gen(sounds, pos + 1, False, Stroke(''), outline + [stroke])
    elif sound == END:
        try:
            i = outline.index(Stroke('AE'), 1)
        except ValueError:
            pass
        else:
            if not outline[i - 1] & MID_BANK:
                outline[i - 1] |= outline.pop(i)
        yield tuple(outline)
        return

    matches = []
    for rules in RULES[right]:
        for rule in rules:
            match = rule.match(sounds, pos, stroke, outline)
            if match is not None:
                matches.append(match)
                break

    for chords, length in matches:
        new_pos     = pos + length
        new_right   = right
        new_stroke  = stroke
        new_outline = outline.copy()
        for i, chord in enumerate(chords):
            if i:
                new_outline.append(new_stroke)
                new_stroke = Stroke('')
            if stackable(new_stroke, chord):
                new_stroke |= chord
            else:
                if not new_right:
                    return
                new_outline.append(new_stroke)
                new_stroke = chord
            new_right = crosses_boundary(chord)
        yield from gen(sounds, new_pos, new_right, new_stroke, new_outline)

def generate(sounds):
    return sorted({
        outline
        for syllabification in syllabify(sounds)
        for outline in gen(syllabification)
    })

import re

from plover_stroke import BaseStroke

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

NON_RIGHT_SOUNDS = LEFT_CONSONANTS | VOWELS

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

SHORT_VOWELS = {
    Stroke('AEU'):  Stroke('A'),
    Stroke('AOE'):  Stroke('E'),
    Stroke('AOEU'): Stroke('EU'),
    Stroke('OE'):   Stroke('O'),
}

def destress(pron):
    return re.sub(r'''
          (?<![əɪ]) \u0301
        | (?<=ɪ) \u0301 (?=j)
        | (?<=ə) \u0301 (?=w)
    ''', '', pron, flags=re.VERBOSE)

def gen(pairs, right=False, stroke=NULL, outline=[]):
    if not pairs:
        # Reject strokes with left-bank keys only, which don't form syllables
        # and are reserved for briefs:
        # T      "it"
        # START  "start"
        # STAR/T "star it"
        if stroke & MID or stroke & RIGHT:
            yield [*outline, stroke]
        return

    for prefix, rest in prefixes(pairs):
        chord = None

        if not right:
            match prefix, rest:
                case [('c', 's')], _:
                    chord = Stroke('KR')
                case [(_, 'ɪj')], [] if outline:
                    chord = Stroke('AE')
                case [(_, sound)], _:
                    chord = NON_RIGHT_SOUNDS.get(sound)
                case [(_, 'ʃ'), (_, 'r')], _:
                    chord = Stroke('SKHR')
        else:
            match prefix, rest:
                case [(_, sound)], _:
                    chord = RIGHT_CONSONANTS.get(sound)

        if chord is None:
            continue

        if chord & LEFT or chord & RIGHT:
            if in_steno_order(stroke, chord):
                if right:
                    yield from gen(rest, False, NULL, outline+[stroke|chord])
                yield from gen(rest, right, stroke|chord, outline)
            else:
                if not right:
                    # If a word begins with a series of consonants that are out of steno order,
                    # insert schwas in between:
                    #   TKPWU/WEPB "Gwen"
                    # This rule doesn't apply in the middle of a word, where there are usually
                    # more efficient breaks:
                    #   SEG/WAEU "segue" (not SE/TKPWU/WAEU)
                    # This also helps to prevent very awkward breaks:
                    #   AB/SES "abscess" (not A/PWU/SES)
                    if not outline: # building the first stroke
                        yield from gen(rest, right, chord, outline+[stroke|Stroke('U')])
                else:
                    yield from gen(pairs, False, NULL, outline+[stroke])
        elif not right and chord & MID:
            short_vowel = SHORT_VOWELS.get(chord, chord)
            yield from gen(rest, False, NULL, outline+[stroke|short_vowel])
            yield from gen(rest, True, stroke|chord, outline)

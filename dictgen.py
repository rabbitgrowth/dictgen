from plover_stroke import BaseStroke

class Stroke(BaseStroke):
    pass

Stroke.setup(
    '# S- T- K- P- W- H- R- A- O- * -E -U -F -R -P -B -L -G -T -S -D -Z'.split(),
    'A- O- * -E -U'.split(),
)

NULL = Stroke('')

L, M, R = map(Stroke, ['STKPWHR', 'AOEU', 'FRPBLGTSDZ'])

def read_chords(file):
    with open(file) as f:
        chords = {}
        for line in f:
            sound, chord = line.strip().split()
            chords[sound] = Stroke(chord)
    return chords

LC, V, RC = (read_chords(f'chords/{basename}.txt') for basename in ['LC', 'V', 'RC'])

def prefixes(pron):
    for i in range(1, len(pron)+1):
        yield pron[:i], pron[i:]

ODD_CASES = {
    (Stroke('SH'), Stroke('R')),
    (Stroke('-P'), Stroke('-L')),
}

def in_steno_order(a, b):
    # Reject cases that are technically in steno order but cause conflicts and
    # don't feel right, like using SHR for shr-:
    # SHRED  "sled"
    # SKHRED "shred" (or SHU/RED)
    return (not a or not b or Stroke(a.last()) < Stroke(b.first())) and (a, b) not in ODD_CASES

def gen(pron, right=False, stroke=NULL, outline=[], level=0):
    print('  '*level, end='')
    print(pron or '-', 'LR'[right], stroke or '-', '/'.join(map(str, outline)) or '-', sep=' ')
    level += 1

    if not pron:
        # Reject strokes with left-bank keys only, which are reserved for briefs:
        # T      "it"
        # START  "start"
        # STAR/T "star it"
        if stroke & (M|R):
            yield [*outline, stroke]
        return

    C = LC if not right else RC

    for sound, sounds in prefixes(pron):
        if sound in C:
            chord = C[sound]
            if in_steno_order(stroke, chord):
                if right:
                    yield from gen(sounds, False, NULL, [*outline, stroke|chord], level)
                yield from gen(sounds, right, stroke|chord, [*outline], level)
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
                        yield from gen(sounds, right, chord, [*outline, stroke|Stroke('U')], level)
                else:
                    yield from gen(sound+sounds, False, NULL, [*outline, stroke], level)
        elif not right and sound in V:
            chord = V[sound]
            yield from gen(sounds, False, NULL, [*outline, stroke|chord], level)
            yield from gen(sounds, True, stroke|chord, [*outline], level)

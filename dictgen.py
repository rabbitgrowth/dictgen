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

def in_steno_order(a, b):
    return not a or not b or Stroke(a.last()) < Stroke(b.first())

def gen(pron, right=False, stroke=NULL, outline=[], l=0):
    print('  '*l, end='')
    print(
        '-' if not pron else ''.join(pron),
        'L' if not right else 'R',
        '-' if not stroke else stroke,
        '-' if not outline else '/'.join(map(str, outline)),
        sep=' '
    )

    if not pron:
        # Reject strokes with left-bank keys only, which are reserved for briefs
        # T      it
        # START  start
        # STAR/T star it
        if stroke & (M|R):
            yield [*outline, stroke]
        return

    consonants = LC if not right else RC

    for sound, sounds in prefixes(pron):
        if sound in consonants:
            chord = consonants[sound]
            if in_steno_order(stroke, chord):
                if right:
                    yield from gen(sounds, False, NULL, [*outline, stroke|chord], l+1)
                yield from gen(sounds, right, stroke|chord, [*outline], l+1)
            else:
                if not right:
                    yield from gen(sounds, right, chord, [*outline, stroke|Stroke('U')], l+1)
                else:
                    yield from gen([sound, *sounds], False, NULL, [*outline, stroke], l+1)
        elif not right and sound in V:
            chord = V[sound]
            yield from gen(sounds, True, stroke|chord, [*outline], l+1)

from plover_stroke import BaseStroke

class Stroke(BaseStroke):
    pass

Stroke.setup(
    '# S- T- K- P- W- H- R- A- O- * -E -U -F -R -P -B -L -G -T -S -D -Z'.split(),
    'A- O- * -E -U'.split(),
)

NULL = Stroke('')

def read_chords(file):
    with open(file) as f:
        chords = {}
        for line in f:
            sound, chord = line.strip().split()
            chords[sound] = Stroke(chord)
    return chords

LEFT, RIGHT, VOWELS = (read_chords(f'chords/{basename}.txt')
                       for basename in ['left', 'right', 'vowels'])

def in_steno_order(a, b):
    return not a or not b or Stroke(a.last()) < Stroke(b.first())

def gen(sounds, right=False, stroke=NULL, outline=[], l=0):
    print('  '*l, end='')
    print(
        '-' if not sounds else ''.join(sounds),
        'L' if not right else 'R',
        '-' if not stroke else stroke,
        '-' if not outline else '/'.join(map(str, outline)),
        sep=' '
    )

    if not sounds:
        if stroke:
            yield [*outline, stroke]
        return

    sound = sounds[0]

    consonants = LEFT if not right else RIGHT

    if sound in consonants:
        chord = consonants[sound]
        if in_steno_order(stroke, chord):
            if right:
                yield from gen(sounds[1:], False, NULL, [*outline, stroke|chord], l+1)
            yield from gen(sounds[1:], right, stroke|chord, [*outline], l+1)
        else:
            if not right:
                yield from gen(sounds[1:], right, chord, [*outline, stroke|Stroke('U')], l+1)
            else:
                yield from gen(sounds, False, NULL, [*outline, stroke], l+1)
    elif not right and sound in VOWELS:
        chord = VOWELS[sound]
        yield from gen(sounds[1:], True, stroke|chord, [*outline], l+1)

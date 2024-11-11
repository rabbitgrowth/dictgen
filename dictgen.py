from plover_stroke import BaseStroke

class Stroke(BaseStroke):
    pass

Stroke.setup(
    '# S- T- K- P- W- H- R- A- O- * -E -U -F -R -P -B -L -G -T -S -D -Z'.split(),
    'A- O- * -E -U'.split(),
)

def read_chords(file):
    with open(file) as f:
        chords = {}
        for line in f:
            sound, chord = line.strip().split()
            chords[sound] = Stroke(chord)
    return chords

LEFT   = read_chords('chords/left.txt')
RIGHT  = read_chords('chords/right.txt')
VOWELS = read_chords('chords/vowels.txt')

def in_steno_order(a, b):
    return not a or not b or Stroke(a.last()) < Stroke(b.first())

def gen(sounds, left=True, stroke=Stroke(''), outline=[]):
    print(sounds, left, stroke, outline, sep=' | ')

    if not sounds:
        if stroke:
            yield [*outline, stroke]
        return

    sound = sounds[0]

    consonants = LEFT if left else RIGHT

    if sound in consonants:
        chord = consonants[sound]
        if in_steno_order(stroke, chord):
            yield from gen(sounds[1:], left, stroke | chord, outline.copy())
        else:
            if left:
                yield from gen(sounds[1:], left, chord, [*outline, stroke | Stroke('U')])
            else:
                yield from gen(sounds, True, Stroke(''), [*outline, stroke])
    elif left and sound in VOWELS:
        chord = VOWELS[sound]
        yield from gen(sounds[1:], False, stroke | chord, outline.copy())
    else:
        raise ValueError(f'unknown sound {sound}')

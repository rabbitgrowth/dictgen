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

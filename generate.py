import re

from clusters import ONSETS, CODAS
from rules import RULES
from sound import START, BREAK, END
from stroke import Stroke, MID_BANK, RIGHT_BANK

def syllabify(sounds):
    clusters, vowels = group_by_type(sounds)
    if len(vowels) < 2:
        return [sounds]
    prev = None
    parts = [[clusters.pop(0)]]
    assert len(vowels) == len(clusters)
    for vowel, cluster in zip(vowels, clusters):
        if prev is not None:
            prev_vowel, prev_cluster = prev
            parts.append([[prev_vowel]])
            if BREAK in prev_cluster:
                # Use the pre-inserted break
                parts.append([prev_cluster])
                continue
            consonant_indices = [
                i
                for i, sound in enumerate(prev_cluster)
                if sound.is_consonant() or sound.spell == 'r'
            ]
            start = 0
            stop = len(prev_cluster) + 1
            if consonant_indices:
                if prev_vowel.stressed and (len(consonant_indices) > 1 or not vowel.stressed):
                    start = consonant_indices[0] + 1
                if vowel.stressed:
                    stop = consonant_indices[-1] + 1
            splits = [(prev_cluster[:i], prev_cluster[i:]) for i in range(start, stop)]
            parts.append([
                [*coda, BREAK, *onset]
                for coda, onset in splits
                if is_possible_coda(coda) and is_possible_onset(onset)
            ])
        prev = vowel, cluster
    parts.extend([[[vowel]], [cluster]])
    return combine(parts)

def group_by_type(sounds):
    clusters = []
    cluster  = []
    vowels = []
    for sound in sounds:
        if sound.is_vowel():
            clusters.append(cluster)
            cluster = []
            vowels.append(sound)
        else:
            cluster.append(sound)
    clusters.append(cluster)
    assert len(clusters) == len(vowels) + 1
    return clusters, vowels

def to_string(sounds):
    return ''.join(sound.ipa for sound in sounds)

def is_possible_onset(sounds):
    return to_string(sounds) in ONSETS

def is_possible_coda(sounds):
    return to_string(sounds) in CODAS

def combine(parts):
    results = [[]]
    for part in parts:
        results = [result + choice for result in results for choice in part]
    return results

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
    sounds = [START, *sounds, BREAK, END]
    return sorted({
        outline
        for syllabifications in syllabify(sounds)
        for outline in gen(syllabifications)
    })

import re

from clusters import ONSETS, CODAS
from rules import RULES
from sound import Sound, BREAK
from stroke import Stroke

def syllabify(sounds):
    consonant_clusters, vowels = group_by_type(sounds)
    if len(vowels) < 2:
        return [sounds]
    prev = None
    parts = [[consonant_clusters.pop(0)]]
    assert len(vowels) == len(consonant_clusters)
    for vowel, consonant_cluster in zip(vowels, consonant_clusters):
        if prev is not None:
            prev_vowel, prev_consonant_cluster = prev
            parts.append([[prev_vowel]])
            if BREAK in prev_consonant_cluster:
                # Use the pre-inserted break
                parts.append([prev_consonant_cluster])
                continue
            splits = split(prev_consonant_cluster)
            if len(splits) > 1:
                # The stronger vowel attracts at least one consonant
                if prev_vowel.stronger_than(vowel):
                    splits.pop(0)
                elif vowel.stronger_than(prev_vowel):
                    splits.pop()
            parts.append([
                [*coda, BREAK, *onset]
                for coda, onset in splits
                if is_possible_coda(coda) and is_possible_onset(onset)
            ])
        prev = vowel, consonant_cluster
    parts.extend([[[vowel]], [consonant_cluster]])
    return combine(parts)

def group_by_type(sounds):
    consonant_clusters = []
    consonant_cluster  = []
    vowels = []
    for sound in sounds:
        if sound.is_vowel():
            consonant_clusters.append(consonant_cluster)
            consonant_cluster = []
            vowels.append(sound)
        else:
            consonant_cluster.append(sound)
    consonant_clusters.append(consonant_cluster)
    assert len(consonant_clusters) == len(vowels) + 1
    return consonant_clusters, vowels

def split(sounds):
    return [(sounds[:i], sounds[i:]) for i in range(len(sounds)+1)]

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

MID_AND_RIGHT_BANKS = Stroke('AOEUFRPBLGTSDZ')

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
    if pos == len(sounds):
        yield tuple(outline)
        return

    if sounds[pos] == BREAK:
        yield from gen(sounds, pos+1, False, Stroke(''), outline+[stroke])
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
                new_right = False
            if crosses_boundary(chord):
                new_right = True
            if stackable(new_stroke, chord):
                new_stroke |= chord
            else:
                if not new_right:
                    new_stroke |= Stroke('U')
                new_outline.append(new_stroke)
                new_stroke = chord
                new_right = False
        yield from gen(sounds, new_pos, new_right, new_stroke, new_outline)

def generate(sounds):
    sounds.append(BREAK)
    return sorted({
        outline
        for syllabifications in syllabify(sounds)
        for outline in gen(syllabifications)
    })

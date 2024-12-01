import re

from clusters import ONSETS, CODAS
from rules import RULES
from sound import Sound, BREAK
from stroke import Stroke

VOWEL = re.compile(r'([aɑɛɪɔoɵʉʌə])(\u0301?)([ːjw]?)')

def parse_ipa(ipa):
    vowel = VOWEL.match(ipa)
    if vowel:
        first, stress, second = vowel.groups()
        ipa = first + second
        stressed = bool(stress)
    else:
        stressed = False
    return Sound(ipa, stressed)

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
    if not vowels:
        raise ValueError('no vowel')
    return consonant_clusters, vowels

def divide(sounds):
    return [(sounds[:i], sounds[i:]) for i in range(len(sounds)+1)]

def to_string(sounds):
    return ''.join(sound.ipa for sound in sounds)

def is_possible_onset(sounds):
    return not sounds or to_string(sounds) in ONSETS

def is_possible_coda(sounds):
    return not sounds or to_string(sounds) in CODAS

def combine(parts):
    products = [[]]
    for part in parts:
        products = [product+choice for product in products for choice in part]
    return products

def syllabify(sounds):
    consonant_clusters, vowels = group_by_type(sounds)
    parts = [[consonant_clusters.pop(0)]]
    prev = None
    for vowel, consonant_cluster in zip(vowels, consonant_clusters):
        if prev is not None:
            prev_vowel, prev_consonant_cluster = prev
            parts.append([[prev_vowel]])
            if BREAK in prev_consonant_cluster:
                parts.append([prev_consonant_cluster])
                continue
            divisions = divide(prev_consonant_cluster)
            if len(divisions) > 1:
                # The stronger vowel attracts at least one consonant
                if prev_vowel.stronger_than(vowel):
                    divisions.pop(0)
                elif vowel.stronger_than(prev_vowel):
                    divisions.pop()
            parts.append([
                [*coda, BREAK, *onset]
                for coda, onset in divisions
                if is_possible_coda(coda) and is_possible_onset(onset)
            ])
        prev = vowel, consonant_cluster
    parts.extend([[[vowel]], [consonant_cluster]])
    return combine(parts)

MID_BANK   = Stroke('AOEU')
RIGHT_BANK = Stroke('FRPBLGTSDZ')

MID_AND_RIGHT_BANKS = MID_BANK | RIGHT_BANK

def crosses_boundary(chord):
    if not chord:
        return True
    return bool(Stroke(chord.last()) & MID_AND_RIGHT_BANKS)

def in_steno_order(a, b):
    return not a or not b or Stroke(a.last()) < Stroke(b.first())

UNSTACKABLE = {
    (Stroke('SH'), Stroke('R')),
    # TODO add more cases like T + P and -P + -L?
}

STAR = Stroke('*')

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
        yield from gen(sounds, pos+length, new_right, new_stroke, new_outline)

def generate(sounds):
    sounds.append(BREAK)
    return {
        outline
        for syllables in syllabify(sounds)
        for outline in gen(syllables)
    }

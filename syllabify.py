from clusters import ONSETS, CODAS
from sound import BREAK

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
    vowels   = []
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

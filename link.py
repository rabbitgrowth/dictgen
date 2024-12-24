from sound import Sound

PAIRS = [
    ('', [Sound('.')]),
    ('a', [Sound('a')]),
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛj')]),
    ('b', [Sound('b')]),
    ('bb', [Sound('b')]),
    ('c', [Sound('k')]),
    ('c', []),
    ('cc', [Sound('k')]),
    ('d', [Sound('d')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('f', [Sound('f')]),
    ('g', [Sound('g')]),
    ('h', [Sound('h')]),
    ('h', []),
    ('i', [Sound('ə')]),
    ('i', [Sound('ɪ')]),
    ('j', [Sound('ʤ')]),
    ('k', [Sound('k')]),
    ('l', [Sound('l')]),
    ('m', [Sound('m')]),
    ('n', [Sound('n')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('ou', [Sound('aw')]),
    ('p', [Sound('p')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('s', [Sound('s')]),
    ('sh', [Sound('ʃ')]),
    ('t', [Sound('t')]),
    ('u', [Sound('ʌ')]),
    ('v', [Sound('v')]),
    ('w', [Sound('w')]),
    ('x', [Sound('k'), Sound('s')]),
    ('y', [Sound('j')]),
    ('y', [Sound('ɪj')]),
    ('z', [Sound('z')]),
]

def link(word, pron):
    sounds = list(map(Sound.from_ipa, pron.split()))
    try:
        pairs = next(pair(word, sounds))
    except StopIteration:
        raise ValueError(f'Failed to link "{word}" to "{pron}"')
    for spell, sequence in pairs:
        if not sequence:
            yield Sound('', spelled=spell)
        else:
            for i, sound in enumerate(sequence):
                if not i:
                    sound.spelled = spell
                    sound.cont = False
                else:
                    sound.cont = True
                yield sound

def pair(word, sounds, pairs=[]):
    if not word and not sounds:
        yield pairs
        return
    for spell, pattern in PAIRS:
        sequence = sounds[:len(pattern)]
        if word.startswith(spell) and pattern == sequence:
            yield from pair(
                word  [len(spell)  :],
                sounds[len(pattern):],
                pairs + [(spell, sequence)]
            )

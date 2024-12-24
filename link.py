from sound import Sound

PAIRS = [
    ('bb', [Sound('b')]),
    ('cc', [Sound('k')]),
    ('dd', [Sound('d')]),
    ('ff', [Sound('f')]),
    ('gg', [Sound('g')]),
    ('kk', [Sound('k')]),
    ('ll', [Sound('l')]),
    ('mm', [Sound('m')]),
    ('nn', [Sound('n')]),
    ('pp', [Sound('p')]),
    ('rr', [Sound('r')]),
    ('ss', [Sound('s')]),
    ('tt', [Sound('t')]),
    ('vv', [Sound('v')]),
    ('zz', [Sound('z')]),

    ('a', [Sound('a')]),
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛj')]),
    ('b', [Sound('b')]),
    ('c', [Sound('k')]),
    ('c', [Sound('s')]),
    ('c', []),
    ('d', [Sound('d')]),
    ('e', [Sound('ə')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('e', []),
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
    ('o', [Sound('ɔ')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('o', [Sound('ʌ')]),
    ('oa', [Sound('oː')]),
    ('ou', [Sound('aw')]),
    ('p', [Sound('p')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('s', [Sound('s')]),
    ('sh', [Sound('ʃ')]),
    ('t', [Sound('t')]),
    ('ti', [Sound('ʃ')]),
    ('u', [Sound('ə')]),
    ('u', [Sound('ʉw')]),
    ('u', [Sound('ʌ')]),
    ('v', [Sound('v')]),
    ('w', [Sound('w')]),
    ('x', [Sound('k'), Sound('s')]),
    ('y', [Sound('j')]),
    ('y', [Sound('ɪj')]),
    ('z', [Sound('z')]),

    ('', [Sound('.')]),
    ('', [Sound('ə')]),
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

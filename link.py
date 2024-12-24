from sound import Sound

PAIRS = [
    ('a', [Sound('a')]),
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛj')]),
    ('b', [Sound('b')]),
    ('bb', [Sound('b')]),
    ('c', [Sound('k')]),
    ('c', [Sound('s')]),
    ('c', []),
    ('cc', [Sound('k')]),
    ('d', [Sound('d')]),
    ('dd', [Sound('d')]),
    ('e', [Sound('ə')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('e', []),
    ('f', [Sound('f')]),
    ('ff', [Sound('f')]),
    ('g', [Sound('g')]),
    ('gg', [Sound('g')]),
    ('h', [Sound('h')]),
    ('h', []),
    ('i', [Sound('ə')]),
    ('i', [Sound('ɪ')]),
    ('j', [Sound('ʤ')]),
    ('k', [Sound('k')]),
    ('kk', [Sound('k')]),
    ('l', [Sound('l')]),
    ('ll', [Sound('l')]),
    ('m', [Sound('m')]),
    ('mm', [Sound('m')]),
    ('n', [Sound('n')]),
    ('nn', [Sound('n')]),
    ('o', [Sound('ɔ')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('o', [Sound('ʌ')]),
    ('oa', [Sound('oː')]),
    ('ou', [Sound('aw')]),
    ('p', [Sound('p')]),
    ('pp', [Sound('p')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('rr', [Sound('r')]),
    ('s', [Sound('s')]),
    ('sh', [Sound('ʃ')]),
    ('ss', [Sound('s')]),
    ('t', [Sound('t')]),
    ('ti', [Sound('ʃ')]),
    ('tt', [Sound('t')]),
    ('u', [Sound('ə')]),
    ('u', [Sound('ʉw')]),
    ('u', [Sound('ʌ')]),
    ('v', [Sound('v')]),
    ('vv', [Sound('v')]),
    ('w', [Sound('w')]),
    ('x', [Sound('k'), Sound('s')]),
    ('y', [Sound('j')]),
    ('y', [Sound('ɪj')]),
    ('z', [Sound('z')]),
    ('zz', [Sound('z')]),
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

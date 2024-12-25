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
    ('a', [Sound('ɑː')]),
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛj')]),
    ('a', [Sound('ɪ')]),
    ('b', [Sound('b')]),
    ('c', [Sound('k')]),
    ('c', [Sound('s')]),
    ('ch', [Sound('tʃ')]),
    ('d', [Sound('d')]),
    ('dg', [Sound('dʒ')]),
    ('e', [Sound('ə')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('f', [Sound('f')]),
    ('g', [Sound('dʒ')]),
    ('g', [Sound('g')]),
    ('h', [Sound('h')]),
    ('i', [Sound('ɑj')]),
    ('i', [Sound('ə')]),
    ('i', [Sound('ɪ')]),
    ('ie', [Sound('ɪj')]),
    ('j', [Sound('dʒ')]),
    ('k', [Sound('k')]),
    ('l', [Sound('l')]),
    ('m', [Sound('m')]),
    ('n', [Sound('n')]),
    ('ng', [Sound('ŋ')]),
    ('o', [Sound('ɔ')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('o', [Sound('ʌ')]),
    ('oa', [Sound('oː')]),
    ('ou', [Sound('aw')]),
    ('ow', [Sound('ɔ')]), # kn[ow]ledge
    ('p', [Sound('p')]),
    ('q', [Sound('k')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('s', [Sound('s')]),
    ('s', [Sound('z')]),
    ('sh', [Sound('ʃ')]),
    ('t', [Sound('t')]),
    ('t', [Sound('tʃ')]),
    ('ti', [Sound('ʃ')]),
    ('u', [Sound('w')]),
    ('u', [Sound('ə')]),
    ('u', [Sound('ʉw')]),
    ('u', [Sound('ʌ')]),
    ('v', [Sound('v')]),
    ('w', [Sound('w')]),
    ('x', [Sound('k'), Sound('s')]),
    ('y', [Sound('j')]),
    ('y', [Sound('ɪj')]),
    ('z', [Sound('z')]),

    ('air', [Sound('ɛː')]),
    ('er', [Sound('əː')]),

    ('ed', [Sound('t')]),

    ('', [Sound('.')]),
    ('', [Sound('j')]), # b[]eauty
    ('', [Sound('ə')]), # simp[]le

    ('c', []), # ba[c]k
    ('e', []), # fac[e]
    ('h', []), # [h]our
    ('r', []), # pa[r]t
    ('u', []), # act[u]ally
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

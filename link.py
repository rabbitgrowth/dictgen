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

    ('ow', [Sound('ɔ')]), # "kn[ow]ledge"

    ('a', [Sound('a')]),
    ('a', [Sound('oː')]), # "[a]ll"
    ('a', [Sound('ɔ')]), # "[a]lter"
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛj')]),
    ('a', [Sound('ɪ')]),
    ('ai', [Sound('ɛ')]), # "ag[ai]n"
    ('ai', [Sound('ɛj')]),
    ('ay', [Sound('ɛj')]),
    ('b', [Sound('b')]),
    ('c', [Sound('k')]),
    ('c', [Sound('s')]),
    ('ch', [Sound('tʃ')]),
    ('ci', [Sound('ʃ')]), # "spe[ci]al"
    ('d', [Sound('d')]),
    ('d', [Sound('t')]), # "face[d]"
    ('dg', [Sound('dʒ')]),
    ('e', [Sound('ə')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('ea', [Sound('ɛ')]),
    ('ee', [Sound('ɪj')]),
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
    ('n', [Sound('ŋ')]), # "a[n]ger"
    ('ng', [Sound('ŋ')]),
    ('o', [Sound('ɔ')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('o', [Sound('ʌ')]), # "l[o]ve"
    ('oa', [Sound('oː')]),
    ('oo', [Sound('ʉw')]),
    ('ou', [Sound('aw')]),
    ('ou', [Sound('ə')]), # "fam[ou]s"
    ('ou', [Sound('əw')]), # "s[ou]l"
    ('ow', [Sound('aw')]),
    ('oy', [Sound('oj')]),
    ('p', [Sound('p')]),
    ('q', [Sound('k')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('s', [Sound('s')]),
    ('s', [Sound('z')]),
    ('sh', [Sound('ʃ')]),
    ('t', [Sound('t')]),
    ('t', [Sound('tʃ')]),
    ('th', [Sound('ð')]),
    ('th', [Sound('θ')]),
    ('ti', [Sound('ʃ')]), # "ac[ti]on"
    ('u', [Sound('w')]),
    ('u', [Sound('ə')]),
    ('u', [Sound('ʉw')]),
    ('u', [Sound('ʌ')]),
    ('v', [Sound('v')]),
    ('w', [Sound('w')]),
    ('x', [Sound('k'), Sound('s')]),
    ('y', [Sound('j')]),
    ('y', [Sound('ɑj')]),
    ('y', [Sound('ə')]), # "anal[y]sis"
    ('y', [Sound('ɪj')]),
    ('z', [Sound('z')]),

    # Don't analyze <r> as part of a vowel even though that might make
    # more sense in cases like <ur> /əː/. This ensures that <r> can
    # consistently be matched as a standalone silent letter and that
    # no extra rules are needed for when the <r> is pronounced:
    # d ai r y
    # d ɛ́ː r ɪj
    ('a', [Sound('ɑː')]),
    ('ai', [Sound('ɛː')]),
    ('e', [Sound('əː')]),
    ('o', [Sound('oː')]),
    ('r', []),

    ('c', []), # "ba[c]k"
    ('e', []), # "fac[e]"
    ('gh', []), # "thou[gh]"
    ('h', []), # "[h]our"
    ('w', []), # "s[w]ord"

    ('', [Sound('.')]),
    ('', [Sound('j')]), # "b[]eauty"
    ('', [Sound('ə')]), # "simp[]le"
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

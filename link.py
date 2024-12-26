from sound import Sound

PAIRS = [
    # Order matters here; what is listed first gets matched first.

    ('ai', [Sound('ɛ')]), # "ag[ai]n"
    ('ai', [Sound('ɛj')]),
    ('ay', [Sound('ɛj')]),
    ('ch', [Sound('tʃ')]),
    ('dg', [Sound('dʒ')]),
    ('ea', [Sound('ɛ')]),
    ('ea', [Sound('ɪj')]),
    ('ee', [Sound('ɪj')]),
    ('ie', [Sound('ɪj')]),
    ('ng', [Sound('ŋ')]),
    ('oa', [Sound('oː')]), # "br[oa]d"
    ('oa', [Sound('əw')]),
    ('oi', [Sound('oj')]),
    ('oo', [Sound('ʉw')]),
    ('ou', [Sound('aw')]),
    ('ou', [Sound('ə')]), # "fam[ou]s"
    ('ou', [Sound('əw')]), # "s[ou]l"
    ('ow', [Sound('aw')]),
    ('ow', [Sound('ɔ')]), # "kn[ow]ledge"; not <o> /ɔ/, <w> /∅/
    ('oy', [Sound('oj')]),
    ('sh', [Sound('ʃ')]),
    ('th', [Sound('ð')]),
    ('th', [Sound('θ')]),

    ('ci', [Sound('ʃ')]), # "spe[ci]al"
    ('ti', [Sound('ʃ')]), # "ac[ti]on"
    ('xi', [Sound('k'), Sound('ʃ')]), # "an[xi]ous"

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
    ('a', [Sound('oː')]), # "[a]ll"
    ('a', [Sound('ɔ')]), # "[a]lter"
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛ')]), # "[a]ny"
    ('a', [Sound('ɛj')]),
    ('a', [Sound('ɪ')]),
    ('b', [Sound('b')]),
    ('c', [Sound('k')]),
    ('c', [Sound('s')]),
    ('c', [Sound('ʃ')]), # "appre[c]iate"
    ('d', [Sound('d')]),
    ('d', [Sound('t')]), # "face[d]"
    ('e', [Sound('ə')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('e', [Sound('ɪj')]),
    ('f', [Sound('f')]),
    ('g', [Sound('dʒ')]),
    ('g', [Sound('g')]),
    ('h', [Sound('h')]),
    ('i', [Sound('ɑj')]),
    ('i', [Sound('ə')]),
    ('i', [Sound('ɪ')]),
    ('i', [Sound('ɪj')]),
    ('j', [Sound('dʒ')]),
    ('k', [Sound('k')]),
    ('l', [Sound('l')]),
    ('m', [Sound('m')]),
    ('n', [Sound('n')]),
    ('n', [Sound('ŋ')]), # "a[n]ger"
    ('o', [Sound('w'), Sound('ʌ')]), # "[o]ne"
    ('o', [Sound('ɔ')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('o', [Sound('ʉw')]), # "pr[o]ve"
    ('o', [Sound('ʌ')]), # "l[o]ve"
    ('p', [Sound('p')]),
    ('q', [Sound('k')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('s', [Sound('s')]),
    ('s', [Sound('z')]),
    ('t', [Sound('t')]),
    ('t', [Sound('tʃ')]),
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
    ('e', [Sound('ɛː')]),
    ('ea', [Sound('ɪː')]),
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
            yield Sound('', stressed=False, spelled=spell, cont=False)
        else:
            for i, sound in enumerate(sequence):
                if not i:
                    sound.spelled = spell
                    sound.cont = False
                else:
                    sound.spelled = ''
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

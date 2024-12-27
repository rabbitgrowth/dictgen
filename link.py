from sound import Sound

PAIRS = [
    # Order matters here; what is listed first gets matched first.

    # <k n ow l e dg e> not <k n o w l e dg e>
    # /  n ɔ́  l ɪ dʒ  /     /  n ɔ́   l ɪ dʒ  /
    ('ow', [Sound('ɔ')]),

    ('ai', [Sound('ɛ')]), # "ag[ai]n"
    ('ai', [Sound('ɛj')]),
    ('ay', [Sound('ɛj')]),
    ('ch', [Sound('k')]),
    ('ch', [Sound('tʃ')]),
    ('dg', [Sound('dʒ')]),
    ('ea', [Sound('ɛ')]),
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
    ('oy', [Sound('oj')]),
    ('sh', [Sound('ʃ')]),
    ('th', [Sound('ð')]),
    ('th', [Sound('θ')]),
    ('ue', [Sound('ʉw')]),

    ('ci', [Sound('ʃ')]), # "spe[ci]al"
    ('ti', [Sound('ʃ')]), # "ac[ti]on"
    ('xi', [Sound('k'), Sound('ʃ')]), # "an[xi]ous"

    # Consonant doubling
    # <a cc ou n t> not <a c c ou n t>
    # /ə k  áw n t/ not /ə k   áw n t/
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
    ('a', [Sound('ɛː')]), # "[a]rea"
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

    # <a  r e  a> not <a  r ea  >
    # /ɛ́ː r ɪj ə/     /ɛ́ː r ɪj ə/
    ('ea', [Sound('ɪj')]),

    # Non-rhoticity
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
    ('k', []), # "[k]now"
    ('w', []), # "s[w]ord"

    ('', [Sound('.')]),
    ('', [Sound('j')]), # "b[]eauty"
    ('', [Sound('ə')]), # "simp[]le"
]

def link(word, ipa):
    pron = list(map(Sound.from_ipa, ipa.split()))
    try:
        pairs = next(pair(word, pron))
    except StopIteration:
        raise ValueError(f'Failed to link "{word}" to "{ipa}"')
    for spell, sounds in pairs:
        if not sounds:
            yield Sound('', stressed=False, spelled=spell, cont=False)
        else:
            for i, sound in enumerate(sounds):
                if not i:
                    sound.spelled = spell
                    sound.cont = False
                else:
                    sound.spelled = ''
                    sound.cont = True
                yield sound

def pair(word, pron, pairs=[]):
    if not word and not pron:
        yield pairs
        return
    for spell, sounds in PAIRS:
        if word.lower().startswith(spell) and sounds == pron[:len(sounds)]:
            yield from pair(
                word[len(spell) :],
                pron[len(sounds):],
                pairs + [(
                    word[:len(spell) ],
                    pron[:len(sounds)]
                )]
            )

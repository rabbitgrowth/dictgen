from collections import defaultdict

from sound import Sound

PAIRS = [
    # <b a c k> not <b a c k>
    # /b á   k/     /b á k  /
    ('c', []),
    ('c', [Sound('k')]),

    ('a', [Sound('a')]),
    ('a', [Sound('oː')]), # "[a]ll"
    ('a', [Sound('ɔ')]), # "[a]lter"
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛ')]), # "[a]ny"
    ('a', [Sound('ɛj')]),
    ('a', [Sound('ɛː')]), # "[a]rea"
    ('a', [Sound('ɪ')]),
    ('ai', [Sound('ɛ')]), # "ag[ai]n"
    ('ai', [Sound('ɛj')]),
    ('au', [Sound('oː')]),
    ('au', [Sound('ɑː')]),
    ('au', [Sound('ɔ')]), # "bec[au]se"
    ('au', [Sound('ə')]), # "bec[au]se"
    ('ay', [Sound('ɛj')]),
    ('b', [Sound('b')]),
    ('bb', [Sound('b')]),
    ('c', [Sound('s')]),
    ('c', [Sound('ʃ')]), # "appre[c]iate"
    ('cc', [Sound('k')]),
    ('ch', [Sound('k')]),
    ('ch', [Sound('tʃ')]),
    ('ci', [Sound('ʃ')]), # "spe[ci]al"
    ('d', [Sound('d')]),
    ('d', [Sound('t')]), # "face[d]"
    ('dd', [Sound('d')]),
    ('dg', [Sound('dʒ')]),
    ('e', [Sound('ə')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('e', [Sound('ɪj')]),
    ('ea', [Sound('ɛ')]),
    ('ea', [Sound('ɪj')]),
    ('eau', [Sound('ʉw')]), # "b[eau]ty"
    ('ee', [Sound('ɪj')]),
    ('f', [Sound('f')]),
    ('ff', [Sound('f')]),
    ('g', [Sound('dʒ')]),
    ('g', [Sound('g')]),
    ('gg', [Sound('g')]),
    ('h', [Sound('h')]),
    ('i', [Sound('j')]), # "bill[i]on"
    ('i', [Sound('ɑj')]),
    ('i', [Sound('ə')]),
    ('i', [Sound('ɪ')]),
    ('i', [Sound('ɪj')]),
    ('ie', [Sound('ɪj')]),
    ('j', [Sound('dʒ')]),
    ('k', [Sound('k')]),
    ('kk', [Sound('k')]),
    ('l', [Sound('l')]),
    ('ll', [Sound('l')]),
    ('m', [Sound('m')]),
    ('mm', [Sound('m')]),
    ('n', [Sound('n')]),
    ('n', [Sound('ŋ')]), # "ba[n]k"
    ('ng', [Sound('ŋ')]),
    ('nn', [Sound('n')]),
    ('o', [Sound('w'), Sound('ʌ')]), # "[o]ne"
    ('o', [Sound('ɔ')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('o', [Sound('ʉw')]), # "pr[o]ve"
    ('o', [Sound('ʌ')]), # "l[o]ve"
    ('oa', [Sound('oː')]), # "br[oa]d"
    ('oa', [Sound('əw')]),
    ('oi', [Sound('oj')]),
    ('oo', [Sound('ʉw')]),
    ('oo', [Sound('ʌ')]),
    ('ou', [Sound('aw')]),
    ('ou', [Sound('ə')]), # "fam[ou]s"
    ('ou', [Sound('əw')]), # "s[ou]l"
    ('ow', [Sound('aw')]),
    ('ow', [Sound('ɔ')]),
    ('oy', [Sound('oj')]),
    ('p', [Sound('p')]),
    ('ph', [Sound('f')]),
    ('pp', [Sound('p')]),
    ('q', [Sound('k')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('rr', [Sound('r')]),
    ('s', [Sound('s')]),
    ('s', [Sound('z')]),
    ('sh', [Sound('ʃ')]),
    ('ss', [Sound('s')]),
    ('t', [Sound('t')]),
    ('t', [Sound('tʃ')]), # "atti[t]ude"
    ('th', [Sound('ð')]),
    ('th', [Sound('θ')]),
    ('ti', [Sound('ʃ')]), # "ac[ti]on"
    ('tt', [Sound('t')]),
    ('u', [Sound('w')]),
    ('u', [Sound('ə')]),
    ('u', [Sound('ʉw')]),
    ('u', [Sound('ʌ')]),
    ('ue', [Sound('ʉw')]),
    ('v', [Sound('v')]),
    ('vv', [Sound('v')]),
    ('w', [Sound('w')]),
    ('x', [Sound('k'), Sound('s')]),
    ('xi', [Sound('k'), Sound('ʃ')]), # "an[xi]ous"
    ('y', [Sound('j')]),
    ('y', [Sound('ɑj')]),
    ('y', [Sound('ə')]), # "anal[y]sis"
    ('y', [Sound('ɪ')]),
    ('y', [Sound('ɪj')]),
    ('z', [Sound('z')]),
    ('zz', [Sound('z')]),

    # Non-rhoticity
    # Don't analyze <r> as part of a vowel even though that might make
    # more sense in cases like <ur> /əː/. This ensures that <r> can
    # consistently be matched as a standalone silent letter and that
    # no extra rules are needed for when the <r> is pronounced:
    # <d ai r y >
    # /d ɛ́ː r ɪj/
    ('a', [Sound('ɑː')]),
    ('ai', [Sound('ɛː')]),
    ('e', [Sound('əː')]),
    ('e', [Sound('ɛː')]),
    ('e', [Sound('ɪː')]),
    ('ea', [Sound('ɛː')]),
    ('ea', [Sound('ɪː')]),
    ('ee', [Sound('ɪː')]),
    ('i', [Sound('əː')]),
    ('o', [Sound('oː')]),
    ('r', []),

    ('a', []), # "basic[a]lly"
    ('e', []), # "fac[e]"
    ('g', []), # "si[g]n"
    ('gh', []), # "thou[gh]"
    ('h', []), # "[h]our"
    ('k', []), # "[k]now"
    ('n', []), # "autum[n]"
    ('u', []), # "act[u]ally"
    ('w', []), # "s[w]ord"
    ('y', []), # "be[y]ond"

    ('', [Sound('.')]),
    ('', [Sound('j')]), # "b[]eauty"
    ('', [Sound('ə')]), # "simp[]le"
]

def link(word, ipa):
    pron = list(map(Sound.from_ipa, ipa.split()))
    scores = defaultdict(list)
    for pairs, score in pair(word, pron):
        scores[score].append(pairs)
    if not scores:
        raise ValueError(f'Failed to link "{word}" to "{ipa}"')
    pairs = scores[min(scores)][0]
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

def pair(word, pron, pairs=[], score=0):
    if not word and not pron:
        yield pairs, score
        return
    for spell, sounds in PAIRS:
        # Penalize unspelled sounds and silent letters to avoid
        # incorrect "lazy" pairings:
        # <a  r e  a> not <a  r ea  >
        # /ɛ́ː r ɪj ə/     /ɛ́ː r ɪj ə/
        # <a cc ou n t> not <a c c ou n t>
        # /ə k  áw n t/     /ə k   áw n t/
        # <k n ow l e dg e> not <k n o w l e dg e>
        # /  n ɔ́  l ɪ dʒ  /     /  n ɔ́   l ɪ dʒ  /
        penalty = (not spell) + (not sounds)
        if word.lower().startswith(spell) and sounds == pron[:len(sounds)]:
            yield from pair(
                word[len(spell) :],
                pron[len(sounds):],
                pairs + [(
                    word[:len(spell) ],
                    pron[:len(sounds)]
                )],
                score + penalty
            )

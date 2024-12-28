from math import inf

from sound import Sound
from trie import Trie

PAIRS = Trie([
    # <b a c k> not <b a c k>
    # /b á   k/     /b á k  /
    ('c', []),
    ('c', [Sound('k')]),

    # <n a  t  u r e> not <n a  t  u r e>
    # /n ɛ́j tʃ ə    /     /n ɛ́j tʃ   ə  /
    # <b u i l d> not <b u i l d>
    # /b   ɪ́ l d/     /b ɪ́   l d/
    ('u', [Sound('ə')]),
    ('u', []),
    ('u', [Sound('ɪ')]), # "b[u]sy"

    ('a', [Sound('a')]),
    ('a', [Sound('oː')]), # "[a]ll"
    ('a', [Sound('ɑː')]),
    ('a', [Sound('ɔ')]), # "[a]lter"
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛ')]), # "[a]ny"
    ('a', [Sound('ɛj')]),
    ('a', [Sound('ɛː')]), # "[a]rea"
    ('a', [Sound('ɪ')]),
    ('ai', [Sound('ə')]), # "cert[ai]n"
    ('ai', [Sound('ɛ')]), # "ag[ai]n"
    ('ai', [Sound('ɛj')]),
    ('ai', [Sound('ɛː')]),
    ('ai', [Sound('ɪ')]), # "capt[ai]n"
    ('au', [Sound('oː')]),
    ('au', [Sound('ɑː')]),
    ('au', [Sound('ɔ')]), # "bec[au]se"
    ('au', [Sound('ə')]), # "bec[au]se"
    ('aw', [Sound('oː')]),
    ('ay', [Sound('ɛj')]),
    ('b', [Sound('b')]),
    ('bb', [Sound('b')]),
    ('c', [Sound('s')]),
    ('c', [Sound('ʃ')]), # "appre[c]iate"
    ('cc', [Sound('k')]),
    ('ch', [Sound('k')]),
    ('ch', [Sound('tʃ')]),
    ('ch', [Sound('ʃ')]),
    ('ci', [Sound('ʃ')]), # "spe[ci]al"
    ('d', [Sound('d')]),
    ('d', [Sound('dʒ')]), # "[d]ue"
    ('d', [Sound('t')]), # "face[d]"
    ('dd', [Sound('d')]),
    ('dg', [Sound('dʒ')]),
    ('e', [Sound('ə')]),
    ('e', [Sound('əː')]), # "conc[e]rn"
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɛː')]),
    ('e', [Sound('ɪ')]),
    ('e', [Sound('ɪj')]),
    ('e', [Sound('ɪː')]),
    ('ea', [Sound('əː')]), # "[ea]rn"
    ('ea', [Sound('ɛ')]),
    ('ea', [Sound('ɛː')]),
    ('ea', [Sound('ɪj')]),
    ('ea', [Sound('ɪː')]),
    ('eau', [Sound('ʉw')]), # "b[eau]ty"
    ('ee', [Sound('ɪj')]),
    ('ee', [Sound('ɪː')]),
    ('ei', [Sound('ɑj')]), # "[ei]ther"
    ('ei', [Sound('ɛj')]), # "[ei]ght"
    ('ei', [Sound('ɪj')]),
    ('eu', [Sound('ɵː')]), # "[eu]ro"
    ('ew', [Sound('ʉw')]),
    ('f', [Sound('f')]),
    ('ff', [Sound('f')]),
    ('g', [Sound('dʒ')]),
    ('g', [Sound('g')]),
    ('gg', [Sound('g')]),
    ('gh', [Sound('f')]),
    ('h', [Sound('h')]),
    ('i', [Sound('j')]), # "bill[i]on"
    ('i', [Sound('ɑj')]),
    ('i', [Sound('ə')]),
    ('i', [Sound('əː')]), # "b[i]rd"
    ('i', [Sound('ɪ')]),
    ('i', [Sound('ɪj')]),
    ('ie', [Sound('ɑj')]),
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
    ('o', [Sound('oː')]),
    ('o', [Sound('w'), Sound('ʌ')]), # "[o]ne"
    ('o', [Sound('ɔ')]),
    ('o', [Sound('ə')]),
    ('o', [Sound('əw')]),
    ('o', [Sound('ʉw')]), # "pr[o]ve"
    ('o', [Sound('ʌ')]), # "l[o]ve"
    ('oa', [Sound('oː')]), # "br[oa]d"
    ('oa', [Sound('ə')]), # "cupb[oa]rd"
    ('oa', [Sound('əw')]),
    ('oi', [Sound('oj')]),
    ('oo', [Sound('oː')]), # "d[oo]r"
    ('oo', [Sound('ɵ')]),
    ('oo', [Sound('ʉw')]),
    ('oo', [Sound('ʌ')]),
    ('ou', [Sound('aw')]),
    ('ou', [Sound('oː')]), # "t[ou]r"
    ('ou', [Sound('ə')]), # "fam[ou]s"
    ('ou', [Sound('əw')]), # "s[ou]l"
    ('ou', [Sound('ɵ')]), # "sh[ou]ld"
    ('ou', [Sound('ʌ')]), # "en[ou]gh"
    ('ow', [Sound('aw')]),
    ('ow', [Sound('ɔ')]),
    ('ow', [Sound('əw')]),
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
    ('s', [Sound('ʃ')]), # "[s]ure"
    ('sci', [Sound('ʃ')]),
    ('sh', [Sound('ʃ')]),
    ('si', [Sound('ʒ')]),
    ('ss', [Sound('s')]),
    ('ssi', [Sound('ʃ')]),
    ('t', [Sound('t')]),
    ('t', [Sound('tʃ')]), # "atti[t]ude"
    ('tch', [Sound('tʃ')]),
    ('th', [Sound('ð')]),
    ('th', [Sound('θ')]),
    ('ti', [Sound('ʃ')]), # "ac[ti]on"
    ('tt', [Sound('t')]),
    ('u', [Sound('oː')]), # "c[u]re"
    ('u', [Sound('w')]),
    ('u', [Sound('əː')]), # "t[u]rn"
    ('u', [Sound('ɛ')]), # "b[u]ry"
    ('u', [Sound('ɵ')]),
    ('u', [Sound('ɵː')]), # "d[u]ring"
    ('u', [Sound('ʉw')]),
    ('u', [Sound('ʌ')]),
    ('ue', [Sound('ʉw')]),
    ('v', [Sound('v')]),
    ('vv', [Sound('v')]),
    ('w', [Sound('w')]),
    ('x', [Sound('g'), Sound('z')]), # "e[x]act"
    ('x', [Sound('k'), Sound('s')]),
    ('xi', [Sound('k'), Sound('ʃ')]), # "an[xi]ous"
    ('y', [Sound('j')]),
    ('y', [Sound('ɑj')]),
    ('y', [Sound('ə')]), # "anal[y]sis"
    ('y', [Sound('ɪ')]),
    ('y', [Sound('ɪj')]),
    ('z', [Sound('z')]),
    ('zz', [Sound('z')]),

    # Silent letters
    # Don't analyze <r> as part of a vowel even though that might make
    # more sense in cases like <ur> /əː/. This ensures that <r> can
    # consistently be matched as a standalone silent letter and that
    # no extra rules are needed for when the <r> is pronounced:
    # <d ai r y >
    # /d ɛ́ː r ɪj/
    ('a', []), # "basic[a]lly"
    ('b', []), # "bom[b]"
    ('e', []), # "fac[e]"
    ('g', []), # "si[g]n"
    ('h', []), # "[h]our"
    ('i', []), # "fr[i]end"
    ('k', []), # "[k]now"
    ('l', []), # "ca[l]m"
    ('n', []), # "autum[n]"
    ('o', []), # "choc[o]late"
    ('p', []), # "cu[p]board"
    ('r', []), # "pa[r]t"
    ('t', []), # "cas[t]le"
    ('u', []), # "b[u]ild"
    ('w', []), # "s[w]ord"
    ('y', []), # "be[y]ond"

    # Unspelled sounds
    ('', [Sound('.')]),
    ('', [Sound('j')]), # "b[]eauty"
    ('', [Sound('r')]), # "draw[]ing"
    ('', [Sound('ə')]), # "simp[]le"
])

def link(word, ipa):
    pron = list(map(Sound.from_ipa, ipa.split()))
    pairs = get_best_pairs(word, pron)
    if pairs is None:
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

def pair(word, pron, pairs=[], score=0, prev_length=None):
    if not word and not pron:
        yield pairs, score
        return
    for length, patterns in enumerate(PAIRS.lookup(word.lower())):
        for pattern in patterns:
            # Penalize unspelled sounds and silent letters to avoid
            # incorrect "lazy" pairings:
            # <a  r e  a> not <a  r ea  >
            # /ɛ́ː r ɪj ə/     /ɛ́ː r ɪj ə/
            # <a cc ou n t> not <a c c ou n t>
            # /ə k  áw n t/     /ə k   áw n t/
            # <k n ow l e dg e> not <k n o w l e dg e>
            # /  n ɔ́  l ɪ dʒ  /     /  n ɔ́   l ɪ dʒ  /
            # Additionally penalize an unspelled sound immediately
            # followed by a silent letter:
            # <c a  s t   l e> not <c a  s   t l e>
            # /k ɑ́ː s   ə l  /     /k ɑ́ː s ə   l  /
            penalty = (
                  (not length)
                + (not pattern)
                + (not prev_length and not pattern)
            )
            if pattern == pron[:len(pattern)]:
                yield from pair(
                    word[length:],
                    pron[len(pattern):],
                    pairs + [(word[:length], pron[:len(pattern)])],
                    score + penalty,
                    length
                )

def get_best_pairs(word, pron):
    best_pairs = None
    best_score = inf
    for pairs, score in pair(word, pron):
        if not score: # best possible score
            return pairs
        if score < best_score:
            best_pairs = pairs
            best_score = score
    return best_pairs

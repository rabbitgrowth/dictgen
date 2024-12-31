from math import inf

from sound import Sound
from trie import Trie

PAIRS = [
    ('a', [Sound('a')]),
    ('a', [Sound('oː')], 1), # "[a]ll"; not "extr[a]ordinary"
    ('a', [Sound('ɑː')]),
    ('a', [Sound('ɔ')]), # "[a]lter"
    ('a', [Sound('ə')]),
    ('a', [Sound('ɛ')]), # "[a]ny"
    ('a', [Sound('ɛj')]),
    ('a', [Sound('ɛː')]),
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
    ('awy', [Sound('oj')]), # "l[awy]er"
    ('ay', [Sound('ɛj')]),
    ('b', [Sound('b')]),
    ('bb', [Sound('b')]),
    ('c', [Sound('k')], 1), # "be[c]ome"; not "ba[c]k"
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
    ('e', [Sound('ɔ')], 1), # "g[e]nre"; not "g[e]ography"
    ('e', [Sound('ə')]),
    ('e', [Sound('əː')]),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɛː')]),
    ('e', [Sound('ɪ')]),
    ('e', [Sound('ɪj')]),
    ('e', [Sound('ɪː')]),
    ('ea', [Sound('ɑː')]), # "h[ea]rt"
    ('ea', [Sound('əː')]),
    ('ea', [Sound('ɛ')]),
    ('ea', [Sound('ɛj')]), # "gr[ea]t"
    ('ea', [Sound('ɛː')]),
    ('ea', [Sound('ɪj')]),
    ('ea', [Sound('ɪː')]),
    ('ea', [Sound('ɪː')]), # "id[ea]"
    ('eau', [Sound('ʉw')]), # "b[eau]ty"
    ('ee', [Sound('ɪj')]),
    ('ee', [Sound('ɪː')]),
    ('ei', [Sound('ɑj')]), # "[ei]ther"
    ('ei', [Sound('ə')]), # "for[ei]gn"
    ('ei', [Sound('ɛj')]), # "[ei]ght"
    ('ei', [Sound('ɪj')]),
    ('eu', [Sound('ɵː')]), # "[eu]ro"
    ('ew', [Sound('ʉw')]),
    ('ey', [Sound('ɑj')]), # "[ey]e"
    ('ey', [Sound('ɛj')]), # "gr[ey]"
    ('ey', [Sound('ɪj')]),
    ('f', [Sound('f')]),
    ('ff', [Sound('f')]),
    ('g', [Sound('dʒ')]),
    ('g', [Sound('g')]),
    ('g', [Sound('ʒ')]), # "[g]enre"
    ('gg', [Sound('g')]),
    ('gh', [Sound('f')]),
    ('h', [Sound('h')]),
    ('i', [Sound('j')]), # "bill[i]on"
    ('i', [Sound('ɑj')]),
    ('i', [Sound('ə')]),
    ('i', [Sound('əː')]),
    ('i', [Sound('ɪ')]),
    ('i', [Sound('ɪj')]),
    ('ie', [Sound('ɑj')]),
    ('ie', [Sound('ɛ')]), # "fr[ie]nd"
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
    ('o', [Sound('əː')]),
    ('o', [Sound('ʉw')]), # "pr[o]ve"
    ('o', [Sound('ʌ')]), # "l[o]ve"
    ('oa', [Sound('oː')]),
    ('oa', [Sound('oː')]), # "br[oa]d"
    ('oa', [Sound('ə')]), # "cupb[oa]rd"
    ('oa', [Sound('əw')]),
    ('oi', [Sound('oj')]),
    ('oo', [Sound('oː')]),
    ('oo', [Sound('ɵ')]),
    ('oo', [Sound('ʉw')]),
    ('oo', [Sound('ʌ')]),
    ('ou', [Sound('aw')]),
    ('ou', [Sound('oː')]),
    ('ou', [Sound('ə')]),
    ('ou', [Sound('ə')]), # "fam[ou]s"
    ('ou', [Sound('əw')]), # "s[ou]l"
    ('ou', [Sound('əː')]),
    ('ou', [Sound('ɵ')]), # "sh[ou]ld"
    ('ou', [Sound('ʉw')]), # "gr[ou]p"
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
    ('sci', [Sound('ʃ')]), # "con[sci]ous"
    ('sh', [Sound('ʃ')]),
    ('shi', [Sound('ʃ')]), # "fa[shi]on"
    ('si', [Sound('ʒ')]),
    ('ss', [Sound('s')]),
    ('ss', [Sound('ʃ')]), # "i[ss]ue"
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
    ('u', [Sound('ə')]),
    ('u', [Sound('əː')]),
    ('u', [Sound('ɛ')], 1), # "b[u]ry"; not "g[u]ess"
    ('u', [Sound('ɪ')], 1), # "b[u]sy"; not "b[u]ild"
    ('u', [Sound('ɵ')]),
    ('u', [Sound('ɵː')]), # "sec[u]re"
    ('u', [Sound('ʉw')]),
    ('u', [Sound('ʌ')]),
    ('ue', [Sound('ʉw')]),
    ('ui', [Sound('ʉw')]), # "fr[ui]t"
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
    ('a', []), # "basic[a]lly"
    ('b', []), # "bom[b]"
    ('c', []), # "ba[c]k"
    ('d', []), # "san[d]wich"
    ('e', []), # "mak[e]"
    ('g', []), # "si[g]n"
    ('h', []), # "[h]our"
    ('i', []), # "bus[i]ness"
    ('k', []), # "[k]now"
    ('l', []), # "ca[l]m"
    ('n', []), # "autum[n]"
    ('o', []), # "choc[o]late"
    ('p', []), # "cu[p]board"
    ('r', []), # "pa[r]t"
    ('s', []), # "i[s]land"
    ('t', []), # "cas[t]le"
    ('u', []), # "b[u]ild"
    ('w', []), # "s[w]ord"

    # Unspelled sounds
    ('', [Sound('.')]),
    ('', [Sound('j')]), # "b[]eauty"
    ('', [Sound('r')]), # "draw[]ing"
    ('', [Sound('ə')]), # "simp[]le"
]

TRIE = Trie()

for spell, *args in PAIRS:
    if len(args) == 1:
        sounds, = args
        rarity = 0
    else:
        sounds, rarity = args
    TRIE.insert(spell, (sounds, rarity))

def parse_ipa(ipa):
    return list(map(Sound.from_ipa, ipa.split()))

def link(word, ipa):
    pron = parse_ipa(ipa)
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

def pair(word, pron, pairs=[], score=0, prev_unspelled=False):
    if not word and not pron:
        yield pairs, score
        return
    for length, group in enumerate(TRIE.lookup(word.lower())):
        for sounds, rarity in group:
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
            unspelled = not length
            silent    = not sounds
            penalty = rarity + unspelled + silent + (prev_unspelled and silent)
            if sounds == pron[:len(sounds)]:
                yield from pair(
                    word[length:],
                    pron[len(sounds):],
                    pairs + [(word[:length], pron[:len(sounds)])],
                    score + penalty,
                    unspelled
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

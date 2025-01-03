from heapq import heappush, heappop

from sound import Sound
from trie import Trie

PATTERNS = [
    [('a', [Sound('a')])],
    [('a', [Sound('oː')])], # "[a]ll"; not "extr[a]ordinary"
    [('a', [Sound('ɑː')])],
    [('a', [Sound('ɔ')])], # "[a]lter"
    [('a', [Sound('ə')])],
    [('a', [Sound('ɛ')])], # "[a]ny"
    [('a', [Sound('ɛj')])],
    [('a', [Sound('ɛː')])], # "[a]rea", "aw[a]re"
    [('a', [Sound('ɪ')])],
    [('ai', [Sound('ə')])], # "cert[ai]n"
    [('ai', [Sound('ɛ')])], # "ag[ai]n"
    [('ai', [Sound('ɛj')])],
    [('ai', [Sound('ɛː')])],
    [('ai', [Sound('ɪ')])], # "capt[ai]n"
    [('au', [Sound('oː')])],
    [('au', [Sound('ɑː')])],
    [('au', [Sound('ɔ')])], # "bec[au]se"
    [('au', [Sound('ə')])], # "bec[au]se"
    [('aw', [Sound('oː')])],
    [('awy', [Sound('oj')])], # "l[awy]er"
    [('ay', [Sound('ɛj')])],
    [('b', [Sound('b')])],
    [('bb', [Sound('b')])],
    [('c', [Sound('k')])], # "be[c]ome"; not "ba[c]k"
    [('c', [Sound('s')])],
    [('c', [Sound('ʃ')])], # "appre[c]iate"
    [('cc', [Sound('k')])],
    [('ch', [Sound('k')])],
    [('ch', [Sound('tʃ')])],
    [('ch', [Sound('ʃ')])],
    [('ci', [Sound('ʃ')])], # "spe[ci]al"
    [('d', [Sound('d')])],
    [('d', [Sound('dʒ')])], # "[d]ue"
    [('d', [Sound('t')])], # "face[d]"
    [('dd', [Sound('d')])],
    [('dg', [Sound('dʒ')])],
    [('e', [Sound('ɔ')])], # "g[e]nre"; not "g[e]ography"
    [('e', [Sound('ə')])],
    [('e', [Sound('əː')])], # "conc[e]rn"
    [('e', [Sound('ɛ')])],
    [('e', [Sound('ɛː')])],
    [('e', [Sound('ɪ')])],
    [('e', [Sound('ɪj')])],
    [('e', [Sound('ɪː')])],
    [('ea', [Sound('ɑː')])], # "h[ea]rt"
    [('ea', [Sound('əː')])], # "[ea]rn"
    [('ea', [Sound('ɛ')])],
    [('ea', [Sound('ɛj')])], # "gr[ea]t"
    [('ea', [Sound('ɛː')])],
    [('ea', [Sound('ɪj')])],
    [('ea', [Sound('ɪː')])], # "id[ea]", "d[ea]r"
    [('eau', [Sound('ʉw')])], # "b[eau]ty"
    [('ee', [Sound('ɪj')])],
    [('ee', [Sound('ɪː')])],
    [('ei', [Sound('ɑj')])], # "[ei]ther"
    [('ei', [Sound('ə')])], # "for[ei]gn"
    [('ei', [Sound('ɛ')])], # "l[ei]sure"
    [('ei', [Sound('ɛj')])], # "[ei]ght"
    [('ei', [Sound('ɪj')])],
    [('eu', [Sound('ɵː')])], # "[eu]ro"
    [('ew', [Sound('ʉw')])],
    [('ey', [Sound('ɑj')])], # "[ey]e"
    [('ey', [Sound('ɛj')])], # "gr[ey]"
    [('ey', [Sound('ɪj')])],
    [('f', [Sound('f')])],
    [('ff', [Sound('f')])],
    [('g', [Sound('dʒ')])],
    [('g', [Sound('g')])],
    [('g', [Sound('ʒ')])], # "[g]enre"
    [('gg', [Sound('g')])],
    [('gh', [Sound('f')])],
    [('h', [Sound('h')])],
    [('i', [Sound('j')])], # "bill[i]on"
    [('i', [Sound('ɑj')])],
    [('i', [Sound('ə')])],
    [('i', [Sound('əː')])], # "b[i]rd"
    [('i', [Sound('ɪ')])],
    [('i', [Sound('ɪj')])],
    [('ie', [Sound('ɑj')])],
    [('ie', [Sound('ɛ')])], # "fr[ie]nd"
    [('ie', [Sound('ɪj')])],
    [('j', [Sound('dʒ')])],
    [('k', [Sound('k')])],
    [('kk', [Sound('k')])],
    [('l', [Sound('l')])],
    [('ll', [Sound('l')])],
    [('m', [Sound('m')])],
    [('mm', [Sound('m')])],
    [('n', [Sound('n')])],
    [('n', [Sound('ŋ')])], # "ba[n]k"
    [('ng', [Sound('ŋ')])],
    [('nn', [Sound('n')])],
    [('o', [Sound('oː')])], # "b[o]rn"
    [('o', [Sound('w'), Sound('ʌ')])], # "[o]ne"
    [('o', [Sound('ɔ')])],
    [('o', [Sound('ə')])],
    [('o', [Sound('əw')])],
    [('o', [Sound('əː')])], # "w[o]rse"
    [('o', [Sound('ʉw')])], # "pr[o]ve"
    [('o', [Sound('ʌ')])], # "l[o]ve"
    [('oa', [Sound('oː')])], # "br[oa]d", "b[oa]rd"
    [('oa', [Sound('ə')])], # "cupb[oa]rd"
    [('oa', [Sound('əw')])],
    [('oi', [Sound('oj')])],
    [('oo', [Sound('oː')])], # "d[oo]r"
    [('oo', [Sound('ɵ')])], # "f[oo]t"
    [('oo', [Sound('ʉw')])],
    [('oo', [Sound('ʌ')])], # "bl[oo]d"
    [('ou', [Sound('aw')])],
    [('ou', [Sound('oː')])], # "f[ou]r"
    [('ou', [Sound('ə')])], # "fam[ou]s", "fav[ou]r"
    [('ou', [Sound('əw')])], # "s[ou]l"
    [('ou', [Sound('əː')])], # "j[ou]rney"
    [('ou', [Sound('ɵ')])], # "sh[ou]ld"
    [('ou', [Sound('ʉw')])], # "gr[ou]p"
    [('ou', [Sound('ʌ')])], # "en[ou]gh"
    [('ow', [Sound('aw')])],
    [('ow', [Sound('ɔ')])],
    [('ow', [Sound('əw')])],
    [('oy', [Sound('oj')])],
    [('p', [Sound('p')])],
    [('ph', [Sound('f')])],
    [('pp', [Sound('p')])],
    [('q', [Sound('k')])],
    [('r', [Sound('r')])],
    [('r', [Sound('ə')])],
    [('rr', [Sound('r')])],
    [('s', [Sound('s')])],
    [('s', [Sound('z')])],
    [('s', [Sound('ʃ')])], # "[s]ure"
    [('s', [Sound('ʒ')])], # "lei[s]ure"
    [('sci', [Sound('ʃ')])], # "con[sci]ous"
    [('sh', [Sound('ʃ')])],
    [('shi', [Sound('ʃ')])], # "fa[shi]on"
    [('si', [Sound('ʒ')])],
    [('ss', [Sound('s')])],
    [('ss', [Sound('ʃ')])], # "i[ss]ue"
    [('ssi', [Sound('ʃ')])],
    [('t', [Sound('t')])],
    [('t', [Sound('tʃ')])], # "atti[t]ude"
    [('tch', [Sound('tʃ')])],
    [('th', [Sound('ð')])],
    [('th', [Sound('θ')])],
    [('ti', [Sound('ʃ')])], # "ac[ti]on"
    [('tt', [Sound('t')])],
    [('u', [Sound('oː')])], # "c[u]re"
    [('u', [Sound('w')])],
    [('u', [Sound('ə')])],
    [('u', [Sound('əː')])], # "t[u]rn"
    [('u', [Sound('ɛ')])], # "b[u]ry"; not "g[u]ess"
    [('u', [Sound('ɪ')])], # "b[u]sy"; not "b[u]ild"
    [('u', [Sound('ɵ')])],
    [('u', [Sound('ɵː')])], # "sec[u]re"
    [('u', [Sound('ʉw')])],
    [('u', [Sound('ʌ')])],
    [('ue', [Sound('ʉw')])],
    [('ui', [Sound('ʉw')])], # "fr[ui]t"
    [('v', [Sound('v')])],
    [('vv', [Sound('v')])],
    [('w', [Sound('w')])],
    [('x', [Sound('g'), Sound('z')])], # "e[x]act"
    [('x', [Sound('k'), Sound('s')])],
    [('xi', [Sound('k'), Sound('ʃ')])], # "an[xi]ous"
    [('y', [Sound('j')])],
    [('y', [Sound('ɑj')])],
    [('y', [Sound('ə')])], # "anal[y]sis"
    [('y', [Sound('ɪ')])],
    [('y', [Sound('ɪj')])],
    [('z', [Sound('z')])],
    [('zz', [Sound('z')])],
]

PENALIZED_PATTERNS = [
    # Silent letters
    [('a', [])], # "basic[a]lly"
    [('b', [])], # "bom[b]"
    [('c', [])], # "ba[c]k"
    [('d', [])], # "san[d]wich"
    [('e', [])], # "mak[e]"
    [('g', [])], # "si[g]n"
    [('h', [])], # "[h]our"
    [('i', [])], # "bus[i]ness"
    [('k', [])], # "[k]now"
    [('l', [])], # "ca[l]m"
    [('n', [])], # "autum[n]"
    [('o', [])], # "choc[o]late"
    [('p', [])], # "cu[p]board"
    [('r', [])], # "pa[r]t"
    [('s', [])], # "i[s]land"
    [('t', [])], # "cas[t]le"
    [('u', [])], # "b[u]ild"
    [('w', [])], # "s[w]ord"

    # Unspelled sounds
    [('', [Sound('.')])],
    [('', [Sound('j')])], # "b[]eauty"
    [('', [Sound('k')])], # "leng[]th"; not "ci[]rcle"
    [('', [Sound('r')])], # "draw[]ing"
    [('', [Sound('ə')])], # "simp[]le"
]

TRIE = Trie()

for patterns, penalty in [(PATTERNS, 0), (PENALIZED_PATTERNS, 1)]:
    for pattern in patterns:
        key = [char for spell, _ in pattern for char in spell]
        TRIE.insert(key, (pattern, penalty))

def parse_ipa(ipa):
    return list(map(Sound.from_ipa, ipa.split()))

def link(word, ipa):
    pron = parse_ipa(ipa)
    pairs = pair(word, pron)
    if pairs is None:
        raise ValueError(f'Failed to link <{word}> to /{ipa}/')
    for spell, sounds in pairs:
        if not sounds:
            sounds = [Sound.from_ipa('')]
        for i, sound in enumerate(sounds):
            if not i:
                sound.spelled = spell
                sound.cont = False
            else:
                sound.spelled = ''
                sound.cont = True
            yield sound


def pair(word, pron):
    count = 0
    queue = [(0, 0, word, pron, [])]
    while queue:
        score, _, word, pron, pairs = heappop(queue)
        if not word and not pron:
            return pairs
        for patterns in reversed(list(TRIE.lookup(word))):
            for pattern, penalty in patterns:
                count += 1
                result = match(word, pron, pairs, pattern)
                if result is not None:
                    heappush(queue, (score + penalty, count, *result))

def match(word, pron, pairs, pattern):
    matched = []
    for spell, sounds in pattern:
        word_head = word[:len(spell ) ]
        word_tail = word[ len(spell ):]
        pron_head = pron[:len(sounds) ]
        pron_tail = pron[ len(sounds):]
        if spell != word_head or sounds != pron_head:
            return None
        matched.append((word_head, pron_head))
        word = word_tail
        pron = pron_tail
    return word, pron, pairs + matched

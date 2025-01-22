from heapq import heappush, heappop

from sound import Sound
from trie import Trie

PATTERNS = [
    [('a', ['a'])],
    [('a', ['ɑː'])],
    [('a', ['ɔ'])], # "[a]lter"
    [('a', ['ə'])],
    [('a', ['ɛ'])], # "[a]ny"
    [('a', ['ɛj'])],
    [('a', ['ɛː'])], # "[a]rea"
    [('a', ['ɪ'])],
    [('ai', ['ə'])], # "cert[ai]n"
    [('ai', ['ɛ'])], # "ag[ai]n"
    [('ai', ['ɛj'])],
    [('ai', ['ɛː'])],
    [('ai', ['ɪ'])], # "capt[ai]n"
    [('au', ['oː'])],
    [('au', ['ɑː'])],
    [('au', ['ɔ'])], # "bec[au]se"
    [('au', ['ə'])], # "bec[au]se"
    [('aw', ['oː'])],
    [('ay', ['ɛj'])],
    [('b', ['b'])],
    [('c', ['s'])],
    [('c', ['ʃ'])], # "appre[c]iate"
    [('ch', ['dʒ'])], # "sandwi[ch]"
    [('ch', ['k'])],
    [('ch', ['tʃ'])],
    [('ch', ['ʃ'])],
    [('d', ['d'])],
    [('d', ['dʒ'])], # "[d]ue"
    [('d', ['t'])], # "face[d]"
    [('dg', ['dʒ'])],
    [('e', ['ə'])],
    [('e', ['əː'])], # "conc[e]rn"
    [('e', ['ɛ'])],
    [('e', ['ɛj'])], # "caf[e]"
    [('e', ['ɛː'])],
    [('e', ['ɪ'])],
    [('e', ['ɪj'])],
    [('e', ['ɪː'])],
    [('ea', ['ɑː'])], # "h[ea]rt"
    [('ea', ['əː'])], # "[ea]rn"
    [('ea', ['ɛ'])],
    [('ea', ['ɛj'])], # "gr[ea]t"
    [('ea', ['ɛː'])],
    [('ea', ['ɪj'])],
    [('ea', ['ɪː'])], # "id[ea]", "d[ea]r"
    [('eau', ['ʉw'])], # "b[eau]ty"
    [('ee', ['ɪj'])],
    [('ee', ['ɪː'])],
    [('ei', ['ɑj'])], # "[ei]ther"
    [('ei', ['ə'])], # "for[ei]gn"
    [('ei', ['ɛ'])], # "l[ei]sure"
    [('ei', ['ɛj'])], # "[ei]ght"
    [('ei', ['ɛː'])], # "th[ei]r"
    [('ei', ['ɪj'])],
    [('eo', ['ɪj'])], # "p[eo]ple"
    [('eu', ['ɵː'])], # "[eu]ro"
    [('ew', ['ʉw'])],
    [('ey', ['ɑj'])], # "[ey]e"
    [('ey', ['ɛj'])], # "gr[ey]"
    [('ey', ['ɪj'])],
    [('f', ['f'])],
    [('f', ['v'])], # "o[f]"
    [('g', ['dʒ'])],
    [('g', ['g'])],
    [('g', ['ʒ'])], # "[g]enre"
    [('gh', ['f'])],
    [('h', ['h'])],
    [('i', ['j'])], # "bill[i]on"
    [('i', ['ɑj'])],
    [('i', ['ə'])],
    [('i', ['əː'])], # "b[i]rd"
    [('i', ['ɪ'])],
    [('i', ['ɪj'])],
    [('ia', ['ə'])], # "parl[ia]ment"
    [('ia', ['ɪ'])], # "marr[ia]ge"
    [('ie', ['ɑj'])],
    [('ie', ['ɛ'])], # "fr[ie]nd"
    [('j', ['dʒ'])],
    [('k', ['k'])],
    [('l', ['l'])],
    [('m', ['m'])],
    [('n', ['n'])],
    [('n', ['ŋ'])], # "ba[n]k"
    [('ng', ['ŋ'])],
    [('o', ['oː'])], # "b[o]rn"
    [('o', ['w', 'ʌ'])], # "[o]ne"
    [('o', ['ɔ'])],
    [('o', ['ə'])],
    [('o', ['əw'])],
    [('o', ['əː'])], # "w[o]rse"
    [('o', ['ɵ'])], # "w[o]man"
    [('o', ['ʉw'])], # "pr[o]ve"
    [('o', ['ʌ'])], # "l[o]ve"
    [('oa', ['oː'])], # "br[oa]d", "b[oa]rd"
    [('oa', ['ə'])], # "cupb[oa]rd"
    [('oa', ['əw'])],
    [('oe', ['əw'])], # "t[oe]"
    [('oe', ['ʉw'])], # "sh[oe]"
    [('oi', ['oj'])],
    [('oo', ['oː'])], # "d[oo]r"
    [('oo', ['ɵ'])], # "f[oo]t"
    [('oo', ['ʉw'])],
    [('oo', ['ʌ'])], # "bl[oo]d"
    [('ou', ['aw'])],
    [('ou', ['oː'])], # "p[ou]r"
    [('ou', ['ɑː'])], # "[ou]r"
    [('ou', ['ə'])], # "fam[ou]s", "fav[ou]r"
    [('ou', ['əw'])], # "s[ou]l"
    [('ou', ['əː'])], # "j[ou]rney"
    [('ou', ['ɵ'])], # "sh[ou]ld"
    [('ou', ['ʉw'])], # "gr[ou]p"
    [('ou', ['ʌ'])], # "en[ou]gh"
    [('ow', ['aw'])],
    [('ow', ['ɔ'])],
    [('ow', ['əw'])],
    [('oy', ['oj'])],
    [('p', ['p'])],
    [('ph', ['f'])],
    [('q', ['k'])],
    [('r', ['r'])],
    [('s', ['s'])],
    [('s', ['z'])],
    [('s', ['ʃ'])], # "[s]ure"
    [('s', ['ʒ'])], # "lei[s]ure"
    [('sch', ['ʃ'])], # "[sch]edule"
    [('sh', ['ʃ'])],
    [('t', ['t'])],
    [('t', ['tʃ'])], # "atti[t]ude"
    [('tch', ['tʃ'])],
    [('th', ['ð'])],
    [('th', ['θ'])],
    [('u', ['oː'])], # "c[u]re"
    [('u', ['w'])],
    [('u', ['əː'])], # "t[u]rn"
    [('u', ['ɵ'])],
    [('u', ['ɵː'])], # "sec[u]re"
    [('u', ['ʉw'])],
    [('u', ['ʌ'])],
    [('ue', ['ʉw'])],
    [('ui', ['ʉw'])], # "fr[ui]t"
    [('v', ['v'])],
    [('w', ['w'])],
    [('x', ['g', 'z'])], # "e[x]act"
    [('x', ['k', 's'])],
    [('x', ['k', 'ʃ'])], # "lu[x]ury"
    [('y', ['j'])],
    [('y', ['ɑj'])],
    [('y', ['ə'])], # "anal[y]sis"
    [('y', ['ɪ'])],
    [('y', ['ɪj'])],
    [('z', ['z'])],

    [('bb', ['b'])],
    [('cc', ['k'])],
    [('dd', ['d'])],
    [('ff', ['f'])],
    [('gg', ['dʒ'])], # "su[gg]est"
    [('gg', ['g'])],
    [('kk', ['k'])],
    [('ll', ['l'])],
    [('mm', ['m'])],
    [('nn', ['n'])],
    [('pp', ['p'])],
    [('rr', ['r'])],
    [('ss', ['s'])],
    [('ss', ['z'])], # "po[ss]ess"
    [('ss', ['ʃ'])], # "i[ss]ue"
    [('tt', ['t'])],
    [('vv', ['v'])],
    [('zz', ['z'])],

    [('ci', ['ʃ'])], # "spe[ci]al"
    [('c', ['ʃ']), ('ie', ['ɪj'])], # "spe[cie]s"
    [('gi', ['dʒ'])], # "re[gi]on"
    [('sci', ['ʃ'])], # "con[sci]ous"
    [('shi', ['ʃ'])], # "fa[shi]on"
    [('si', ['ʃ'])], # "pen[si]on"
    [('si', ['ʒ'])], # "ver[si]on"
    [('ssi', ['ʃ'])], # "mi[ssi]on"
    [('ti', ['tʃ'])], # "ques[ti]on"
    [('ti', ['ʃ'])], # "ac[ti]on"
    [('xi', ['k', 'ʃ'])], # "an[xi]ous"

    [('awy', ['oj'])], # "l[awy]er"
    [('aye', ['ɛː'])], # "pr[aye]r"

    [('a', ['oː'])], # "[a]ll"
    [('a', []), ('o', ['oː'])], # "extr[ao]rdinary"

    [('c', ['k'])], # "be[c]ome"
    [('c', []), ('k', ['k'])], # "ba[ck]"

    [('e', ['ɔ'])], # "g[e]nre"
    [('e', []), ('o', ['ɔ'])], # "g[eo]graphy"

    [('ie', ['ɪj'])], # "mov[ie]"
    [('i', ['ɪj']), ('e', ['ə']), ('r', [])], # "earl[ier]"

    [('r', ['ə'])], # "fi[r]e"
    [('r', []), ('o', ['ə'])], # "i[ro]n"

    [('u', ['ə'])], # "acc[u]rate"
    [('u', []), ('a', ['ə'])], # "act[ua]lly"

    [('u', ['ɛ'])], # "b[u]ry"
    [('u', []), ('e', ['ɛ'])], # "g[ue]ss"

    [('u', ['ɪ'])], # "b[u]sy"
    [('u', []), ('i', ['ɪ'])], # "b[ui]ld"
]

PENALIZED_PATTERNS = [
    # Penalize unspelled sounds and silent letters to speed things up
    # and discourage overly "lazy" pairings:
    # <a  r e  a> not <a  r ea  >
    # /ɛ́ː r ɪj ə/     /ɛ́ː r ɪj ə/
    # <a cc ou n t> not <a c c ou n t>
    # /ə k  áw n t/     /ə k   áw n t/
    # Actually, "account" would be correct even without the penalty
    # because longer spellings are matched first, but it seems more
    # robust to not rely on that.
    # More importantly, unspelled sounds and silent letters need to be
    # penalized by the same amount to get cases like this right:
    # <f ai l   u r e> not <f ai l u r   e>
    # /f ɛ́j l j ə    /     /f ɛ́j l     j ə/

    # Silent letters
    [('a', [])], # "basic[a]lly"
    [('au', [])], # "rest[au]rant"
    [('b', [])], # "clim[b]"
    [('c', [])], # "ba[c]k"
    [('d', [])], # "san[d]wich"
    [('e', [])], # "mak[e]"
    [('g', [])], # "si[g]n"
    [('gh', [])], # "li[gh]t"
    [('h', [])], # "[h]our", "o[h]"
    [('i', [])], # "bus[i]ness"
    [('k', [])], # "[k]now"
    [('l', [])], # "ca[l]m"
    [('m', [])], # "[m]nemonic"
    [('n', [])], # "autum[n]"
    [('o', [])], # "choc[o]late"
    [('p', [])], # "cu[p]board"
    [('s', [])], # "i[s]land"
    [('t', [])], # "cas[t]le"
    [('u', [])], # "b[u]ild"
    [('w', [])], # "s[w]ord"

    # Don't analyze <r> as part of a vowel even though that might make
    # more sense in cases like <ir> /əː/. This ensures that <r> can
    # consistently be matched as a standalone silent letter and that
    # no extra rules are needed for when the <r> is pronounced:
    # <f ai r y >
    # /f ɛ́ː r ɪj/
    [('r', [])],

    # Unspelled sounds
    [('', ['j'])], # "b[]eauty"
    [('', ['k'])], # "leng[]th"
    [('', ['r'])], # "draw[]ing"
    [('', ['ə'])], # "simp[]le"
]

TRIE = Trie(Trie)

for patterns, penalty in [(PATTERNS, 0), (PENALIZED_PATTERNS, 1)]:
    for pattern in patterns:
        spell_key = []
        sound_key = []
        lengths   = []
        for spell, sounds in pattern:
            spell_key.extend(spell)
            sound_key.extend(sounds)
            lengths.append((len(spell), len(sounds)))
        TRIE[spell_key][sound_key] = lengths, penalty

def split(lst, i):
    return lst[:i], lst[i:]

def parse_ipa(ipa):
    return list(map(Sound.from_ipa, ipa.split()))

def link(word, ipa):
    result = []
    pron = parse_ipa(ipa)
    pairs = pair(word, pron)
    if pairs is None:
        raise ValueError(f'Failed to link <{word}> to /{ipa}/')
    for spell, sounds in pairs:
        if not sounds:
            sounds = [Sound.from_ipa('')]
        for i, sound in enumerate(sounds):
            if not i:
                sound.spell = spell
                sound.cont = False
            else:
                sound.spell = ''
                sound.cont = True
            result.append(sound)
    return result

def pair(word, pron):
    count = 0
    queue = [(0, count, word, pron, [])]
    while queue:
        score, _, word, pron, pairs = heappop(queue)
        if not word and not pron:
            return pairs
        for trie in reversed(list(TRIE.lookup_prefixes(word.lower()))):
            for lengths, penalty in trie.lookup_prefixes(sound.ipa for sound in pron):
                count += 1
                new_word = word
                new_pron = pron
                new_pairs = []
                for word_length, pron_length in lengths:
                    word_head, new_word = split(new_word, word_length)
                    pron_head, new_pron = split(new_pron, pron_length)
                    new_pairs.append((word_head, pron_head))
                heappush(queue, (
                    score + penalty,
                    count,
                    new_word,
                    new_pron,
                    pairs + new_pairs
                ))

from link import link

STRESS = '\u0301'

def show(sound):
    if sound.stressed:
        return sound.ipa[0] + STRESS + sound.ipa[1:]
    return sound.ipa

def length(item):
    return len(item.replace(STRESS, ''))

with open('dict.tsv') as f, open('links.txt', 'w') as g:
    def tee(string):
        print(string, end='')
        g.write(string)
    for i, line in enumerate(f):
        word, pron = line.strip().split('\t')
        sounds = link(word, pron)
        pairs = [(show(sound), sound.spelled) for sound in sounds]
        lengths = [max(map(length, pair)) for pair in pairs]
        if i:
            tee('\n')
        for items in reversed(list(zip(*pairs))):
            tee(' '.join(item.ljust(length) for item, length in zip(items, lengths)).strip())
            tee('\n')

from link import link

STRESS = '\u0301'

def show_ipa(sound):
    if sound.stressed:
        return sound.ipa[0] + STRESS + sound.ipa[1:]
    return sound.ipa

def show_spell(sound):
    if sound.cont:
        return '…'
    return sound.spelled

def width(item):
    return len(item.replace(STRESS, ''))

def pad(string, width):
    return string.ljust(width + string.count(STRESS))

with open('dict.tsv') as f, open('links.txt', 'w') as g:
    def tee(string):
        print(string, end='')
        g.write(string)
    for i, line in enumerate(f):
        word, pron = line.strip().split('\t')
        sounds = link(word, pron)
        pairs = [(show_ipa(sound), show_spell(sound)) for sound in sounds]
        widths = [max(map(width, pair)) for pair in pairs]
        if i:
            tee('\n')
        for items in reversed(list(zip(*pairs))):
            tee(' '.join(pad(item, width) for item, width in zip(items, widths)).strip())
            tee('\n')

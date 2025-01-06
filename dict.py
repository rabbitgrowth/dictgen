from generate import generate
from link import link

STRESS = '\u0301'

def show_ipa(sound):
    return sound.ipa[0] + STRESS + sound.ipa[1:] if sound.stressed else sound.ipa

def show_spell(sound):
    return '-' if sound.cont else sound.spell

def width(item):
    return len(item.replace(STRESS, ''))

def pad(string, width):
    return string.ljust(width + string.count(STRESS))

with open('dict.tsv', encoding='utf-8') as f, open('dict.txt', 'w', encoding='utf-8') as g:
    def tee(string=''):
        print(string)
        g.write(string)
        g.write('\n')
    for i, line in enumerate(f):
        word, ipa = line.strip().split('\t')
        sounds = link(word, ipa)
        pairs = [(show_ipa(sound), show_spell(sound)) for sound in sounds]
        widths = [max(map(width, pair)) for pair in pairs]
        ipas, spells = zip(*pairs)
        if i:
            tee()
        tee(word)
        for items in [spells, ipas]:
            line = ' '.join(pad(item, width) for item, width in zip(items, widths))
            tee(line.rstrip())
        for outline in generate(sounds):
            tee('/'.join(map(str, outline)))

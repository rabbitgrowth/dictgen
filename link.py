from sound import Sound

PAIRS = [
    ('', [Sound('.')]),
    ('a', [Sound('a')]),
    ('b', [Sound('b')]),
    ('bb', [Sound('b')]),
    ('c', [Sound('k')]),
    ('cc', [Sound('k')]),
    ('c', []),
    ('e', [Sound('ɛ')]),
    ('e', [Sound('ɪ')]),
    ('h', []),
    ('i', [Sound('ɪ')]),
    ('k', [Sound('k')]),
    ('ou', [Sound('aw')]),
    ('p', [Sound('p')]),
    ('r', [Sound('r')]),
    ('r', [Sound('ə')]),
    ('s', [Sound('s')]),
    ('sh', [Sound('ʃ')]),
    ('t', [Sound('t')]),
    ('u', [Sound('ʌ')]),
    ('x', [Sound('k'), Sound('s')]),
]

def link(word, pron):
    sounds = list(map(Sound.from_ipa, pron.split()))
    try:
        pairs = next(pair(word, sounds))
    except StopIteration:
        raise ValueError(f'Failed to link "{word}" to "{pron}"')
    for spell, sequence in pairs:
        if not sequence:
            yield Sound('', spelled=spell)
        else:
            for i, sound in enumerate(sequence):
                if not i:
                    sound.spelled = spell
                    sound.cont = False
                else:
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

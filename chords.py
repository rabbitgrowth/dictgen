from stroke import Stroke

LEFT_CHORDS = {
    'b': Stroke('PW'),
    'd': Stroke('TK'),
    'f': Stroke('TP'),
    'g': Stroke('TKPW'),
    'h': Stroke('H'),
    'k': Stroke('K'),
    'l': Stroke('HR'),
    'm': Stroke('PH'),
    'n': Stroke('TPH'),
    'p': Stroke('P'),
    'r': Stroke('R'),
    's': Stroke('S'),
    't': Stroke('T'),
    'v': Stroke('SR'),
    'w': Stroke('W'),
    'j': Stroke('KWR'),
    'z': Stroke('SWR'),
    'ʃ': Stroke('SH'),
    'θ': Stroke('TH'),
    'ð': Stroke('TH'),
    'tʃ': Stroke('KH'),
    'dʒ': Stroke('SKWR'),
}

MID_CHORDS = {
    'ɪ':  Stroke('EU'),
    'ɪj': Stroke('AOE'),
    'ɪː': Stroke('AOE'), # TODO except in "idea"?
    'ɛ':  Stroke('E'),
    'ɛj': Stroke('AEU'),
    'ɛː': Stroke('AEU'),
    'a':  Stroke('A'),
    'ɑj': Stroke('AOEU'),
    'ɑː': Stroke('A'),
    'ʌ':  Stroke('U'),
    'əw': Stroke('OE'),
    'əː': Stroke('U'),
    'ɔ':  Stroke('AU'), # TODO use O?
    'oj': Stroke('OEU'),
    'oː': Stroke('AU'),
    'ɵ':  Stroke('AO'), # TODO except in "put" etc.?
    'ʉw': Stroke('AOU'),
    'ɵː': Stroke('AOU'), # TODO to be confirmed
    'ə':  Stroke('U'),
    'aw': Stroke('OU'),
}

RIGHT_CHORDS = {
    'b': Stroke('-B'),
    'd': Stroke('-D'),
    'f': Stroke('-F'),
    'g': Stroke('-G'),
    'k': Stroke('-BG'),
    'l': Stroke('-L'),
    'm': Stroke('-PL'),
    'n': Stroke('-PB'),
    'p': Stroke('-P'),
    'r': Stroke('-R'),
    's': Stroke('-S'),
    't': Stroke('-T'),
    'v': Stroke('-FB'),
    'z': Stroke('-Z'),
    'ŋ': Stroke('-PBG'),
    'ʃ': Stroke('-GS'),
    'θ': Stroke('-GT'),
    'ð': Stroke('-GT'),
    'tʃ': Stroke('-FP'),
    'dʒ': Stroke('-PBLG'),
}

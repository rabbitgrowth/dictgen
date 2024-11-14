import unittest

from dictgen import Stroke, destress, gen

class TestDictgen(unittest.TestCase):
    def T(self, word, pron, outlines):
        letters = word.split()
        symbols = destress(pron).split()
        pairs = list(zip(letters, symbols, strict=True))
        result = set(map(tuple, gen(pairs)))
        expected = {
            tuple(map(Stroke, outline.strip().split('/')))
            for outline in outlines.split()
        }
        self.assertEqual(result, expected)

    def test_basic(self):
        self.T('c a t', 'k á t', 'KAT')
        self.T('s t r a p', 's t r á p', 'STRAP')

    def test_multistroke(self):
        self.T('h a h a h a', 'h a h a h a', 'HA/HA/HA')

    def test_consonants_out_of_steno_order(self):
        self.T('G w e n', 'g w ɛ́ n', 'TKPWU/WEPB')
        self.T('s e g u e', 's ɛ́ g w ɛj', 'SEG/WAEU')

    def test_compound_sounds(self):
        self.T('s l e d', 's l ɛ́ d', 'SHRED')
        self.T('sh r e d', 'ʃ r ɛ́ d', 'SKHRED SHU/RED')

    def test_orthographic_chord(self):
        self.T('s e ll', 's ɛ́ l', 'SEL')
        self.T('c e ll', 's ɛ́ l', 'KREL')
        self.T('Sz e ll', 's ɛ́ l', 'SEL')

    def test_vowel_variants(self):
        self.T('f ee', 'f ɪ́j', 'TPAOE')
        self.T('f l ee', 'f l ɪ́j', 'TPHRAOE')
        self.T('f l ee ce', 'f l ɪ́j s', 'TPHRAOES')
        self.T('f e m a le', 'f ɪ́j m ɛj l', 'TPAOEPL/AEUL TPE/PHAEUL')
        self.T('s e l f ie', 's ɛ́ l f ɪj', 'SEL/TPAE')

if __name__ == '__main__':
    unittest.main()

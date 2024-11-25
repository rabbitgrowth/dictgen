import unittest

from stroke import Stroke
from dictgen import to_sounds, syllabify, gen

class TestDictgen(unittest.TestCase):
    def T(self, word, pron, outlines):
        pairs = zip(word.split(), pron.split(), strict=True)
        sounds = to_sounds(pairs)
        result = {
            outline
            for syllabification in syllabify(sounds)
            for outline in gen(syllabification)
        }
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

    def test_vowel_omission_principle(self):
        self.T('c o n f l i c t', 'k ə n f l ɪ́ k t', 'KUPB/TPHREUBGT')
        self.T('c o n f l i c t', 'k ɔ́ n f l ɪ k t', 'KAUPB/TPHR-BGT')

if __name__ == '__main__':
    unittest.main()

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

if __name__ == '__main__':
    unittest.main()

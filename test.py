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

    def test_cvc(self):
        self.T('c a t', 'k á t', 'KAT')
        self.T('d o g', 'd ɔ́ g', 'TKAUG')

    def test_ccvcc(self):
        self.T('s c r i p t', 's k r ɪ́ p t', 'SKREUPT')

    def test_compound_sounds(self):
        self.T('s l e d', 's l ɛ́ d', 'SHRED')
        self.T('sh r e d', 'ʃ r ɛ́ d', 'SKHRED SHU/RED')

    def test_ight(self):
        self.T('r i te',  'r ɑ́j t', 'RAOEUT')
        self.T('r igh t', 'r ɑ́j t', 'ROEUGT')

    @unittest.expectedFailure
    def test_igh_t(self):
        self.T('h igh # t ai l', 'h ɑ́j # t ɛj l', 'HAOEU/TAEUL')

    def test_consonants_out_of_steno_order(self):
        self.T('G w e n', 'g w ɛ́ n', 'TKPWU/WEPB')
        self.T('s e g u e', 's ɛ́ g w ɛj', 'SEG/WAEU')

    def test_left_vowel_attracts_consonant(self):
        self.T('f o ll ow', 'f ɔ́ l əw', 'TPAUL/OE')

    def test_right_vowel_attracts_consonant(self):
        self.T('a b ou t', 'ə b áw t', 'U/PWOUT')

if __name__ == '__main__':
    unittest.main()

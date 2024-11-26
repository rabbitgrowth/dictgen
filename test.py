import unittest

from stroke import Stroke
from dictgen import Sound, syllabify, gen

class TestDictgen(unittest.TestCase):
    def T(self, word, pron, outlines):
        pairs = zip(word.split(' '), pron.split(' '), strict=True)
        sounds = [Sound(ipa, spelling) for spelling, ipa in pairs]
        result = {
            outline
            for syllables in syllabify(sounds)
            for outline in gen(syllables)
        }
        expected = {
            tuple(map(Stroke, outline.split('/')))
            for outline in outlines.split()
        }
        self.assertEqual(result, expected)

    def test_consonant_vowel_consonant(self):
        self.T('c a t', 'k á t', 'KAT')
        self.T('d o g', 'd ɔ́ g', 'TKAUG')

    def test_consonants_vowel_consonants(self):
        self.T('s c r i p t', 's k r ɪ́ p t', 'SKREUPT')

    def test_compound_sounds(self):
        self.T('s l e d', 's l ɛ́ d', 'SHRED')
        self.T('sh r e d', 'ʃ r ɛ́ d', 'SKHRED SHU/RED')

    def test_silent_h(self):
        self.T('h eir', ' ɛ́ː', 'HAEUR')
        self.T('air', 'ɛ́ː', 'AEUR')

    def test_wh_pronounced_w(self):
        self.T('w h a t', 'w  ɔ́ t', 'WHAUT')

    @unittest.expectedFailure
    def test_wh_pronounced_h(self):
        self.T('w h o le', ' h ə́w l', 'HOEL')

    def test_ight(self):
        self.T('r i te',  'r ɑ́j t', 'RAOEUT')
        self.T('r igh t', 'r ɑ́j t', 'ROEUGT')

    def test_igh_t(self):
        self.T('h igh  t ai l', 'h ɑ́j . t ɛj l', 'HAOEU/TAEUL')

    def test_consonants_out_of_steno_order(self):
        self.T('G w e n', 'g w ɛ́ n', 'TKPWU/WEPB')
        self.T('s e g u e', 's ɛ́ g w ɛj', 'SEG/WAEU')

    def test_left_vowel_attracts_consonant(self):
        self.T('f o ll ow', 'f ɔ́ l əw', 'TPAUL/OE')

    @unittest.expectedFailure
    def test_left_vowel_attracts_consonants(self):
        self.T('i n t e r e s t', 'ɪ́ n t  r ɛ s t', 'EUPB/TR*ES EUPBT/R*ES')

    def test_right_vowel_attracts_consonant(self):
        self.T('a b ou t', 'ə b áw t', 'U/PWOUT')

    def test_right_vowel_attracts_consonants(self):
        self.T('c o m p l e te', 'k ə m p l ɪ́j t', 'KUPL/PHRAOET KUFPL/HRAOET')

    def test_not_start_with_impossible_onset(self):
        self.T('a d m i t', 'ə d m ɪ́ t', 'UD/PHEUT') # not U/TKPHEUT

if __name__ == '__main__':
    unittest.main()

import unittest

from stroke import Stroke
from dictgen import parse_pron, syllabify, gen

class TestDictgen(unittest.TestCase):
    def T(self, pron, outlines):
        sounds = parse_pron(pron)
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
        self.T('k á t', 'KAT')
        self.T('d ɔ́ g', 'TKAUG')

    def test_consonants_vowel_consonants(self):
        self.T('s k r ɪ́ p t', 'SKREUPT')

    def test_compound_sounds(self):
        self.T('s l ɛ́ d', 'SHRED')
        self.T('ʃ r ɛ́ d', 'SKHRED SHU/RED')

    def test_silent_h(self):
        self.T(':h ɛ́ː', 'HAEUR')
        self.T('   ɛ́ː', 'AEUR')

    def test_wh_pronounced_w(self):
        self.T('w:wh ɪ́ ʧ', 'WHEUFP')
        self.T('w    ɪ́ ʧ', 'WEUFP')

    def test_wh_pronounced_h(self):
        self.T('h:wh ə́w l', 'WHOEL')
        self.T('h    ə́w l', 'HOEL')

    def test_ight(self):
        self.T('r ɑ́j t', 'RAOEUT')
        self.T('r ɑ́j:igh t', 'ROEUGT')

    def test_igh_t(self):
        self.T('h ɑ́j:igh . t ɛj l', 'HAOEU/TAEUL')

    def test_consonants_out_of_steno_order(self):
        self.T('g w ɛ́ n', 'TKPWU/WEPB')
        self.T('s ɛ́ g w ɛj', 'SEG/WAEU')

    def test_left_vowel_attracts_consonant(self):
        self.T('f ɔ́ l əw', 'TPAUL/OE')

    @unittest.expectedFailure
    def test_left_vowel_attracts_consonants(self):
        self.T('ɪ́ n t r ɛ s t', 'EUPB/TR*ES EUPBT/R*ES')

    def test_right_vowel_attracts_consonant(self):
        self.T('ə b áw t', 'U/PWOUT')

    def test_right_vowel_attracts_consonants(self):
        self.T('k ə m p l ɪ́j t', 'KUPL/PHRAOET KUFPL/HRAOET')

    def test_not_start_with_impossible_onset(self):
        self.T('ə d m ɪ́ t', 'UD/PHEUT') # not U/TKPHEUT

if __name__ == '__main__':
    unittest.main()

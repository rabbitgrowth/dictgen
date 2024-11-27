import unittest

from stroke import Stroke
from dictgen import parse_pron, syllabify, stackable, gen

class TestStackable(unittest.TestCase):
    def test_simple_cases(self):
        self.assertTrue (stackable(Stroke('S'), Stroke('T')))
        self.assertFalse(stackable(Stroke('T'), Stroke('S')))

    def test_empty_strokes(self):
        self.assertTrue(stackable(Stroke(''),  Stroke('S')))
        self.assertTrue(stackable(Stroke('S'), Stroke('')))

    def test_with_star(self):
        self.assertTrue (stackable(Stroke('S*'), Stroke('T')))
        self.assertFalse(stackable(Stroke('T*'), Stroke('S')))
        self.assertTrue (stackable(Stroke('S'),  Stroke('T*')))
        self.assertFalse(stackable(Stroke('T'),  Stroke('S*')))
        self.assertFalse(stackable(Stroke('S*'), Stroke('T*')))

    def test_longer_strokes(self):
        self.assertTrue (stackable(Stroke('STRAU'),    Stroke('-PBG')))
        self.assertFalse(stackable(Stroke('STR*EPBG'), Stroke('-GT')))

    def test_exceptions(self):
        self.assertTrue (stackable(Stroke('SP'), Stroke('R')))
        self.assertFalse(stackable(Stroke('SH'), Stroke('R')))

class TestDictgen(unittest.TestCase):
    def T(self, word, pron, outlines):
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
        self.T('cat', 'k á t', 'KAT')
        self.T('dog', 'd ɔ́ g', 'TKAUG')

    def test_consonants_vowel_consonants(self):
        self.T('script', 's k r ɪ́ p t', 'SKREUPT')

    def test_shr(self):
        self.T('shred', 'ʃ r ɛ́ d', 'SKHRED SHU/RED')
        self.T('sled',  's l ɛ́ d', 'SHRED')

    def test_silent_h(self):
        self.T('heir', ':h ɛ́ː', 'HAEUR')
        self.T('air',  '   ɛ́ː', 'AEUR')

    def test_wh_pronounced_w(self):
        self.T('which', 'w:wh ɪ́ ʧ', 'WHEUFP')
        self.T('witch', 'w    ɪ́ ʧ', 'WEUFP')

    def test_wh_pronounced_h(self):
        self.T('whole', 'h:wh ə́w l', 'WHOEL')
        self.T('hole',  'h    ə́w l', 'HOEL')

    def test_vowel_omission_principle(self):
        self.T('title',    't ɑ́j t ə l',    'TAOEUT/-L')
        self.T('children', 'ʧ ɪ́ l d r ə n', 'KHEUL/TKR-PB KHEULD/R-PB')
        self.T('visit',    'v ɪ́ z ɪ t',     'SREUZ/-T')
        self.T('mountain', 'm áw n t ɪ n',  'PHOUPB/T-PB PHOUPBT/-PB')

    def test_ight(self):
        self.T('rite',  'r ɑ́j     t', 'RAOEUT')
        self.T('right', 'r ɑ́j:igh t', 'ROEUGT')

    def test_igh_t(self):
        self.T('hightail', 'h ɑ́j:igh . t ɛj l', 'HAOEU/TAEUL')

    def test_initial_consonants_out_of_steno_order(self):
        self.T('Gwen', 'g w ɛ́ n', 'TKPWU/WEPB')

    def test_medial_consonants_out_of_steno_order(self):
        self.T('segue', 's ɛ́ g w ɛj', 'SEG/WAEU') # not SE/TKPWU/WAEU

    def test_left_vowel_attracts_consonant(self):
        self.T('follow', 'f ɔ́ l əw', 'TPAUL/OE')

    def test_left_vowel_attracts_consonants(self):
        self.T('interest', 'ɪ́ n t r ɛ s t', 'EUPB/TR*ES EUPBT/R*ES')

    def test_right_vowel_attracts_consonant(self):
        self.T('about', 'ə b áw t', 'U/PWOUT')

    def test_right_vowel_attracts_consonants(self):
        self.T('complete', 'k ə m p l ɪ́j t', 'KUPL/PHRAOET KUFPL/HRAOET')

    def test_not_start_with_impossible_onset(self):
        self.T('admit', 'ə d m ɪ́ t', 'UD/PHEUT') # not U/TKPHEUT

if __name__ == '__main__':
    unittest.main()

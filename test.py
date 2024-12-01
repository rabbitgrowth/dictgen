import unittest

from stroke import Stroke
from dictgen import parse_ipa, stackable, generate

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

def split(string):
    for word in string.split():
        yield '' if word == '-' else word

class TestDictgen(unittest.TestCase):
    def T(self, word, pron, outlines):
        sounds = []
        for spelled, ipa in zip(split(word), split(pron)):
            sound = parse_ipa(ipa)
            sound.spelled = spelled
            sounds.append(sound)
        expected = {
            tuple(map(Stroke, outline.split('/')))
            for outline in outlines.split()
        }
        self.assertEqual(generate(sounds), expected)

    def test_consonant_vowel_consonant(self):
        self.T('c a t', 'k á t', 'KAT')
        self.T('d o g', 'd ɔ́ g', 'TKAUG')

    def test_consonants_vowel_consonants(self):
        self.T('s c r i p t', 's k r ɪ́ p t', 'SKREUPT')

    def test_shr(self):
        self.T('sh r e d', 'ʃ r ɛ́ d', 'SKHRED SHU/RED')
        self.T('s  l e d', 's l ɛ́ d', 'SHRED')

    def test_silent_h(self):
        self.T('h eir', '- ɛ́ː', 'HAEUR')
        self.T('  air', '  ɛ́ː', 'AEUR')

    def test_wh_pronounced_w(self):
        self.T('w h i ch',  'w - ɪ́ ʧ', 'WHEUFP')
        self.T('w   i tch', 'w   ɪ́ ʧ', 'WEUFP')

    def test_wh_pronounced_h(self):
        self.T('w h o le', '- h ə́w l', 'WHOEL')
        self.T('  h o le', '  h ə́w l', 'HOEL')

    def test_y_ending(self):
        self.T('f a m i l y', 'f á m - l ɪj', 'TPAPL/HRAE')
        self.T('e m p l oy ee', 'ɛ́ m p l oj ɪ́j', 'EPL/PHROEU/AE EFPL/HROEU/AE')

    def test_y_ending_foldable(self):
        self.T('p r i v a c y', 'p r ɪ́ v ə s ɪj',
               'PREUFB/U/SAE PREUFB/SAE PREUFB/-S/AE PREUFB/AES')
        self.T('a g e n c y', 'ɛ́j ʤ ə n s ɪj',
               'AEUPBLG/-PB/SAE AEUPBLG/-PBS/AE AEUPBLG/AEPBS')

    def test_ight(self):
        self.T('r i te',  'r ɑ́j t', 'RAOEUT')
        self.T('r igh t', 'r ɑ́j t', 'ROEUGT')

    def test_igh_t(self):
        self.T('h igh - t ai l', 'h ɑ́j:igh . t ɛj l', 'HAOEU/TAEUL') # not HOEUGT/AEUL

    def test_omit_weak_schwa(self):
        self.T('t i t - le', 't ɑ́j t ə l', 'TAOEUT/-L')
        self.T('ch i l d r e n', 'ʧ ɪ́ l d r ə n', 'KHEUL/TKR-PB KHEULD/R-PB')
        self.T('v i s i t', 'v ɪ́ z ɪ t', 'SREUZ/-T')
        self.T('m ou n t ai n', 'm áw n t ɪ n', 'PHOUPB/T-PB PHOUPBT/-PB')

    def test_not_omit_initial_weak_schwa(self):
        self.T('a b ou t', 'ə b áw t', 'U/PWOUT')

    def test_not_omit_when_conflict_with_inflections(self):
        self.T('r a p i d', 'r á p ɪ d', 'RAP/UD')
        self.T('d e s i g n at e', 'd ɛ́ z ɪ g n ɛj t', 'TKEZ/UG/TPHAEUT')
        self.T('t a l i s m a n', 't á l ɪ z m ə n', 'TAL/UZ/PH-PB')

    def test_omit_when_not_conflict_with_inflections(self):
        self.T('r a p i d s', 'r á p ɪ d z', 'RAP/-DZ')

    def test_omit_weak_schwa_at_syllable_end(self):
        self.T('c o n f e r e n ce', 'k ɔ́ n f ə r ə n s',
               'KAUPB/TPU/R-PBS KAUPB/TPR-PBS KAUPB/TP-R/-PBS') # not KAUPB/TP/R-PBS

    def test_silent_b(self):
        self.T('c l i me', 'k l ɑ́j m', 'KHRAOEUPL')
        self.T('c l i mb', 'k l ɑ́j m', 'KHRAOEUPL/-B')

    def test_initial_consonants_out_of_steno_order(self):
        self.T('G w e n', 'g w ɛ́ n', 'TKPWU/WEPB')

    def test_medial_consonants_out_of_steno_order(self):
        self.T('s e g u e', 's ɛ́ g w ɛj', 'SEG/WAEU') # not SE/TKPWU/WAEU

    def test_left_vowel_attracts_consonant(self):
        self.T('f o ll ow', 'f ɔ́ l əw', 'TPAUL/OE')

    def test_left_vowel_attracts_consonants(self):
        self.T('i n t r o', 'ɪ́ n t r əw', 'EUPB/TROE EUPBT/ROE')

    def test_right_vowel_attracts_consonant(self):
        self.T('m a ch i ne', 'm ə ʃ ɪ́j n', 'PHU/SHAOEPB')

    def test_right_vowel_attracts_consonants(self):
        self.T('c o m p l e te', 'k ə m p l ɪ́j t', 'KUPL/PHRAOET KUFPL/HRAOET')

    def test_not_start_with_impossible_onset(self):
        self.T('a d m i t', 'ə d m ɪ́ t', 'UD/PHEUT') # not U/TKPHEUT

if __name__ == '__main__':
    unittest.main()

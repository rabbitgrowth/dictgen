import unittest

from generate import generate
from link import link
from sound import Sound
from stroke import Stroke

class TestGenerate(unittest.TestCase):
    def T(self, word, pron, outlines):
        sounds = link(word, pron)
        result = generate(sounds)
        expected = sorted(
            tuple(map(Stroke, outline.split('/')))
            for outline in outlines.split()
        )
        self.assertEqual(result, expected)

    def test_consonant_vowel_consonant(self):
        self.T('cat', 'k á t', 'KAT')
        self.T('dog', 'd ɔ́ g', 'TKAUG')

    def test_consonants_vowel_consonants(self):
        self.T('script', 's k r ɪ́ p t', 'SKREUPT')

    def test_shr(self):
        self.T('shred', 'ʃ r ɛ́ d', 'SKHRED')
        self.T('sled',  's l ɛ́ d', 'SHRED')

    def test_silent_h(self):
        self.T('heir', 'ɛ́ː', 'HAEUR')
        self.T('air',  'ɛ́ː', 'AEUR')

    def test_silent_h_in_wh(self):
        self.T('which', 'w ɪ́ tʃ', 'WHEUFP')
        self.T('witch', 'w ɪ́ tʃ', 'WEUFP')

    def test_silent_w_in_wh(self):
        self.T('whole', 'h ə́w l', 'WHOEL')
        self.T('hole',  'h ə́w l', 'HOEL')

    def test_silent_b(self):
        self.T('clime', 'k l ɑ́j m', 'KHRAOEUPL')
        self.T('climb', 'k l ɑ́j m', 'KHRAOEUPL/-B')

    def test_skip_other_silent_letters(self):
        self.T('yacht', 'j ɔ́ t', 'KWRAUT')
        self.T('mnemonic', 'n ɪ m ɔ́ n ɪ k', 'TPHEU/PHAUPB/-BG')
        self.T('restaurant', 'r ɛ́ s t r ɔ n t', 'RES/TRAUPBT R*ES/RAUPBT')

    def test_y_ending(self):
        self.T('family', 'f á m l ɪj', 'TPAPL/HRAE')
        self.T('employee', 'ɛ́ m p l oj ɪ́j', 'EPL/PHROEU/AE EFPL/HROEU/AE')

    @unittest.expectedFailure
    def test_y_ending_foldable(self):
        self.T('privacy', 'p r ɪ́ v ə s ɪj',
               'PREUFB/U/SAE PREUFB/SAE PREUFB/-S/AE PREUFB/AES')
        self.T('agency', 'ɛ́j dʒ ə n s ɪj',
               'AEUPBLG/-PB/SAE AEUPBLG/-PBS/AE AEUPBLG/AEPBS')

    def test_orthographic_ight(self):
        self.T('rite',  'r ɑ́j t', 'RAOEUT')
        self.T('right', 'r ɑ́j t', 'ROEUGT')

    def test_not_orthographic_ight_if_interrupted_by_break(self):
        self.T('hightail', 'h ɑ́j . t ɛj l', 'HAOEU/TAEUL') # not HOEUGT/AEUL

    def test_orthographic_ss(self):
        self.T('mass',    'm á s',     'PHAFS')
        self.T('massive', 'm á s ɪ v', 'PHAS/-FB')

    def test_not_orthographic_ss_if_multistroke(self):
        self.T('witness', 'w ɪ́ t n ə s', 'WEUT/TPH-S')

    def test_omit_schwa(self):
        self.T('title', 't ɑ́j t ə l', 'TAOEUT/-L')
        self.T('children', 'tʃ ɪ́ l d r ə n', 'KHEUL/TKR-PB KHEULD/R-PB')
        self.T('visit', 'v ɪ́ z ɪ t', 'SREUZ/-T')
        self.T('mountain', 'm áw n t ɪ n', 'PHOUPB/T-PB PHOUPBT/-PB')

    def test_not_omit_initial_schwa(self):
        self.T('about', 'ə b áw t', 'U/PWOUT')

    def test_not_omit_schwa_when_conflict_with_inflectional_endings(self):
        self.T('rapid', 'r á p ɪ d', 'RAP/UD')
        self.T('designate', 'd ɛ́ z ɪ g n ɛj t', 'TKEZ/UG/TPHAEUT')
        self.T('talisman', 't á l ɪ z m ə n', 'TAL/UZ/PH-PB')

    def test_omit_schwa_when_not_conflict_with_inflectional_endings(self):
        self.T('rapids', 'r á p ɪ d z', 'RAP/-DZ')

    def test_not_omit_schwa_when_right_bank_empty(self):
        self.T('conference', 'k ɔ́ n f ə r ə n s',
               'KAUPB/TPU/R-PBS KAUPB/TPR-PBS KAUPB/TP-R/-PBS') # not KAUPB/TP/R-PBS

    def test_omit_j(self):
        self.T('new',    'n j ʉ́w',      'TPHAOU')
        self.T('beauty', 'b j ʉ́w t ɪj', 'PWAOUT/AE')

    def test_not_omit_initial_j(self):
        self.T('year', 'j ɪ́ː',   'KWRAOER')
        self.T('use',  'j ʉ́w z', 'KWRAOUZ')

    def test_not_omit_j_when_left_bank_empty(self):
        self.T('failure', 'f ɛ́j l j ə',  'TPAEUL/KWR-R')
        self.T('million', 'm ɪ́ l j ə n', 'PHEUL/KWR-PB')

    def test_omit_j_or_not_depending_on_syllabification(self):
        self.T('abuse',  'ə b j ʉ́w s', 'U/PWAOUS UB/KWRAOUS')
        self.T('accuse', 'ə k j ʉ́w z', 'U/KAOUZ UBG/KWRAOUZ')

    def test_optionally_omit_j_schwa(self):
        self.T('accurate', 'á k j ə r ə t', 'ABG/KWR-R/-T ABG/KWRU/R-T ABG/R-T')
        self.T('regulation', 'r ɛ́ g j ə l ɛ́j ʃ ə n', 'REG/KWRU/HRAEUGZ REG/HRAEUGZ')

    def test_fold_inflectional_s(self):
        self.T('plans', 'p l á n z', 'PHRAPBZ')
        self.T('terms', 't ə́ː m z',  'TURPLZ')

    def test_come_back_for_inflectional_s(self):
        self.T('bags',  'b á  g z', 'PWAG/-Z')
        self.T('backs', 'b á  k s', 'PWABG/-Z')
        self.T('barks', 'b ɑ́ː k s', 'PWARBG/-Z')

    def test_write_z_for_inflectional_s_pronounced_s(self):
        self.T('tips', 't ɪ́ p s', 'TEUPZ')

    def test_write_s_for_inflectional_s_preceded_by_t(self):
        self.T('gets', 'g ɛ́ t s', 'TKPWETS')

    def test_write_noninflectional_s_normally(self):
        self.T('yes', 'j ɛ́ s', 'KWRES')
        self.T('has', 'h á z', 'HAZ')

    def test_detect_whether_s_is_inflectional_based_on_spelling(self):
        self.T('lapse',  'l á p s',  'HRAPS')
        self.T('laps',   'l á p s',  'HRAPZ')
        self.T('tease',  't ɪ́j z',   'TAOEZ')
        self.T('tees',   't ɪ́j z',   'TAOE/-Z')
        self.T('freeze', 'f r ɪ́j z', 'TPRAOEZ')
        self.T('frees',  'f r ɪ́j z', 'TPRAOE/-Z')

    def test_initial_consonants_out_of_steno_order(self):
        self.T('Gwen', 'g w ɛ́ n', 'TKPWU/WEPB')

    def test_medial_consonants_out_of_steno_order(self):
        self.T('language', 'l á ŋ g w ɪ dʒ', 'HRAPBG/W-PBLG') # not HRAPBG/TKPWU/W-PBLG

    def test_final_consonants_out_of_steno_order(self):
        self.T('help', 'h ɛ́ l p', 'HEL/-P')

    def test_left_vowel_attracts_consonant(self):
        self.T('follow', 'f ɔ́ l əw', 'TPAUL/OE')

    def test_left_vowel_attracts_consonants(self):
        self.T('intro', 'ɪ́ n t r əw', 'EUPB/TROE EUPBT/ROE')

    def test_right_vowel_attracts_consonant(self):
        self.T('machine', 'm ə ʃ ɪ́j n', 'PHU/SHAOEPB')

    def test_right_vowel_attracts_consonants(self):
        self.T('complete', 'k ə m p l ɪ́j t', 'KUPL/PHRAOET KUFPL/HRAOET')

    def test_not_start_with_impossible_onset(self):
        self.T('admit', 'ə d m ɪ́ t', 'UD/PHEUT') # not U/TKPHEUT

if __name__ == '__main__':
    unittest.main()

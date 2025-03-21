import unittest

from link import link
from sound import Sound

class TestLink(unittest.TestCase):
    def T(self, word, ipa, expected):
        result = list(link(word, ipa))
        self.assertEqual(result, expected)

    def test_silent_letter(self):
        self.T('know', 'n ə́w', [
            Sound('', 'k'),
            Sound('n', 'n'),
            Sound('əw', 'ow', stressed=True),
        ])
        self.T('island', 'ɑ́j l ə n d', [
            Sound('ɑj', 'i', stressed=True),
            Sound('', 's'),
            Sound('l', 'l'),
            Sound('ə', 'a'),
            Sound('n', 'n'),
            Sound('d', 'd'),
        ])
        self.T('climb', 'k l ɑ́j m', [
            Sound('k', 'c'),
            Sound('l', 'l'),
            Sound('ɑj', 'i', stressed=True),
            Sound('m', 'm'),
            Sound('', 'b'),
        ])

    def test_silent_letters(self):
        self.T('light', 'l ɑ́j t', [
            Sound('l', 'l'),
            Sound('ɑj', 'i', stressed=True),
            Sound('', 'gh'),
            Sound('t', 't'),
        ])
        self.T('restaurant', 'r ɛ́ s t r ɔ n t', [
            Sound('r', 'r'),
            Sound('ɛ', 'e', stressed=True),
            Sound('s', 's'),
            Sound('t', 't'),
            Sound('', 'au'),
            Sound('r', 'r'),
            Sound('ɔ', 'a'),
            Sound('n', 'n'),
            Sound('t', 't'),
        ])

    def test_silent_letter_in_specific_position(self):
        self.T('back', 'b á k', [
            Sound('b', 'b'),
            Sound('a', 'a', stressed=True),
            Sound('', 'c'), # not /k/
            Sound('k', 'k'),
        ])
        self.T('build', 'b ɪ́ l d', [
            Sound('b', 'b'),
            Sound('', 'u'), # not /ɪ/ as in "busy"
            Sound('ɪ', 'i', stressed=True),
            Sound('l', 'l'),
            Sound('d', 'd'),
        ])

    def test_unspelled_sound(self):
        self.T('length', 'l ɛ́ ŋ k θ', [
            Sound('l', 'l'),
            Sound('ɛ', 'e', stressed=True),
            Sound('ŋ', 'ng'),
            Sound('k', ''),
            Sound('θ', 'th'),
        ])

    def test_silent_letter_and_unspelled_sound(self):
        self.T('simple', 's ɪ́ m p ə l', [
            Sound('s', 's'),
            Sound('ɪ', 'i', stressed=True),
            Sound('m', 'm'),
            Sound('p', 'p'),
            Sound('ə', ''),
            Sound('l', 'l'),
            Sound('', 'e'),
        ])

    def test_silent_letter_before_unspelled_sound(self):
        self.T('castle', 'k ɑ́ː s ə l', [
            Sound('k', 'c'),
            Sound('ɑː', 'a', stressed=True),
            Sound('s', 's'),
            Sound('', 't'), # order matters here
            Sound('ə', ''), # order matters here
            Sound('l', 'l'),
            Sound('', 'e'),
        ])

    def test_avoid_silent_letter(self):
        self.T('area', 'ɛ́ː r ɪj ə', [
            Sound('ɛː', 'a', stressed=True),
            Sound('r', 'r'),
            Sound('ɪj', 'e'), # not <ea>
            Sound('ə', 'a'),
        ])

    def test_override_avoidance_of_silent_letter(self):
        self.T('barrier', 'b á r ɪj ə', [
            Sound('b', 'b'),
            Sound('a', 'a', stressed=True),
            Sound('r', 'rr'),
            Sound('ɪj', 'i'), # not <ie>
            Sound('ə', 'e'),
            Sound('', 'r'),
        ])

    def test_r_not_part_of_vowel(self):
        self.T('part', 'p ɑ́ː t', [
            Sound('p', 'p'),
            Sound('ɑː', 'a', stressed=True),
            Sound('', 'r'),
            Sound('t', 't'),
        ])

    def test_r_not_part_of_vowel_against_intuition(self):
        self.T('first', 'f ə́ː s t', [
            Sound('f', 'f'),
            Sound('əː', 'i', stressed=True),
            Sound('', 'r'),
            Sound('s', 's'),
            Sound('t', 't'),
        ])

    def test_r_not_even_part_of_silent_vowel(self):
        self.T('comfortable', 'k ʌ́ m f t ə b ə l', [
            Sound('k', 'c'),
            Sound('ʌ', 'o', stressed=True),
            Sound('m', 'm'),
            Sound('f', 'f'),
            Sound('', 'o'),
            Sound('', 'r'),
            Sound('t', 't'),
            Sound('ə', 'a'),
            Sound('b', 'b'),
            Sound('ə', ''),
            Sound('l', 'l'),
            Sound('', 'e'),
        ])

    def test_letter_with_multiple_sounds(self):
        self.T('box', 'b ɔ́ k s', [
            Sound('b', 'b'),
            Sound('ɔ', 'o', stressed=True),
            Sound('k', 'x'),
            Sound('s', '', cont=True),
        ])

    def test_avoid_runs_of_penalized_patterns(self):
        self.T('failure', 'f ɛ́j l j ə', [
            Sound('f', 'f'),
            Sound('ɛj', 'ai', stressed=True),
            Sound('l', 'l'),
            Sound('j', ''),
            Sound('ə', 'u'),
            Sound('', 'r'),
            Sound('', 'e'),
            # not <f ai l u r   e>
            #     /f ɛ́j l     j ə/
        ])

    def test_preserve_capital_letter(self):
        self.T('April', 'ɛ́j p r ɪ l', [
            Sound('ɛj', 'A', stressed=True),
            Sound('p', 'p'),
            Sound('r', 'r'),
            Sound('ɪ', 'i'),
            Sound('l', 'l'),
        ])
        self.T('Thursday', 'θ ə́ː z d ɛj', [
            Sound('θ', 'Th'),
            Sound('əː', 'u', stressed=True),
            Sound('', 'r'),
            Sound('z', 's'),
            Sound('d', 'd'),
            Sound('ɛj', 'ay'),
        ])

if __name__ == '__main__':
    unittest.main()

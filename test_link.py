import unittest

from link import link
from sound import Sound

class TestLink(unittest.TestCase):
    def T(self, word, ipa, expected):
        result = list(link(word, ipa))
        self.assertEqual(result, expected)

    def test_silent_letter(self):
        self.T('back', 'b á k', [
            Sound('b', 'b'),
            Sound('a', 'a', stressed=True),
            Sound('', 'c'),
            Sound('k', 'k'),
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

    def test_avoid_silent_letter(self):
        self.T('area', 'ɛ́ː r ɪj ə', [
            Sound('ɛː', 'a', stressed=True),
            Sound('r', 'r'),
            Sound('ɪj', 'e'), # not <ea>
            Sound('ə', 'a'),
        ])

if __name__ == '__main__':
    unittest.main()

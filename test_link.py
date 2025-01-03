import unittest

from link import link
from sound import Sound

class TestLink(unittest.TestCase):
    def T(self, word, ipa, expected):
        result = list(link(word, ipa))
        self.assertEqual(result, expected)

    def test_simple_case(self):
        self.T('a', 'ɛj', [
            Sound('ɛj', 'a'),
        ])

    def test_silent_letter_and_unspelled_sound(self):
        self.T('able', 'ɛ́j b ə l', [
            Sound('ɛj', 'a', stressed=True),
            Sound('b', 'b'),
            Sound('ə', ''),
            Sound('l', 'l'),
            Sound('', 'e'),
        ])

if __name__ == '__main__':
    unittest.main()

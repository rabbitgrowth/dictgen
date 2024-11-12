import unittest

from dictgen import gen

# TODO add stress to pronunciation

class TestDictgen(unittest.TestCase):
    def test_gen(self):
        tests = [
            ('cat', 'kat', {'KAT'}),
            ('car', 'kar', {'KAR'}),
            ('cart', 'kart', {'KART'}),

            ('strap', 'strap', {'STRAP'}),

            ('ha', 'ha', {'HA'}),
            ('haha', 'haha', {'HA/HA'}),
            ('hahaha', 'hahaha', {'HA/HA/HA'}),

            ('Gwen', 'gwɛn', {'TKPWU/WEPB'}),
            ('segue', 'sɛgwɛj', {'SEG/WAEU'}),

            ('sled', 'slɛd', {'SHRED'}),
            ('shred', 'ʃrɛd', {'SKHRED', 'SHU/RED'}),
        ]

        for word, pron, expected in tests:
            result = {'/'.join(map(str, outline)) for outline in gen(pron)}
            self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

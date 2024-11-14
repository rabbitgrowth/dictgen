import unittest

from dictgen import Stroke, destress, gen

class TestDictgen(unittest.TestCase):
    def test_gen(self):
        with open('test.txt') as f:
            pars = f.read().split('\n\n')
            for par in pars:
                par = par.strip()
                word, pron, *outlines = par.splitlines()
                letters = word.split()
                symbols = destress(pron).split()
                pairs = list(zip(letters, symbols, strict=True))
                result = set(map(tuple, gen(pairs)))
                expected = {
                    tuple(map(Stroke, outline.strip().split('/')))
                    for outline in outlines
                }
                self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

import unittest

from . import nirvana, \
    Not, And, Or, Xor


class TestNirvana(unittest.TestCase):
    def test_nand(self):
        self.assertEqual(True, nirvana.nand(False, False))
        self.assertEqual(True, nirvana.nand(True, False))
        self.assertEqual(True, nirvana.nand(False, True))
        self.assertEqual(False, nirvana.nand(True, True))


class TestChips(unittest.TestCase):
    def test_not(self):
        self.assertEqual(True, Not(False))
        self.assertEqual(False, Not(True))

    def test_and(self):
        self.assertEqual(False, And(False, False))
        self.assertEqual(False, And(True, False))
        self.assertEqual(False, And(False, True))
        self.assertEqual(True, And(True, True))

    def test_or(self):
        self.assertEqual(False, Or(False, False))
        self.assertEqual(True, Or(True, False))
        self.assertEqual(True, Or(False, True))
        self.assertEqual(True, Or(True, True))

    def test_xor(self):
        self.assertEqual(False, Xor(False, False))
        self.assertEqual(True, Xor(True, False))
        self.assertEqual(True, Xor(False, True))
        self.assertEqual(False, Xor(True, True))


if __name__ == '__main__':
    unittest.main()

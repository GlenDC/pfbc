from itertools import combinations_with_replacement
import unittest

from pfbc.hardware import nirvana
from pfbc.hardware.chips import \
    Not, And, Or, Xor, Mux, DMux, \
    Not16, And16, Or16, Mux16, \
    Or8Way, DMux4Way, DMux8Way, \
    Mux4Way16, Mux8Way16


class TestNirvana(unittest.TestCase):
    def test_nand(self):
        for (a, b) in combinations_with_replacement([False, True], 2):
            self.assertEqual(not(a and b), nirvana.nand(a, b))


class TestChips(unittest.TestCase):
    def test_not(self):
        for i in [False, True]:
            self.assertEqual(not(i), Not(i))

    def test_and(self):
        for (a, b) in combinations_with_replacement([False, True], 2):
            self.assertEqual(a and b, And(a, b))

    def test_or(self):
        for (a, b) in combinations_with_replacement([False, True], 2):
            self.assertEqual(a or b, Or(a, b))

    def test_xor(self):
        for (a, b) in combinations_with_replacement([False, True], 2):
            self.assertEqual(a^b, Xor(a, b))

    def test_mux(self):
        for (a, b, s) in combinations_with_replacement([False, True], 3):
            out = b if s else a
            self.assertEqual(out, Mux(a, b, s))

    def test_dmux(self):
        for (i, s) in combinations_with_replacement([False, True], 2):
            out = (0, i) if s else (i, 0)
            self.assertEqual(out, DMux(i, s))


class TestChipsBus(unittest.TestCase):
    def test_not16(self):
        for a in combinations_with_replacement([False, True], 16):
            out = tuple(not(x) for x in a)
            self.assertEqual(out, Not16(a))

    def test_and16(self):
        for t in combinations_with_replacement([False, True], 32):
            a, b = t[:16], t[16:]
            out = tuple(x and y for (x, y) in zip(a, b))
            self.assertEqual(out, And16(a, b))

    def test_or16(self):
        for t in combinations_with_replacement([False, True], 32):
            a, b = t[:16], t[16:]
            out = tuple(x or y for (x, y) in zip(a, b))
            self.assertEqual(out, Or16(a, b))

    def test_mux16(self):
        for t in combinations_with_replacement([False, True], 33):
            a, b = t[:16], t[16:32]
            s = t[-1]
            out = b if s else a
            self.assertEqual(out, Mux16(a, b, s))


class TestChipsMulti(unittest.TestCase):
    def test_or8way(self):
        for a in combinations_with_replacement([False, True], 8):
            out = any(a)
            self.assertEqual(out, Or8Way(a))

    def test_dmux4way(self):
        for (i, s0, s1) in combinations_with_replacement([False, True], 3):
            n = int(s0)<<1 | int(s1)
            out = tuple([0]*n + [i] + [0]*(3-n))
            self.assertEqual(out, DMux4Way(i, (s0, s1)))

    def test_dmux8way(self):
        for (i, s0, s1, s2) in combinations_with_replacement([False, True], 4):
            n = int(s0)<<2 | int(s1)<<1 | int(s2)
            out = tuple([0]*n + [i] + [0]*(7-n))
            self.assertEqual(out, DMux8Way(i, (s0, s1, s2)))


class TestChipsMultiBus(unittest.TestCase):
    def test_mux4way16(self):
        for t in combinations_with_replacement([False, True], (16*4)+2):
            inputs = [t[x:x+16] for x in range(0, len(t)-2, 16)]
            a, b, c, d = inputs
            s0, s1 = t[-2], t[-1]
            out = inputs[int(s0)<<1 | int(s1)]
            self.assertEqual(out, Mux4Way16(a, b, c, d, (s0, s1)))

    def test_mux8way16(self):
        for t in combinations_with_replacement([False, True], (16*8)+3):
            inputs = [t[x:x+16] for x in range(0, len(t)-3, 16)]
            a, b, c, d, e, f, g, h = inputs
            s0, s1, s2 = t[-3], t[-2], t[-1]
            out = inputs[int(s0)<<2 | int(s1)<<1 | int(s2)]
            self.assertEqual(out, Mux8Way16(a, b, c, d, e, f, g, h, (s0, s1, s2)))


if __name__ == '__main__':
    unittest.main()

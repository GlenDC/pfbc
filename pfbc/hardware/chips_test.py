from itertools import combinations
import unittest

from pfbc.hardware import nirvana
from pfbc.hardware.chips import \
    Not, And, Or, Xor, Mux, DMux, \
    Not16, And16, Or16, Mux16, \
    Or8Way, DMux4Way, DMux8Way, \
    Mux4Way16, Mux8Way16


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

    def test_mux(self):
        self.assertEqual(False, Mux(False, False, False))
        self.assertEqual(True, Mux(True, False, False))
        self.assertEqual(False, Mux(False, True, False))
        self.assertEqual(True, Mux(True, True, False))
        self.assertEqual(False, Mux(False, False, True))
        self.assertEqual(False, Mux(True, False, True))
        self.assertEqual(True, Mux(False, True, True))
        self.assertEqual(True, Mux(True, True, True))

    def test_dmux(self):
        self.assertEqual((False, False), DMux(False, False))
        self.assertEqual((False, False), DMux(False, True))
        self.assertEqual((True, False), DMux(True, False))
        self.assertEqual((False, True), DMux(True, True))


class TestChipsBus(unittest.TestCase):
    def test_not16(self):
        self.assertEqual(tuple([True]*16), Not16(tuple([False]*16)))
        self.assertEqual(tuple([False]*16), Not16(tuple([True]*16)))
        self.assertEqual(tuple([False, True]*8), Not16(tuple([True, False]*8)))
        self.assertEqual(tuple([True, False]*8), Not16(tuple([False, True]*8)))
        self.assertEqual(tuple([True]+([False]*14)+[True]), Not16(tuple([False]+([True]*14)+[False])))

    def test_and16(self):
        self.assertEqual(tuple([False]*16), And16((tuple([False]*16)), (tuple([False]*16))))
        self.assertEqual(tuple([False]*16), And16((tuple([True]*16)), (tuple([False]*16))))
        self.assertEqual(tuple([False]*16), And16((tuple([False]*16)), (tuple([True]*16))))
        self.assertEqual(tuple([True]*16), And16((tuple([True]*16)), (tuple([True]*16))))
        self.assertEqual(tuple([True, False]*8), And16(tuple([True, False]*8), tuple([True, False]*8)))
        self.assertEqual(tuple([False, True]*8), And16(tuple([False, True]*8), tuple([False, True]*8)))

    def test_or16(self):
        self.assertEqual(tuple([False]*16), Or16((tuple([False]*16)), (tuple([False]*16))))
        self.assertEqual(tuple([True]*16), Or16((tuple([True]*16)), (tuple([False]*16))))
        self.assertEqual(tuple([True]*16), Or16((tuple([False]*16)), (tuple([True]*16))))
        self.assertEqual(tuple([True]*16), Or16((tuple([True]*16)), (tuple([True]*16))))
        self.assertEqual(tuple([True, False]*8), Or16(tuple([True, False]*8), tuple([True, False]*8)))
        self.assertEqual(tuple([True]*16), Or16(tuple([True, False]*8), tuple([True, True]*8)))
        self.assertEqual(tuple([False, True]*8), Or16(tuple([False, True]*8), tuple([False, True]*8)))
        self.assertEqual(tuple([True]*16), Or16(tuple([True, True]*8), tuple([False, True]*8)))

    def test_mux16(self):
        self.assertEqual(tuple([False]*16), Mux16(tuple([False]*16), tuple([False]*16), False))
        self.assertEqual(tuple([True]*16), Mux16(tuple([True]*16), tuple([False]*16), False))
        self.assertEqual(tuple([False]*16), Mux16(tuple([False]*16), tuple([True]*16), False))
        self.assertEqual(tuple([True]*16), Mux16(tuple([True]*16), tuple([True]*16), False))
        self.assertEqual(tuple([False]*16), Mux16(tuple([False]*16), tuple([False]*16), True))
        self.assertEqual(tuple([False]*16), Mux16(tuple([True]*16), tuple([False]*16), True))
        self.assertEqual(tuple([True]*16), Mux16(tuple([False]*16), tuple([True]*16), True))
        self.assertEqual(tuple([True]*16), Mux16(tuple([True]*16), tuple([True]*16), True))
        self.assertEqual(tuple([False, True]*8), Mux16(tuple([False, True]*8), tuple([True, False]*8), False))
        self.assertEqual(tuple([True, False]*8), Mux16(tuple([False, True]*8), tuple([True, False]*8), True))


class TestChipsMulti(unittest.TestCase):
    def test_or8way(self):
        self.assertEqual(False, Or8Way(tuple([False]*8)))
        self.assertEqual(True, Or8Way(tuple([True]*8)))
        self.assertEqual(True, Or8Way(tuple([True]+([False]*7))))
        self.assertEqual(True, Or8Way(tuple([False, False, True]+([False]*5))))
        self.assertEqual(True, Or8Way(tuple(([False]*7)+[True])))
        self.assertEqual(True, Or8Way(tuple([False]+([True]*7))))

    def test_dmux4way(self):
        self.assertEqual(tuple([False, False, False, False]), DMux4Way(False, tuple([False, False])))
        self.assertEqual(tuple([False, False, False, False]), DMux4Way(False, tuple([True, False])))
        self.assertEqual(tuple([False, False, False, False]), DMux4Way(False, tuple([False, True])))
        self.assertEqual(tuple([False, False, False, False]), DMux4Way(False, tuple([True, True])))
        self.assertEqual(tuple([True, False, False, False]), DMux4Way(True, tuple([False, False])))
        self.assertEqual(tuple([False, True, False, False]), DMux4Way(True, tuple([False, True])))
        self.assertEqual(tuple([False, False, True, False]), DMux4Way(True, tuple([True, False])))
        self.assertEqual(tuple([False, False, False, True]), DMux4Way(True, tuple([True, True])))

    def test_dmux8way(self):
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([False, False, False])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([False, False, True])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([False, True, False])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([False, True, True])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([True, False, False])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([True, False, True])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([True, True, False])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, False]), DMux8Way(False, tuple([True, True, True])))
        self.assertEqual(tuple([True, False, False, False, False, False, False, False]), DMux8Way(True, tuple([False, False, False])))
        self.assertEqual(tuple([False, True, False, False, False, False, False, False]), DMux8Way(True, tuple([False, False, True])))
        self.assertEqual(tuple([False, False, True, False, False, False, False, False]), DMux8Way(True, tuple([False, True, False])))
        self.assertEqual(tuple([False, False, False, True, False, False, False, False]), DMux8Way(True, tuple([False, True, True])))
        self.assertEqual(tuple([False, False, False, False, True, False, False, False]), DMux8Way(True, tuple([True, False, False])))
        self.assertEqual(tuple([False, False, False, False, False, True, False, False]), DMux8Way(True, tuple([True, False, True])))
        self.assertEqual(tuple([False, False, False, False, False, False, True, False]), DMux8Way(True, tuple([True, True, False])))
        self.assertEqual(tuple([False, False, False, False, False, False, False, True]), DMux8Way(True, tuple([True, True, True])))


class TestChipsMultiBus(unittest.TestCase):
    def test_mux4way16(self):
        for t in combinations([False, True], (16*4)+2):
            inputs = [t[x:x+16] for x in xrange(0, len(t)-2, 16)]
            a, b, c, d = inputs
            s0, s1 = t[-2], t[-1]
            out = t[int(s0)<<1 + int(s1)]
            self.assertEqual(out, Mux4Way16(a, b, c, d, (s0, s1)))

    def test_mux8way16(self):
        for t in combinations([False, True], (16*8)+3):
            inputs = [t[x:x+16] for x in xrange(0, len(t)-3, 16)]
            a, b, c, d, e, f, g, h = inputs
            s0, s1, s2 = t[-3], t[-2], t[-1]
            out = t[int(s0)<<2 + int(s1)<<1 + int(s2)]
            self.assertEqual(out, Mux8Way16(a, b, c, d, e, f, g, h, (s0, s1, s2)))


if __name__ == '__main__':
    unittest.main()

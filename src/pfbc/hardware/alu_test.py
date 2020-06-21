from itertools import combinations_with_replacement
import unittest

from pfbc.hardware.alu import \
    adder_half, adder_full, \
    add16, inc16, \
    alu


class TestAdders(unittest.TestCase):
    def test_adder_half(self):
        for (a, b) in combinations_with_replacement([False, True], 2):
            x, y = int(a), int(b)
            t = x+y
            _sum, carry = bool(t%2), t>1
            self.assertEqual((_sum, carry), adder_half(a, b), f"{a}, {b} => {t} (= {x}+{y}), {_sum}, {carry}")

    def test_adder_full(self):
        for (a, b, c) in combinations_with_replacement([False, True], 3):
            x, y, z = int(a), int(b), int(c)
            t = x+y+z
            _sum, carry = bool(t%2), t>1
            self.assertEqual((_sum, carry), adder_full(a, b, c), f"{a}, {b}, {c} => {t} (= {x}+{y}+{z}), {_sum}, {carry}")

    def test_add16(self):
        for s in combinations_with_replacement(['0', '1'], 32):
            a, b = s[:16], s[16:]
            s = int(''.join(a), 2) + int(''.join(b), 2)
            r = "{0:b}".format(s)
            if len(r) > 16:
                r = r[-16:]
            elif len(r) < 16:
                r = '0'*(16-len(r)) + r
            result = tuple(bool(int(c)) for c in r)
            self.assertEqual(result, add16([x == '1' for x in a], [x == '1' for x in b]), f"{''.join(a)} + {''.join(b)} = {s} = {r} = {result}")

    def test_inc16(self):
        for a in combinations_with_replacement(['0', '1'], 16):
            s = int(''.join(a), 2) + 1
            r = "{0:b}".format(s)
            if len(r) > 16:
                r = r[-16:]
            elif len(r) < 16:
                r = '0'*(16-len(r)) + r
            result = tuple(bool(int(c)) for c in r)
            self.assertEqual(result, inc16([x == '1' for x in a]), f"{''.join(a)} + 1 = {s} = {r} = {result}")


class TestALU(unittest.TestCase):
    def test_alu(self):
        pass  # TODO

from typing import Tuple, NewType

from pfbc.hardware import nirvana


Bit = NewType('Bit', bool)
Bus16 = Tuple[
    Bit, Bit, Bit, Bit,
    Bit, Bit, Bit, Bit,
    Bit, Bit, Bit, Bit,
    Bit, Bit, Bit, Bit,
    ]
Bus8 = Tuple[
    Bit, Bit, Bit, Bit,
    Bit, Bit, Bit, Bit,
    ]
Bus4 = Tuple[Bit, Bit, Bit, Bit]
Bus3 = Tuple[Bit, Bit, Bit]
Bus2 = Tuple[Bit, Bit]


def FanOut16(bit: Bit) -> Bus16:
    return tuple([bit]*16)


def Not(i: Bit) -> Bit:
    return nirvana.nand(i, i)


def And(a: Bit, b: Bit) -> Bit:
    out = nirvana.nand(a, b)
    return Not(out)


def Or(a: Bit, b: Bit) -> Bit:
    x = Not(a)
    y = Not(b)
    return nirvana.nand(x, y)


def Xor(a: Bit, b: Bit) -> Bit:
    x = nirvana.nand(a, b)
    y = Or(a, b)
    return And(x, y)


def Mux(a: Bit, b: Bit, s: Bit) -> Bit:
    x = And(a, Not(s))
    y = And(b, s)
    return Or(x, y)


def DMux(i: Bit, s: Bit) -> Bus2:
    return tuple((
        And(i, Not(s)),
        And(i, s),
    ))


def Not16(a: Bus16) -> Bus16:
    return tuple((Not(x) for x in a))


def And16(a: Bus16, b: Bus16) -> Bus16:
    return tuple((And(x, y) for (x, y) in zip(a, b)))


def Or16(a: Bus16, b: Bus16) -> Bus16:
    return tuple((Or(x, y) for (x, y) in zip(a, b)))


def Mux16(a: Bus16, b: Bus16, s: Bit) -> Bus16:
    return tuple((Mux(x, y, s) for (x, y) in zip(a, b)))


def Or8Way(a: Bus8) -> Bit:
    out = Or(a[0], a[1])
    for x in a[2:]:
        out = Or(out, x)
    return out


def Mux4Way16(a: Bus16, b: Bus16, c: Bus16, d: Bus16, s: Bus2) -> Bus16: # TODO: test
    return Or16(
        And16(a, And16(Not16(FanOut16(s[0])), Not16(FanOut16(s[1])))),
        Or16(
            And16(b, And16(Not16(FanOut16(s[0])), FanOut16(s[1]))),
            Or16(
                And16(c, And16(FanOut16(s[0]), Not16(FanOut16(s[1])))),
                And16(d, And16(FanOut16(s[0]), FanOut16(s[1]))),
            ),
        ),
    )


def Mux8Way16(a: Bus16, b: Bus16, c: Bus16, d: Bus16, e: Bus16, f: Bus16, g: Bus16, h: Bus16, s: Bus3) -> Bus16:
    return Or16(
        And16(Not16(FanOut16(s[0])), Mux4Way16(a, b, c, d, tuple(s[1:]))),
        And16(FanOut16(s[0]), Mux4Way16(e, f, g, h, tuple(s[1:]))),
    )


def DMux4Way(i: Bit, s: Bus2) -> Bus4:
    return DMux(And(Not(s[0]), i), s[1]) + \
        DMux(And(s[0], i), s[1])


def DMux8Way(i: Bit, s: Bus3) -> Bus8:
    return DMux4Way(And(Not(s[0]), i), s[1:]) + \
        DMux4Way(And(s[0], i), s[1:])

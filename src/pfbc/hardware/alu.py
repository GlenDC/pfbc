"""
alu.py ... # TODO
# TODO explain about ALU, part in hardware (also relationship to CPU),

implement 2 complement integer,
why this (e.g. what about the naive solution where MSb=sign)

explain how bool arithmetic works as it works
explain why 2 complement implementation works as-is for neg numbers,
as if these numbers were positive numbers

# ...
"""

from pfbc.hardware.chips import \
    Bit, Bus2, Bus16, \
    Xor, And, Or


def adder_half(a: Bit, b: Bit) -> Bus2:
    """
    Computes the sum of two bits

    IN a, b;    // 1-bit inputs
    OUT sum,    // Right bit of a + 
    carry;      // Left bit of a + b
    """
    _sum = Xor(a, b)
    carry = And(a, b)
    return _sum, carry


def adder_full(a: Bit, b: Bit, c: Bit) -> Bus2:
    """
    Computes the sum of three bits

    IN a, b, c;  // 1-bit inputs
    OUT sum,     // Right bit of a + b + 
    carry;       // Left bit of a + b + c

    There might be a better implementation possible
    upon further analysis.
    """
    sum_a_b, carry_a_b = adder_half(a, b)
    sum_a_b_c, carry_a_b_c = adder_half(sum_a_b, c)
    carry = Or(carry_a_b, carry_a_b_c)
    return sum_a_b_c, carry


def add16(a: Bus16, b: Bus16) -> Bus16:
    """
    Adds two 16-bit values

    The most significant carry bit is ignored.

    The implementation for this method is in a very naive way,
    where the signal has to cross a lot of different connections and chips.
    A more efficient implementation is possible by not letting the carry bit
    travel through each position but instead see it as a separate line.
    Such a solution is less obvious however.

    IN  a[16], b[16];
    OUT out[16];
    """
    o15, c = adder_half(a[15], b[15])
    out = [False]*15 + [o15]
    for i in range(1, 16):
        pos = 15-i
        out[pos], c = adder_full(a[pos], b[pos], c)
    return tuple(out)


def inc16(a: Bus16) -> Bus16:
    """
    16-bit incrementer

    out = in + 1 (arithmetic addition)

    The implementation for this method is done so in a very naive way,
    piggy-backing fully on the add16 chip functionality.
    This special edge case however can be implemented more efficiently.

    IN in[16];
    OUT out[16];
    """
    return add16(a, tuple([False]*15+[True]))


def alu(x: Bus16, y: Bus16, zx: Bit, nx: Bit, zy: Bit, ny: Bit, f: Bit, no: Bit) -> (Bus16, Bit, Bit):
    """
    The ALU (Arithmetic Logic Unit)

    Computes one of the following functions:
    x+y, x-y, y-x, 0, 1, -1, x, y, -x, -y, !x, !y,
    x+1, y+1, x-1, y-1, x&y, x|y on two 16-bit inputs, 
    according to 6 input bits denoted zx,nx,zy,ny,f,no.
    In addition, the ALU computes two 1-bit outputs:
    if the ALU output == 0, zr is set to 1; otherwise zr is set to 0;
    if the ALU output < 0, ng is set to 1; otherwise ng is set to 0.

    Implementation: the ALU logic manipulates the x and y inputs
    and operates on the resulting values, as follows:
    if (zx == 1) set x = 0        // 16-bit constant
    if (nx == 1) set x = !x       // bitwise not
    if (zy == 1) set y = 0        // 16-bit constant
    if (ny == 1) set y = !y       // bitwise not
    if (f == 1)  set out = x + y  // integer 2's complement addition
    if (f == 0)  set out = x & y  // bitwise and
    if (no == 1) set out = !out   // bitwise not
    if (out == 0) set zr = 1
    if (out < 0) set ng = 1

    IN:
    x[16], y[16],  // 16-bit inputs        
    zx, // zero the x input?
    nx, // negate the x input?
    zy, // zero the y input?
    ny, // negate the y input?
    f,  // compute out = x + y (if 1) or x & y (if 0)
    no; // negate the out output?

    OUT:
    out[16], // 16-bit output
    zr, // 1 if (out == 0), 0 otherwise
    ng; // 1 if (out < 0),  0 otherwise
    """
    raise NotImplementedError  # TODO

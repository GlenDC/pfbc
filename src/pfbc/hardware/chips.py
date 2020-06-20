"""
chips.py contains all the chips (logical gates)
implementations used as the most primitive building
blocks for everything else.

All these chips are so called
composite gates implemented using only the gates
implemented in this chips as well as the elementary
NAND gate/chip which we'll take as if given by God.

> You can find the source code for the NAND gate
> in the ./src/nirvana directory should you want to know.

The NAND gate is implemented as a C extension
— not because of performance reasons— but as to clearly
highlight that we won't go deeper than this chips.py file
and that starting from the NAND gate we considering everything
from that level and lower as a blackbox. We'll
assume that the electrical engineers and physicists
can handle these lower layers just fine without
a nosy bunch of hackers poking around there.

Some chips manipulate a single bit while other
manipulate a group of bits, called a bus.

The actual implementation of these chips can
— from a Python POV — be implemented a lot more
performant, but that is not the point. The goal
of this project — and as such this module — is
to build a 16-bit computer starting from a NAND
gate and building up, as if it were a real physical
computer. As to demystify the complex system
a modern computer really is.
"""


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


def __fanOut16(bit: Bit) -> Bus16:
    """
    Use a single bit for multiple inputs (called a bus).
    """
    return tuple([bit]*16)


def Not(i: Bit) -> Bit:
    """
    Not gate

    out = not in

    ```
         +--------+  
    i +--+        |  
         |  NAND  +--+ out
    i +--+        |  
         +--------+  
    ```
    """
    return nirvana.nand(i, i)


def And(a: Bit, b: Bit) -> Bit:
    """
    And gate

    out = True if (a == True and b == True)
    , False otherwise


    ```
         +--------+   +-------+
    a +--+        |   |       |
         |  NAND  +---+  NOT  +--+ out
    b +--+        |   |       |
         +--------+   +-------+
    ```
    """
    out = nirvana.nand(a, b)
    return Not(out)


def Or(a: Bit, b: Bit) -> Bit:
    """
    Or gate

    out = True if (a == True or b == True)
    , False otherwise

    ```
         +-------+
         |       |
    a +--+  NOT  +--+  +--------+
         |       |  +--+        |
         +-------+     |  NAND  +--+ out
                   +---+        |
         +-------+ |   +--------+
         |       | |
    b +--+  NOT  +-+
         |       |
         +-------+
    ```
    """
    x = Not(a)
    y = Not(b)
    return nirvana.nand(x, y)


def Xor(a: Bit, b: Bit) -> Bit:
    """
    Exclusive-or gate

    out = not (a == b)

    ```
                +--------+
    a +----+----+        |
           |    |  NAND  +--+  +-------+
           | +--+        |  +--+       |
           | |  +--------+     |  AND  +--+ out
           | |             +---+       |
           | |    +------+ |   +-------+
           +------+      | |
             |    |  OR  +-+
    b +------+----+      |
                  +------+
    ```
    """
    x = nirvana.nand(a, b)
    y = Or(a, b)
    return And(x, y)


def Mux(a: Bit, b: Bit, s: Bit) -> Bit:
    """
    Multiplexor

    out = a if sel == 0
    , b otherwise

    ```
                         +-------+
                    a +--+       |
                         |  AND  +--+
           +-------+  +--+       |  |
           |       |  |  +-------+  |
        +--+  NOT  +--+             |   +------+
        |  |       |                +---+      |
        |  +-------+                    |  OR  +--+ out
        |                            +--+      |
        |                 +-------+  |  +------+
    s +-------------------+       |  |
                          |  AND  +--+
                     b +--+       |
                          +-------+
    ```
    """
    x = And(a, Not(s))
    y = And(b, s)
    return Or(x, y)


def DMux(i: Bit, s: Bit) -> Bus2:
    """
    Demultiplexor

    {a, b} = {in, 0} if sel == 0
    , {0, in} if sel == 1

    ```
                                +-------+
    i +-+-----------------------+       |
        |                       |  AND  +--+  out[0]
        |         +-------+  +--+       |
        |         |       |  |  +-------+
        |         |  NOT  +--+
        |       +-+       |
        |       | +-------+
        |       |               +-------+
        |  s +--+---------------+       |
        |                       |  AND  +--+  out[1]
        +-----------------------+       |
                                +-------+
    ```
    """
    return tuple((
        And(i, Not(s)),
        And(i, s),
    ))


def Not16(a: Bus16) -> Bus16:
    """
    16-bit Not

    for i=0..15: out[i] = not a[i]

    ```
           +-------+ 
           |       | 
    a[0] --+  NOT  +-- out[0]
           |       |
           +-------+

           +-------+ 
           |       | 
    a[1] --+  NOT  +-- out[1]
           |       |
           +-------+

    ...

            +-------+ 
            |       | 
    a[15] --+  NOT  +-- out[15]
            |       |
            +-------+
    ```
    """
    return tuple((Not(x) for x in a))


def And16(a: Bus16, b: Bus16) -> Bus16:
    """
    16-bit bitwise And

    for i = 0..15: out[i] = (a[i] and b[i])

    ```
           +-------+
    a[0] --+       |
           |  AND  +--+ out[0]
    b[0] --+       |
           +-------+

           +-------+
    a[1] --+       |
           |  AND  +--+ out[1]
    b[1] --+       |
           +-------+

    ...

            +-------+
    a[15] --+       |
            |  AND  +--+ out[15]
    b[15] --+       |
            +-------+
    ```
    """
    return tuple((And(x, y) for (x, y) in zip(a, b)))


def Or16(a: Bus16, b: Bus16) -> Bus16:
    """
    16-bit bitwise Or

    for i = 0..15: out[i] = (a[i] or b[i])

    ```
           +------+
    a[0] --+      |
           |  OR  +--+ out[0]
    b[0] --+      |
           +------+

           +------+
    a[1] --+      |
           |  OR  +--+ out[1]
    b[1] --+      |
           +------+

    ...

            +------+
    a[15] --+      |
            |  OR  +--+ out[15]
    b[15] --+      |
            +------+
    ```
    """
    return tuple((Or(x, y) for (x, y) in zip(a, b)))


def Mux16(a: Bus16, b: Bus16, s: Bit) -> Bus16:
    """
    16-bit multiplexor

    for i = 0..15 out[i] = a[i] if sel == 0
    , b[i] if sel == 1

    ```
                +-------+
         a[0] --+       |
                |  MUX  +--+ out[0]
         b[0] --+       |
                +---+---+
                    |
    s -+------------+
       |            |
       |        +---+---+
       | a[1] --+       |
       |        |  MUX  +--+ out[1]
       | b[1] --+       |
       |        +-------+
       |
       +---------- ...
       |  
       |         +-------+
       | a[15] --+       |
       |         |  MUX  +--+ out[15]
       | b[15] --+       |
       |         +---+---+
       |             |
       +-------------+
    ```
    """
    return tuple((Mux(x, y, s) for (x, y) in zip(a, b)))


def Or8Way(a: Bus8) -> Bit:
    """
    8-way Or

    out = (a[0] or a[1] or ... or a[7])

    ```
                     a[2]
                      +  +------+
          +------+    +--+      |
   a[0] +-+      |       |  OR  +--+
          |  OR  +-------+      |  |
   a[1] +-+      |       +------+  |
          +------+                 |
                         +------+  |
          +------+       |      +--+
          |      +-------+  OR  |
       +--+  OR  |       |      +--+ a[3]
       |  |      +---+   +------+
       |  +------+   +           a[7]
       |            a[4]          +
       |  +------+                | +------+
       +--+      |      +------+  +-+      |
          |  OR  +------+      |    |  OR  |
  a[5] +--+      |      |  OR  +----+      |
          +------+   +--+      |    +---+--+
                     +  +------+        |
                    a[6]                +
                                       out
    ```
    """
    out = Or(a[0], a[1])
    for x in a[2:]:
        out = Or(out, x)
    return out


def Mux4Way16(a: Bus16, b: Bus16, c: Bus16, d: Bus16, s: Bus2) -> Bus16:
    """
    4-way 16-bit multiplexor

    out = a if sel == 00
    , b if sel == 01
    , c if sel == 10
    , d if sel == 11

    ```
                                                    s[1]     +------------------+
                                                      +      |                  |
                                                      |      |        s[0]      |
                                                      |      |          +       |
                                                      |      |          |       |
                                                      |      |          |       |
                                                      |      |          |       |
                                                      |      |          |       |
                                                      |      |          |       |
                                                      |      |          |       |
                                                      |      |          |       |
                                      +---------+     |      |          |       |
                                      |         |     |      |  +-------+       |
       +-------------------+----------+   NOT   +-----*------+  |       |       |
       |                   |          |         |     |         |  +----+----+  |
       |                   |          +---------+     |         |  |         |  |
       |                   |                          |         |  |   NOT   |  |
       |                   |   +--------------------------------+  |         |  |
       |                   |   |                      |         |  +----+----+  |
       |                   |   |                      |         |       |       |
       |                   |   |                      |         |       |       |
       |                   |   |                      |         |       |       |
       |   +------------------------------------------------------------+       |
       |   |               |   |                      |         |       |       |
       |   |               |   |                      |         |       |       |
       |   |               |   |                      |         |       |       |
       |   |               |   |                  +---+         |       |       |
       |   |               |   |                  |             |       |       |
       |   |               |   |                  |    +--------+       |   +---+
       |   |               |   |                  |    |                |   |
       |   |               |   |                  |    |                |   |
    +--+---+--+         +--+---+--+             +-+----+--+         +---+---+-+
    |         |         |         |             |         |         |         |
    |   AND   |         |   AND   |          +--+   AND   |         |   AND   |
    |         |         |         |          |  |         |         |         |
    +----+----+         +----+----+          |  +---------+         +----+----+
         |                   |            16 /                           |
      16 /      16        16 /      16       |        16            16   |
         |   +--/--+ a       |   +--/-+ b    +--+   +-/--+ d   c +--/-+  / 16
         |   |               |   |              |   |                 |  |
      +--+---+--+         +--+---+--+        +--+---+--+           +--+--+---+
      |         |         |         |        |         |           |         |
      |  AND16  |         |  AND16  |        |  AND16  |           |  AND16  |
      |         |         |         |        |         |           |         |
      +---+-----+         +-----+---+        +----+----+           +-----+---+
          |                     |                 |   16           16    |
          |   16          16    |                 +---/---+   +----/-----+
          +---/---+   +---/-----+                         |   |
                  |   |                                   |   |
               +--+---+-+          +--------+          +--+---+-+
               |        |    16    |        |     16   |        |
               |  OR16  +-----/----+  OR16  +-----/----+  OR16  |
               |        |          |        |          |        |
               +--------+          +---+----+          +--------+
                                       |
                                       / 16
                                       |
                                       +
                                      out
    ```
    """
    ns0, ns1 = Not(s[0]), Not(s[1])
    ns0f, ns1f = __fanOut16(ns0), __fanOut16(ns1)
    s0f, s1f = __fanOut16(s[0]), __fanOut16(s[1])
    return Or16(
        Or16(
            And16(a, And16(ns1f, ns0f)),
            And16(b, And16(ns1f, s0f)),
        ),
        Or16(
            And16(c, And16(s1f, ns0f)),
            And16(d, And16(s1f, s0f)),
        ),
    )


def Mux8Way16(a: Bus16, b: Bus16, c: Bus16, d: Bus16, e: Bus16, f: Bus16, g: Bus16, h: Bus16, s: Bus3) -> Bus16:
    """
    8-way 16-bit multiple

    out = a if sel == 000
    , b if sel == 001
    , ...
    , h if sel == 111

    ```
                                                  s
                16                 16     1    +-----+
         +------/-------------+----/--x---/----+2|1|0|
         |                    |                +--+-++
         |                    |       16          | |
         |                    +-------/------------------+
         |                                        | |    |
         |                    +-------------------+ |    |
         |                    |                   | |    |
         |                    | +-------------------+    |
         |                    | |                 | |    |
         |         a  b  c  d | |      e  f  g  h | |    |
         |         +  +  +  + | |      +  +  +  + | |    |
         |         |  |  |  | | |      |  |  |  | | |    |
         |       16/16/16/16/ | |    16/16/16/16/ | |    |
         |         |  |  |  | | |      |  |  |  | | |    |
    +----+----+  +-+--+--+--+-+-+-+  +-+--+--+--+-+-+-+  |
    |         |  |                |  |                |  |
    |  NOT16  |  |  MUX_4_WAY_16  |  |  MUX_4_WAY_16  |  |
    |         |  |                |  |                |  |
    +----+----+  +-------+--------+  +-------+--------+  |
         |               |                   |           |
         /16             /16                 /16         |
         |               |                   |       +---+
         +--------+   +--+                   +---+   |
                  |   |                          |   |
               +--+---+--+     +--------+     +--+---+--+
               |         | 16  |        | 16  |         |
               |  AND16  +-/---+  OR16  +-/---+  AND16  |
               |         |     |        |     |         |
               +---------+     +----+---+     +---------+
                                    |
                                    /16
                                    |
                                    +
                                   out
    ```
    """
    s2 = __fanOut16(s[2])
    s = tuple(s[0:2])
    return Or16(
        And16(Not16(s2), Mux4Way16(a, b, c, d, s)),
        And16(s2, Mux4Way16(e, f, g, h, s)),
    )


def DMux4Way(i: Bit, s: Bus2) -> Bus4:
    """
    4-way demultiplexor

    {a, b, c, d} = {in, 0, 0, 0} if sel == 00
    , {0, in, 0, 0} if sel == 01
    , {0, 0, in, 0} if sel == 10
    , {0, 0, 0, in} if sel == 11

    ```
       +--------------+--+ i
       |              |       s
       |   +-------+  |    +---+
       |   |       +-----+-+1|0|
       |   |  NOT  |  |  | +--++
       |   |       |  |  |    |
       |   +---+---+  |  |    |
       |       |      |  |    |
       |  +----+      |  |    |
       |  |           |  |    |
    +--+--+-+      +--+--+-+  |
    |       |      |       |  |
    |  AND  |      |  AND  |  |
    |       |      |       |  |
    +---+---+      +---+---+  |
        |              |      |
        |      +--------------+
        |      |       |      |
    +---+----+ |   +---+----+ |
    |        | |   |        | |
    |  DMUX  +-+   |  DMUX  +-+
    |        |     |        |
    +--+--+--+     +--+--+--+
       |  |           |  |
       +  +           +  +
       a  b           c  d
    ```
    """
    return DMux(And(Not(s[1]), i), s[0]) + \
        DMux(And(s[1], i), s[0])


def DMux8Way(i: Bit, s: Bus3) -> Bus8:
    """
    8-way demultiplexor

    {a, b, c, d, e, f, g, h} = {in, 0, 0, 0, 0, 0, 0, 0} if sel == 000
    , {0, in, 0, 0, 0, 0, 0, 0} if sel == 001
    , ...
    , {0, 0, 0, 0, 0, 0, 0, in} if sel == 111

    ```
         +------------------+--+ i
         |                  |       s
         |       +-------+  |    +-----+
         |  +----+       +-----+-+2|1|0|
         |  |    |  NOT  |  |  | +--+-++
         |  |    |       |  |  |    | |
         |  |    +-------+  |  |    | |
         |  |               |  |    | |
         |  |               |  |    | |
         |  |               |  |    | |
      +--+--+-+          +--+--+-+  | |
      |       |          |       |  | |
      |  AND  |          |  AND  |  | |
      |       |          |       |  | |
      +---+---+          +---+---+  | |
          |                  |      | |
          |    +--------------------+ |
          |    |             |      | |
          |    | +--------------------+
          |    | |           |      | |
    +-----+----+-+-+     +---+------+-+-+
    |              |     |              |
    |  DMUX_4_WAY  |     |  DMUX_4_WAY  |
    |              |     |              |
    +--+--+--+--+--+     +--+--+--+--+--+
       |  |  |  |           |  |  |  |
       +  +  +  +           +  +  +  +
       a  b  c  d           e  f  g  h
    ```
    """
    return DMux4Way(And(Not(s[0]), i), s[1:]) + \
        DMux4Way(And(s[0], i), s[1:])

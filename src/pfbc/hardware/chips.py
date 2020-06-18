from typing import Tuple, NewType

from pfbc.hardware import nirvana

# TODO: add package and function docs!!!
# function docs should include ASCII graph with logic,
# as well as desired functionality


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
                    a[6]                 +
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
                                                    s[0]     +------------------+
                                                      +      |                  |
                                                      |      |        s[1]      |
                                                      |      |          +       |
                                                      / 1    |          |       |
                                                      |      |          / 1     |
                                                      |      |          |       |
                                                      x      |          |       |
                                                      |      |          x       |
                                                      |      |          |       |
                                                      / 16   |          / 16    |
                                      +---------+     +      |          |       |
                 16              16   |         |     |      |  +-------+       |
       +---------/---------+-----/----+  NOT16  +-----*------+  |       |       |
       |                   |          |         |     |         |  +----+----+  |
       |                16 /          +---------+     |         |  |         |  |
       |                   |                          |         |  |  NOT16  |  |
       |                   |   +------------/-------------------+  |         |  |
       |                   |   |            16        |         |  +----+----+  |
       |                   |   |                      |         |       |       |
       |                   |   |                      / 16      |       |       |
       |                   |   |          16          |         |       |       / 16
       |   +------------------------------/-----------------------------+       |
       |   |               |   |                      |         |       |       |
       |   |               |   |                      |         / 16    / 16    |
       |   |               |   |                      |         |       |       |
       |   |               |   |                  +---+         |       |       |
       |   |               |   |                  |             |       |       |
       |   |               |   |                  |    +--------+       |   +---+
       |   |               |   |                  |    |                |   |
       |   |               |   |                  |    |                |   |
    +--+---+--+         +--+---+--+             +-+----+--+         +---+---+-+
    |         |         |         |             |         |         |         |
    |  AND16  |         |  AND16  |          +--+  AND16  |         |  AND16  |
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
    s0, s1 = __fanOut16(s[0]), _fanOut16(s[1])
    ns0, ns1 = Not16(s0), Not16(s1)
    return Or16(
        Or16(
            And16(a, And16(ns0, ns1)),
            And16(b, And16(ns0, s1)),
        ),
        Or16(
            And16(c, And16(s0, ns1)),
            And16(d, And16(s0, s1)),
        ),
    )


def Mux8Way16(a: Bus16, b: Bus16, c: Bus16, d: Bus16, e: Bus16, f: Bus16, g: Bus16, h: Bus16, s: Bus3) -> Bus16:
    return Or16(
        And16(Not16(__fanOut16(s[0])), Mux4Way16(a, b, c, d, tuple(s[1:]))),
        And16(__fanOut16(s[0]), Mux4Way16(e, f, g, h, tuple(s[1:]))),
    )


def DMux4Way(i: Bit, s: Bus2) -> Bus4:
    return DMux(And(Not(s[0]), i), s[1]) + \
        DMux(And(s[0], i), s[1])


def DMux8Way(i: Bit, s: Bus3) -> Bus8:
    return DMux4Way(And(Not(s[0]), i), s[1:]) + \
        DMux4Way(And(s[0], i), s[1:])

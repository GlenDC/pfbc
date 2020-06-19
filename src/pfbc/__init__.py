"""
pfbc (Python 16-bit Computer) implements a 16-bit computer
build from the ground up as if were an actual modern 16-bit computer.

The design is a direct copy of the HACK computer
as described and taught at http://nand2tetris.org.
A big shout out to the team over there for making
this content as accessible as it is. Thank you very much!

Designing a computer is a trade-off between hardware and software.
What is not implemented in hardware can be emulated in software.
As such, to keep it as simple as possible, the hardware (such as the ALU)
is fairly primitive, knowing very well that we can polyfill the missing parts
in our software layer.

In the "hardware" module you'll find all sub modules that form
taken together the physical machine. The "software" module
contains all the sub modules that form taken together the software
running on the machine (including a high level language that allows
you to program modern applications, as well as some example applications).
"""

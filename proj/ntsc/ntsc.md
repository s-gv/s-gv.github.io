# All Digital NTSC Color
*July 13, 2014*

Generate NTSC color signal using only digital integrated circuits. An 8-bit
microcontroller (Atmega16) and a shift register (74LS195) are used to produce
NTSC color signal compatible with modern flat screen TVs. The schematic and
source code are [here](https://github.com/s-gv/ntsc-avr).

## What colors can it produce?

Below is a sample palette produced by this technique.

![Sample](/proj/ntsc/1.jpg)

## How to use

Build the circuit in the schematic below and program the microcontroller with
the binary file in the [repository](https://github.com/s-gv/ntsc-avr/tree/master/bin).
Hook it up to a TV, and you should see a color palette.

![Circuit](/proj/ntsc/2.jpg)

## How does it work?

NTSC color works by superposing a 3.579545 MHz sub-carrier wave on top of the
Black and White NTSC signal. The phase of the subcarrier indicates the color of
the "pixel".

A 14.31818 MHz clock, which is 4 times the sub-carrier frequency, is passed
through a shift register to generate 4 phases the sub-carrier. The amplitude of
these phases in the output signal is controlled by the microcontroller. Thus,
different amounts of the in-phase and quadrature components can be added to
obtain different colors.

This [series](http://sagargv.blogspot.com/2014/07/ntsc-demystified-color-demo-with.html)
of blog posts describes NTSC signals in more detail.

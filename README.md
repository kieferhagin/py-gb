# py-gb

## Goal
This is a programming exercize and labor of love for a man who just fricken loves the Gameboy,
emulation, and Python is okay too.

We will attempt to emulate every component of the Nintendo Gameboy's modified Z80 architecture,
including Gameboy Color functionality.

The first checkpoint will be getting the Nintendo Logo to appear on screen and meeting those
minimum requirements. Having attempted this in Javascript (and being met with failure), I believe
those requirements are, at a high level:

- CPU emulation through BIOS sequence
- GPU emulation with background and tilemaps working
- A very basic canvas to render onto
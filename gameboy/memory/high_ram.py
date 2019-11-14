from gameboy.memory.memory_region import MemoryRegion


class HighRAM(MemoryRegion):
    def __init__(self):
        super().__init__(bytearray(127), 0xFF80)

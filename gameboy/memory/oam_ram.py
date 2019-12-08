from gameboy.memory.memory_region import MemoryRegion


class OAMRam(MemoryRegion):
    def __init__(self):
        super().__init__(bytearray(160), 0xFE00)

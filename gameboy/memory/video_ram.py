from gameboy.memory.memory_region import MemoryRegion


class VideoRAM(MemoryRegion):
    def __init__(self):
        super().__init__(bytearray(8192), 0x8000)

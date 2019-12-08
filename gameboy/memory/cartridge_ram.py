from gameboy.memory.memory_region import MemoryRegion


class CartridgeRAM(MemoryRegion):
    def __init__(self, size: int):
        super().__init__(bytearray(size), 0xA000)

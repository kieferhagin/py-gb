from gameboy.memory_region import MemoryRegion


class ROM(MemoryRegion):
    def __init__(self, data: bytearray):
        super().__init__(data, 0xFFFF)

    def get_title(self) -> str:
        return self.read_byte_range(0x0134, 14).decode('ascii')

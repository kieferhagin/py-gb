class MemoryRegion:
    def __init__(self, data: bytearray, base_address: int):
        self._data = data
        self._base_address = base_address

    def read_byte(self, address: int) -> int:
        return self._data[(address - self._base_address) % len(self._data)]

    def write_byte(self, address: int, value: int):
        self._data[address - self._base_address] = value

    def read_word(self, address: int):
        return self.read_byte(address) + ((self.read_byte(address + 1)) << 8)

    def write_word(self, address, value):
        self.write_byte(address, value & 255)
        self.write_byte(address + 1, (value >> 8))

    def read_byte_range(self, address_start, length):
        start_index = address_start - self._base_address
        return self._data[start_index: start_index + length]

from gameboy.memory.memory_region import MemoryRegion


class IORAM(MemoryRegion):
    def __init__(self):
        super().__init__(bytearray(128), 0xFF00)

        self._boot_rom_locked: bool = False

    def get_boot_ram_locked(self) -> bool:
        return self._boot_rom_locked

    def write_byte(self, address: int, value: int):
        if address == 0xFF50:  # Boot ROM lock
            self._boot_rom_locked = True

            return

        if address == 0xFF41:  # LCD State
            current_lcd_state = self._data[0x41]
            super().write_byte(address, (current_lcd_state & 0x3) | (value & ~0x3))

            return

        if address == 0xFF44:  # LCD Y
            super().write_byte(address, 0)

            return

        return super().write_byte(address, value)

    def read_byte(self, address: int):
        if address == 0xFF50:  # Boot ROM Lock
            return 0xFF if self._boot_rom_locked else 0xFE

        return super().read_byte(address)

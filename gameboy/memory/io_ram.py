from enum import Enum

from gameboy.memory.memory_region import MemoryRegion


class IORAM(MemoryRegion):
    class LCDMode(Enum):
        LCD_HBLANK = 0
        LCD_VBLANK = 1
        LCD_OAM_READ = 2
        LCD_TRANSFER = 3

    def __init__(self):
        super().__init__(bytearray(128), 0xFF00)

        self._boot_rom_locked: bool = False

    def get_boot_ram_locked(self) -> bool:
        return self._boot_rom_locked

    def get_sprite_height(self) -> int:
        return 16 if self._get_lcd_control() & 0x04 else 8

    def get_lcd_window_enable(self) -> bool:
        return self._get_lcd_control() & 0x20 > 0

    def get_lcd_sprite_enable(self) -> bool:
        return self._get_lcd_control() & 0x02 > 0

    def get_lcd_background_enable(self) -> bool:
        return self._get_lcd_control() & 0x01 > 0

    def get_lcd_high_map_window(self) -> bool:
        return self._get_lcd_control() & 0x40 > 0

    def get_lcd_high_map_background(self) -> bool:
        return self._get_lcd_control() & 0x08 > 0

    def get_lcd_low_tiles(self) -> bool:
        return self._get_lcd_control() & 0x10 > 0

    def get_lcd_on(self) -> bool:
        return self._get_lcd_control() & 0x80 > 0

    def get_lcd_window_x(self) -> int:
        return self.read_byte(0xFF4B)

    def get_lcd_window_y(self) -> int:
        return self.read_byte(0xFF4A)

    def is_lcd_y_coincidence_bit_set(self) -> int:
        return self.get_lcd_stat() & 0x04 > 0

    def get_lcd_stat(self) -> int:
        return self.read_byte(0xFF41)

    def set_lcd_stat_bits(self, bits: int):
        self._data[0x41] |= bits

    def clear_lcd_stat_bits(self, bits: int):
        self._data[0x41] &= ~bits

    def set_lcd_mode(self, mode: LCDMode):
        self._data[0x41] = (self._data[0x41] & ~0x03) | mode.value

    def get_lcd_scroll_x(self) -> int:
        return self.read_byte(0xFF43)

    def get_lcd_scroll_y(self) -> int:
        return self.read_byte(0xFF42)

    def get_lcd_background_palette(self) -> int:
        return self.read_byte(0xFF47)

    def get_lcd_y_compare(self) -> int:
        return self.read_byte(0xFF45)

    def get_lcd_object_palette0(self) -> int:
        return self.read_byte(0xFF48)

    def get_lcd_object_palette1(self) -> int:
        return self.read_byte(0xFF49)

    def _get_lcd_control(self) -> int:
        return self.read_byte(0xFF40)

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

from gameboy.memory.memory_region import MemoryRegion


class InterruptFlagRegister(MemoryRegion):
    INTERRUPT_VBLANK = 0x01
    INTERRUPT_LCDC = 0x02
    INTERRUPT_TIMA = 0x04
    INTERRUPT_SERIAL = 0x08
    INTERRUPT_JOYPAD = 0x10

    INTERRUPT_MASK = 0x1F

    def __init__(self):
        super().__init__(bytearray(1), 0xFF0F)
        self._data[0] = 0xE0

    def set_vblank_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_VBLANK

    def set_lcdc_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_LCDC

    def set_tima_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_TIMA

    def set_serial_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_SERIAL

    def set_joypad_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_JOYPAD

    def clear_vblank_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_VBLANK

    def clear_lcdc_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_LCDC

    def clear_tima_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_TIMA

    def clear_serial_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_SERIAL

    def clear_joypad_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_JOYPAD

    def clear_interrupt_by_bit(self, bit_to_clear: int) -> None:
        if bit_to_clear == self.INTERRUPT_VBLANK:
            return self.clear_vblank_interrupt()

        if bit_to_clear == self.INTERRUPT_LCDC:
            return self.clear_lcdc_interrupt()

        if bit_to_clear == self.INTERRUPT_TIMA:
            return self.clear_tima_interrupt()

        if bit_to_clear == self.INTERRUPT_SERIAL:
            return self.clear_serial_interrupt()

        if bit_to_clear == self.INTERRUPT_JOYPAD:
            return self.clear_joypad_interrupt()

        raise Exception('invalid bit to clear: {}'.format(bit_to_clear))

    def write_byte(self, address: int, value: int):
        # Top 4 bits of interrupt flags always read "1"s
        return super().write_byte(address, value | 0xE0)

    def get_interrupt_bits(self):
        return self.read_byte(0xFF0F) & self.INTERRUPT_MASK

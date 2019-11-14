from gameboy.memory.memory_region import MemoryRegion


class InterruptEnableRegister(MemoryRegion):
    INTERRUPT_VBLANK = 0x01
    INTERRUPT_LCDC = 0x02
    INTERRUPT_TIMA = 0x04
    INTERRUPT_SERIAL = 0x08
    INTERRUPT_JOYPAD = 0x10

    def __init__(self):
        super().__init__(bytearray(1), 0xFFFF)

    def enable_vblank_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_VBLANK

    def enable_lcdc_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_LCDC

    def enable_tima_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_TIMA

    def enable_serial_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_SERIAL

    def enable_joypad_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_JOYPAD

    def disable_vblank_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_VBLANK

    def disable_lcdc_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_LCDC

    def disable_tima_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_TIMA

    def disable_serial_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_SERIAL

    def disable_joypad_interrupt(self):
        self._data[0] = self._data[0] & ~self.INTERRUPT_JOYPAD

    def get_interrupt_enabled_bits(self):
        return self.read_byte(0xFFFF)

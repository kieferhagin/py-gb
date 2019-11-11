from gameboy.memory_region import MemoryRegion


class InterruptFlagRegister(MemoryRegion):
    INTERRUPT_TIMA = 0x04

    def __init__(self):
        super().__init__(bytearray(1), 0xFF0F)

    def set_tima_interrupt(self):
        self._data[0] = self._data[0] | self.INTERRUPT_TIMA

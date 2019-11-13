from gameboy.interrupt_enable_register import InterruptEnableRegister
from gameboy.interrupt_flag_register import InterruptFlagRegister


class MemoryUnit:
    def __init__(self):
        self._interrupt_flag_register = InterruptFlagRegister()
        self._interrupt_enable_register = InterruptEnableRegister()

    def read_byte(self, address: int) -> int:
        # Interrupt flags
        if address == 0xFF0F:
            return self._interrupt_flag_register.read_byte(address)

        # Interrupt enable/disable
        if address == 0xFFFF:
            return self._interrupt_enable_register.read_byte(address)

        return 0

    def write_byte(self, address: int, value: int) -> None:
        # Interrupt flags
        if address == 0xFF0F:
            return self._interrupt_flag_register.write_byte(address, value)

        # Interrupt enable/disable
        if address == 0xFFFF:
            return self._interrupt_enable_register.write_byte(address, value)

        return 0

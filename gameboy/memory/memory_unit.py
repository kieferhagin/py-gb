from gameboy.memory.high_ram import HighRAM
from gameboy.memory.interrupt_enable_register import InterruptEnableRegister
from gameboy.memory.interrupt_flag_register import InterruptFlagRegister
from gameboy.memory.video_ram import VideoRAM
from gameboy.memory.work_ram import WorkRAM


class MemoryUnit:
    def __init__(self):
        self._interrupt_flag_register = InterruptFlagRegister()
        self._interrupt_enable_register = InterruptEnableRegister()
        self._video_ram = VideoRAM()
        self._work_ram = WorkRAM()
        self._high_ram = HighRAM()

    def get_interrupt_flag_register(self) -> InterruptFlagRegister:
        return self._interrupt_flag_register

    def get_interrupt_enable_register(self) -> InterruptEnableRegister:
        return self._interrupt_enable_register

    def read_byte(self, address: int) -> int:
        if 0x8000 <= address < 0xA000:  # Video RAM
            return self._video_ram.read_byte(address)

        if 0xC000 <= address < 0xE000:  # Work RAM
            return self._work_ram.read_byte(address)

        if 0xE000 <= address < 0xFE00:  # Work RAM Mirror
            return self._work_ram.read_byte(address - 0x2000)

        if address == 0xFF0F:  # Interrupt flags
            return self._interrupt_flag_register.read_byte(address)

        if 0xFF80 <= address < 0xFFFF:  # High RAM
            return self._high_ram.read_byte(address)

        if address == 0xFFFF:  # Interrupt enable/disable
            return self._interrupt_enable_register.read_byte(address)

        raise NotImplementedError('Address: {}'.format(address))

    def write_byte(self, address: int, value: int) -> None:
        if 0x8000 <= address < 0xA000:  # Video RAM
            return self._video_ram.write_byte(address, value)

        if 0xC000 <= address < 0xE000:  # Work RAM
            return self._work_ram.write_byte(address, value)

        if 0xE000 <= address < 0xFE00:  # Work RAM Mirror
            return self._work_ram.write_byte(address - 0x2000, value)

        if address == 0xFF0F:  # Interrupt flags
            return self._interrupt_flag_register.write_byte(address, value)

        if 0xFF80 <= address < 0xFFFF:  # High RAM
            return self._high_ram.write_byte(address, value)

        if address == 0xFFFF:  # Interrupt enable/disable
            return self._interrupt_enable_register.write_byte(address, value)

        raise NotImplementedError('Address: {}'.format(address))

    def write_word(self, address: int, value: int):
        self.write_byte(address, value & 255)
        self.write_byte(address + 1, (value >> 8))

    def read_word(self, address: int):
        return self.read_byte(address) + ((self.read_byte(address + 1)) << 8)

from gameboy.boot_rom import BootROM
from gameboy.memory.high_ram import HighRAM
from gameboy.memory.interrupt_enable_register import InterruptEnableRegister
from gameboy.memory.interrupt_flag_register import InterruptFlagRegister
from gameboy.memory.video_ram import VideoRAM
from gameboy.memory.work_ram import WorkRAM
from gameboy.rom import ROM


class MemoryUnit:
    def __init__(self):
        self._interrupt_flag_register = InterruptFlagRegister()
        self._interrupt_enable_register = InterruptEnableRegister()
        self._video_ram = VideoRAM()
        self._work_ram = WorkRAM()
        self._high_ram = HighRAM()
        self._boot_rom = BootROM()

        self._cartridge_rom = None

        self._boot_rom_locked = False
        self._cartridge_ram_bank_enabled = False

    def set_cartridge_rom(self, rom: ROM):
        self._cartridge_rom = rom

    def get_interrupt_flag_register(self) -> InterruptFlagRegister:
        return self._interrupt_flag_register

    def get_interrupt_enable_register(self) -> InterruptEnableRegister:
        return self._interrupt_enable_register

    def read_byte(self, address: int) -> int:
        if address <= 0x00FF and not self._boot_rom_locked:  # Boot ROM
            return self._boot_rom.read_byte(address)

        if address < 0x4000:  # ROM bank 0 (fixed)
            if not self._cartridge_rom:
                raise ValueError('No ROM loaded')

            return self._cartridge_rom.read_byte(address)

        if 0x8000 <= address < 0xA000:  # Video RAM
            return self._video_ram.read_byte(address)

        if 0xC000 <= address < 0xE000:  # Work RAM
            return self._work_ram.read_byte(address)

        if 0xE000 <= address < 0xFE00:  # Work RAM Mirror
            return self._work_ram.read_byte(address - 0x2000)

        if address == 0xFF0F:  # Interrupt flags
            return self._interrupt_flag_register.read_byte(address)

        if address == 0xFF50:  # Boot ROM Lock
            return 0xFF if self._boot_rom_locked else 0xFE

        if 0xFF80 <= address < 0xFFFF:  # High RAM
            return self._high_ram.read_byte(address)

        if address == 0xFFFF:  # Interrupt enable/disable
            return self._interrupt_enable_register.read_byte(address)

        raise NotImplementedError('Address: {}'.format(address))

    def write_byte(self, address: int, value: int) -> None:
        if address < 0x2000:  # Cartridge RAM enable
            self._cartridge_ram_bank_enabled = (value & 0xF) == 0xA
            return

        if address < 0x4000:  # ROM bank select
            self._set_rom_bank(address, value)
            return

        if 0x8000 <= address < 0xA000:  # Video RAM
            return self._video_ram.write_byte(address, value)

        if 0xC000 <= address < 0xE000:  # Work RAM
            return self._work_ram.write_byte(address, value)

        if 0xE000 <= address < 0xFE00:  # Work RAM Mirror
            return self._work_ram.write_byte(address - 0x2000, value)

        if address == 0xFF0F:  # Interrupt flags
            return self._interrupt_flag_register.write_byte(address, value)

        if address == 0xFF50:  # Boot ROM lock
            self._boot_rom_locked = True
            return

        if 0xFF80 <= address < 0xFFFF:  # High RAM
            return self._high_ram.write_byte(address, value)

        if address == 0xFFFF:  # Interrupt enable/disable
            return self._interrupt_enable_register.write_byte(address, value)

        raise NotImplementedError('Address: {}'.format(hex(address)))

    def _set_rom_bank(self, address: int, value: int):
        pass

    def write_word(self, address: int, value: int):
        self.write_byte(address, value & 255)
        self.write_byte(address + 1, (value >> 8))

    def read_word(self, address: int):
        return self.read_byte(address) + ((self.read_byte(address + 1)) << 8)

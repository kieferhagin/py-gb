from gameboy.boot_rom import BootROM
from gameboy.memory.cartridge_ram import CartridgeRAM
from gameboy.memory.high_ram import HighRAM
from gameboy.memory.interrupt_enable_register import InterruptEnableRegister
from gameboy.memory.interrupt_flag_register import InterruptFlagRegister
from gameboy.memory.io_ram import IORAM
from gameboy.memory.oam_ram import OAMRam
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
        self._oam = OAMRam()
        self._io_ram = IORAM()

        self._cartridge_rom: ROM = None
        self._cartridge_ram: CartridgeRAM = None

        self._cartridge_ram_bank_enabled = False

        self._mbc_rom_bank = 1
        self._mbc_ram_bank = 0
        self._mbc1_4_32_mode = False

        self._dma_delay_start = False
        self._dma_pending_source = 0
        self._dma_source = 0
        self._dma_active = False

    def set_cartridge_rom(self, rom: ROM):
        self._cartridge_rom = rom
        self._cartridge_ram = CartridgeRAM(self._cartridge_rom.get_ram_size())

    def get_interrupt_flag_register(self) -> InterruptFlagRegister:
        return self._interrupt_flag_register

    def get_interrupt_enable_register(self) -> InterruptEnableRegister:
        return self._interrupt_enable_register

    def read_byte(self, address: int) -> int:
        if self._dma_active and address < 0xFF00:
            return 0xFF

        return self._read_byte_direct(address)

    def _read_byte_direct(self, address: int):
        if address <= 0x00FF and not self._io_ram.get_boot_ram_locked():  # Boot ROM
            return self._boot_rom.read_byte(address)

        if 0x0000 <= address < 0x4000:  # ROM bank 0 (fixed)
            if not self._cartridge_rom:
                raise ValueError('No ROM loaded')

            return self._cartridge_rom.read_byte(address)

        if 0x4000 <= address < 0x8000:  # Banked ROM
            return self._read_banked_rom(address)

        if 0x8000 <= address < 0xA000:  # Video RAM
            return self._video_ram.read_byte(address)

        if 0xA000 <= address < 0xC000:  # Banked RAM
            return self._read_banked_ram(address)

        if 0xC000 <= address < 0xE000:  # Work RAM
            return self._work_ram.read_byte(address)

        if 0xE000 <= address < 0xFE00:  # Work RAM Mirror
            return self._work_ram.read_byte(address - 0x2000)

        if 0xFE00 <= address < 0xFE9F:  # OAM
            return self._oam.read_byte(address)

        if 0xFEA0 <= address < 0xFF00:  # Empty
            return 0x00

        if address == 0xFF0F:  # Interrupt flags
            return self._interrupt_flag_register.read_byte(address)

        if 0xFF00 <= address < 0xFF80:  # IO
            return self._io_ram.read_byte(address)

        if 0xFF80 <= address < 0xFFFF:  # High RAM
            return self._high_ram.read_byte(address)

        if address == 0xFFFF:  # Interrupt enable/disable
            return self._interrupt_enable_register.read_byte(address)

        raise NotImplementedError('Address: {}'.format(address))

    def write_byte(self, address: int, value: int) -> None:
        if self._dma_active and address < 0xFF00:
            return

        return self._write_byte_direct(address, value)

    def _write_byte_direct(self, address: int, value: int):
        if 0x0000 <= address < 0x2000:  # Cartridge RAM enable
            self._cartridge_ram_bank_enabled = (value & 0xF) == 0xA
            return

        if 0x2000 <= address < 0x4000:  # ROM bank select
            self._set_rom_bank(address, value)
            return

        if 0x4000 <= address < 0x6000:  # RAM bank select or high bits of ROM bank if MBC 1
            self._set_ram_bank(address, value)
            return

        if 0x6000 <= address < 0x8000:  # MBC1 mode select or MBC real-time-clock latching
            if self._cartridge_rom.get_memory_bank_model() == ROM.MemoryBankModel.MBC_1:
                self._set_mbc1_mode(value)

                return

            if self._cartridge_rom.get_memory_bank_model() == ROM.MemoryBankModel.MBC_3:
                pass  # TODO: RTC latch

                return

        if 0x8000 <= address < 0xA000:  # Video RAM
            # TODO: Writes to VRAM should be ignored when the LCD is being redrawn
            return self._video_ram.write_byte(address, value)

        if 0xA000 <= address < 0xC000:  # Banked RAM area
            return self._write_banked_ram(address, value)

        if 0xC000 <= address < 0xE000:  # Work RAM
            return self._work_ram.write_byte(address, value)

        if 0xE000 <= address < 0xFE00:  # Work RAM Mirror
            return self._work_ram.write_byte(address - 0x2000, value)

        if 0xFE00 <= address < 0xFE9F:  # OAM
            return self._oam.write_byte(address, value)

        if 0xFEA0 <= address < 0xFF00:  # Empty
            return

        if address == 0xFF0F:  # Interrupt flags
            return self._interrupt_flag_register.write_byte(address, value)

        if address == 0xFF46:  # OAM DMA
            return self._schedule_dma_transfer(value)

        if 0xFF00 <= address < 0xFF80:  # IO
            return self._io_ram.write_byte(address, value)

        if 0xFF80 <= address < 0xFFFF:  # High RAM
            return self._high_ram.write_byte(address, value)

        if address == 0xFFFF:  # Interrupt enable/disable
            return self._interrupt_enable_register.write_byte(address, value)

        raise NotImplementedError('Address: {}'.format(hex(address)))

    def _set_rom_bank(self, address: int, value: int):
        mbc_model = self._cartridge_rom.get_memory_bank_model()

        if mbc_model == ROM.MemoryBankModel.MBC_1:
            # Bottom 5 bits of ROM bank number
            bank_number = value & 0x1F

            # Setting to 0 actually sets it to 1
            if bank_number == 0:
                bank_number = 1

            self._mbc_rom_bank = (self._mbc_rom_bank & 0xE0) | bank_number

            return

        if mbc_model == ROM.MemoryBankModel.MBC_2:
            self._mbc_rom_bank = (value & 0xF) or 1

            return

        if mbc_model == ROM.MemoryBankModel.MBC_3:
            self._mbc_rom_bank = (value & 0x7F) or 1

            return

        if mbc_model == ROM.MemoryBankModel.MBC_5:
            if address < 0x3000:
                self._mbc_rom_bank = (self._mbc_rom_bank & ~0xFF) | value
            else:
                self._mbc_rom_bank = (self._mbc_rom_bank & 0xFF) | ((value & 1) << 8)

    def _set_ram_bank(self, address: int, value: int):
        mbc_model = self._cartridge_rom.get_memory_bank_model()

        if mbc_model == ROM.MemoryBankModel.MBC_1:
            if self._mbc1_4_32_mode:
                self._mbc_ram_bank = value & 0x3
            else:
                self._mbc_rom_bank = (self._mbc_rom_bank & 0x1F) | ((value & 0x3) << 5)

        if mbc_model == ROM.MemoryBankModel.MBC_3:
            self._mbc_ram_bank = value

        if mbc_model == ROM.MemoryBankModel.MBC_5:
            self._mbc_ram_bank = value & 0x0F

    def _set_mbc1_mode(self, value: int):
        if value & 1:  # RAM Banking mode - 32Kbyte RAM in 4 banks, 4MBit ROM
            self._mbc1_4_32_mode = True
            self._mbc_ram_bank = (self._mbc_rom_bank >> 5) & 0x03
            self._mbc_rom_bank &= ~0x1F

        else:  # ROM Banking mode - 8Kbytes unbanked RAM, 16MBit ROM
            self._mbc1_4_32_mode = False
            self._mbc_rom_bank = (self._mbc_rom_bank & 0x1F) | ((self._mbc_ram_bank & 0x03) << 5)
            self._mbc_ram_bank = 0

    def _write_banked_ram(self, address: int, value: int):
        if self._cartridge_ram_bank_enabled:
            cartridge_address = (self._mbc_ram_bank * 0x2000) + address

            if cartridge_address < self._cartridge_rom.get_ram_size():
                # MBC2 has 4 bit memory
                if self._cartridge_rom.get_memory_bank_model() == ROM.MemoryBankModel.MBC_2:
                    value &= 0x0F

                self._cartridge_ram.write_byte(cartridge_address, value)

    def _read_banked_rom(self, address: int) -> int:
        cartridge_address = (self._mbc_rom_bank * 0x4000) + address

        return self._cartridge_rom.read_byte((cartridge_address - 0x4000) % self._cartridge_rom.get_rom_size())

    def _read_banked_ram(self, address: int) -> int:
        cartridge_address = (self._mbc_ram_bank * 0x2000) + address

        if self._cartridge_rom.get_ram_size() > 0 and self._cartridge_ram_bank_enabled:
            return self._cartridge_ram.read_byte(cartridge_address)

        return 0xFF

    def write_word(self, address: int, value: int):
        self.write_byte(address, value & 255)
        self.write_byte(address + 1, (value >> 8))

    def read_word(self, address: int):
        return self.read_byte(address) + ((self.read_byte(address + 1)) << 8)

    def _schedule_dma_transfer(self, value: int):
        if value > 0xF1:
            raise ValueError('Invalid LCD OAM transfer range')

        self._dma_pending_source = value
        self._dma_delay_start = True

    def dma_update(self):
        if self._dma_pending_source:
            if not self._dma_delay_start:
                self._dma_source = self._dma_pending_source << 8
                self._dma_pending_source = 0

            self._dma_delay_start = False

        if self._dma_source and (self._dma_source & 0xFF) < 160:
            self._dma_active = True
            self._oam.write_byte((self._dma_source & 0xFF) + 0xFE00, self._read_byte_direct(self._dma_source))

            self._dma_source += 1
        else:
            self._dma_active = False
            self._dma_source = 0


from enum import Enum

from gameboy.memory.memory_region import MemoryRegion


class ROM(MemoryRegion):

    class MemoryBankModel(Enum):
        MBC_NONE = 0
        MBC_1 = 1
        MBC_2 = 2
        MBC_3 = 3
        MBC_5 = 5

    def __init__(self, data: bytearray):
        super().__init__(data, 0x00)

    def get_title(self) -> str:
        return self.read_byte_range(0x0134, 14).decode('ascii')

    def validate_header_checksum(self) -> bool:
        header_checksum = 0

        for checksum_byte in self.read_byte_range(0x0134, 0x19):
            header_checksum = header_checksum - checksum_byte - 1

        header_checksum &= 0xFF

        return header_checksum == self.read_byte(0x014D)

    def validate_rom_checksum(self) -> bool:
        rom_checksum = 0

        for checksum_byte in self.read_byte_range(0, self.get_rom_size()):
            rom_checksum += checksum_byte

        rom_checksum &= 0xFFFF

        rom_checksum -= self.read_byte(0x014E)
        rom_checksum -= self.read_byte(0x014F)

        expected_checksum = self.read_byte(0x14E) << 8 | self.read_byte(0x14F)

        return expected_checksum == rom_checksum

    def get_memory_bank_model(self) -> MemoryBankModel:
        cartridge_type_byte = self._get_cartridge_type_byte()

        if cartridge_type_byte in [0x00, 0x08, 0x09]:
            return self.MemoryBankModel.MBC_NONE

        if cartridge_type_byte in [0x01, 0x02, 0x03]:
            return self.MemoryBankModel.MBC_1

        if cartridge_type_byte in [0x05, 0x06]:
            return self.MemoryBankModel.MBC_2

        if cartridge_type_byte in range(0x0F, 0x14):
            return self.MemoryBankModel.MBC_3

        if cartridge_type_byte in range(0x19, 0x1F):
            return self.MemoryBankModel.MBC_5

        raise NotImplementedError(f'Cartridge type {cartridge_type_byte} not supported')

    def get_has_battery(self) -> bool:
        return self._get_cartridge_type_byte() in [0x03, 0x06, 0x09, 0x0F, 0x10, 0x13, 0x1B, 0x1E]

    def get_has_rumble(self) -> bool:
        return self._get_cartridge_type_byte() in [0x1C, 0x1D, 0x1E]

    def get_has_real_time_clock(self) -> bool:
        return self._get_cartridge_type_byte() in [0x0F, 0x10]

    def _get_cartridge_type_byte(self) -> int:
        return self.read_byte(0x0147)

    def get_rom_size(self) -> int:
        rom_size_byte = self.read_byte(0x0148)

        if rom_size_byte == 0x00:  # 32KB
            return 32768
        if rom_size_byte == 0x01:  # 64KB
            return 65536
        if rom_size_byte == 0x02:  # 128KB
            return 131072
        if rom_size_byte == 0x03:  # 256KB
            return 262144
        if rom_size_byte == 0x04:  # 512KB
            return 524288
        if rom_size_byte == 0x05:  # 1MB
            return 1048576
        if rom_size_byte == 0x06:  # 2MB
            return 2097152
        if rom_size_byte == 0x52:  # 9 Mbit
            return 1179648
        if rom_size_byte == 0x53:  # 10 Mbit
            return 1310720
        if rom_size_byte == 0x54:  # 12 Mbit
            return 1572864

        raise NotImplementedError(f'Invalid ROM size byte: {rom_size_byte}')

    def get_ram_size(self) -> int:
        ram_size_byte = self.read_byte(0x0149)

        if ram_size_byte == 0x00:  # No RAM, unless MBC2 which always has 512
            if self.get_memory_bank_model() == self.MemoryBankModel.MBC_2:
                return 512

            return 0

        if ram_size_byte == 0x01:
            return 2048
        if ram_size_byte == 0x02:
            return 8192
        if ram_size_byte == 0x03:
            return 32768
        if ram_size_byte == 0x04:
            return 131072

        raise NotImplementedError(f'Invalid RAM size byte: {ram_size_byte}')

from unittest import mock

from gameboy.rom import ROM


def test_rom_get_title(test_rom_fixture):
    assert test_rom_fixture.get_title()[:12] == "INSTR_TIMING"


def test_rom_validate_checksum(test_rom_fixture):
    assert test_rom_fixture.validate_header_checksum()
    test_rom_fixture.write_byte(0x014D, 0)

    assert not test_rom_fixture.validate_header_checksum()


def test_get_cartridge_type(test_rom_fixture):
    assert test_rom_fixture.get_memory_bank_model() == ROM.MemoryBankModel.MBC_1

    test_rom_fixture.write_byte(0x0147, 0x09)

    assert test_rom_fixture.get_memory_bank_model() == ROM.MemoryBankModel.MBC_NONE

    test_rom_fixture.write_byte(0x0147, 0x06)

    assert test_rom_fixture.get_memory_bank_model() == ROM.MemoryBankModel.MBC_2

    test_rom_fixture.write_byte(0x0147, 0x13)

    assert test_rom_fixture.get_memory_bank_model() == ROM.MemoryBankModel.MBC_3

    test_rom_fixture.write_byte(0x0147, 0x1A)

    assert test_rom_fixture.get_memory_bank_model() == ROM.MemoryBankModel.MBC_5


def test_get_has_battery(test_rom_fixture):
    for cartridge_type in [0x03, 0x06, 0x09, 0x0F, 0x10, 0x13, 0x1B, 0x1E]:
        test_rom_fixture.write_byte(0x0147, cartridge_type)
        assert test_rom_fixture.get_has_battery()

    test_rom_fixture.write_byte(0x0147, 0x01)

    assert not test_rom_fixture.get_has_battery()


def test_get_has_rumble(test_rom_fixture):
    for cartridge_type in [0x1C, 0x1D, 0x1E]:
        test_rom_fixture.write_byte(0x0147, cartridge_type)
        assert test_rom_fixture.get_has_rumble()

    test_rom_fixture.write_byte(0x0147, 0x01)

    assert not test_rom_fixture.get_has_rumble()


def test_get_has_real_time_clock(test_rom_fixture):
    for cartridge_type in [0x0F, 0x10]:
        test_rom_fixture.write_byte(0x0147, cartridge_type)
        assert test_rom_fixture.get_has_real_time_clock()

    test_rom_fixture.write_byte(0x0147, 0x01)

    assert not test_rom_fixture.get_has_real_time_clock()


def test_get_rom_size(test_rom_fixture):
    test_rom_fixture.write_byte(0x0148, 0x00)
    assert test_rom_fixture.get_rom_size() == 32768

    test_rom_fixture.write_byte(0x0148, 0x52)
    assert test_rom_fixture.get_rom_size() == 1179648


def test_get_ram_size(test_rom_fixture):
    test_rom_fixture.write_byte(0x0149, 0x00)
    assert test_rom_fixture.get_ram_size() == 0

    test_rom_fixture.write_byte(0x0149, 0x00)
    test_rom_fixture.get_memory_bank_model = mock.Mock()
    test_rom_fixture.get_memory_bank_model.return_value = ROM.MemoryBankModel.MBC_2

    assert test_rom_fixture.get_ram_size() == 512

    test_rom_fixture.write_byte(0x0149, 0x04)

    assert test_rom_fixture.get_ram_size() == 131072


def test_validate_rom_checksum(test_rom_fixture):
    assert test_rom_fixture.validate_rom_checksum()

    test_rom_fixture.write_byte(0x00, 255)
    assert not test_rom_fixture.validate_rom_checksum()

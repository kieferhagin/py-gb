from unittest import mock

import pytest

from gameboy.memory.memory_unit import MemoryUnit
from gameboy.rom import ROM


@pytest.fixture()
def memory_unit_fixture(test_rom_fixture) -> MemoryUnit:
    m = MemoryUnit()
    m.set_cartridge_rom(test_rom_fixture)
    
    return m


def test_memory_unit_init():
    m = MemoryUnit()
    assert m._interrupt_flag_register is not None
    assert m._interrupt_enable_register is not None
    assert m._video_ram is not None
    assert m._work_ram is not None
    assert m._high_ram is not None
    assert m._boot_rom is not None
    assert m._cartridge_rom is None

    assert m._mbc_rom_bank == 1
    assert m._mbc_ram_bank == 0
    assert not m._mbc1_4_32_mode


def test_memory_unit_set_cartridge_rom(memory_unit_fixture):
    test_rom = ROM(bytearray([1, 2, 3, 4]))

    memory_unit_fixture.set_cartridge_rom(test_rom)
    assert memory_unit_fixture._cartridge_rom == test_rom


def test_memory_unit_read_byte_interrupt_flags(memory_unit_fixture):
    memory_unit_fixture._interrupt_flag_register.set_vblank_interrupt()
    assert memory_unit_fixture.read_byte(0xFF0F) == 0xE1


def test_memory_unit_read_byte_interrupt_enable(memory_unit_fixture):
    memory_unit_fixture._interrupt_enable_register.enable_vblank_interrupt()
    assert memory_unit_fixture.read_byte(0xFFFF) == 0x01


def test_memory_unit_write_byte_interrupt_flags(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xFF0F, 0x01)
    assert memory_unit_fixture.read_byte(0xFF0F) == 0xE1


def test_memory_unit_write_byte_interrupt_enable(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xFFFF, 0x01)
    assert memory_unit_fixture.read_byte(0xFFFF) == 0x01


def test_memory_unit_get_interrupt_flag_register(memory_unit_fixture):
    assert memory_unit_fixture.get_interrupt_flag_register() == memory_unit_fixture._interrupt_flag_register


def test_memory_unit_get_interrupt_enable_register(memory_unit_fixture):
    assert memory_unit_fixture.get_interrupt_enable_register() == memory_unit_fixture._interrupt_enable_register


def test_memory_unit_read_video_ram(memory_unit_fixture):
    memory_unit_fixture._video_ram.write_byte(0x8000, 15)
    assert memory_unit_fixture.read_byte(0x8000) == 15


def test_memory_unit_read_work_ram(memory_unit_fixture):
    memory_unit_fixture._work_ram.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xC000) == 15


def test_memory_unit_read_work_ram_mirror(memory_unit_fixture):
    memory_unit_fixture._work_ram.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xE000) == 15


def test_memory_unit_read_high_ram(memory_unit_fixture):
    memory_unit_fixture._high_ram.write_byte(0xFF80, 15)
    assert memory_unit_fixture.read_byte(0xFF80) == 15


def test_memory_unit_write_video_ram(memory_unit_fixture):
    memory_unit_fixture.write_byte(0x8000, 15)
    assert memory_unit_fixture.read_byte(0x8000) == 15


def test_memory_unit_write_work_ram(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xC000) == 15


def test_memory_unit_write_work_ram_mirror(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xE000) == 15


def test_memory_unit_write_high_ram(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xFF80, 15)
    assert memory_unit_fixture.read_byte(0xFF80) == 15


def test_read_word(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xC000, 244)
    memory_unit_fixture.write_byte(0xC001, 1)

    assert memory_unit_fixture.read_word(0xC000) == 500


def test_write_word(memory_unit_fixture):
    memory_unit_fixture.write_word(0xC000, 500)

    assert memory_unit_fixture.read_byte(0xC000) == 244
    assert memory_unit_fixture.read_byte(0xC001) == 1


def test_lock_boot_rom(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xFF50, 1)

    assert memory_unit_fixture._boot_rom_locked


def test_read_locked_boot_rom(memory_unit_fixture):
    assert memory_unit_fixture.read_byte(0xFF50) == 0b11111110

    memory_unit_fixture._boot_rom_locked = True
    assert memory_unit_fixture.read_byte(0xFF50) == 0b11111111


def test_read_boot_rom(memory_unit_fixture):
    memory_unit_fixture._boot_rom.read_byte = mock.Mock()
    memory_unit_fixture._boot_rom_locked = False

    memory_unit_fixture.read_byte(0x00)
    memory_unit_fixture._boot_rom.read_byte.assert_called_once_with(0x00)


def test_read_catridge_rom_bank_0(memory_unit_fixture):
    memory_unit_fixture._cartridge_rom = ROM(bytearray([117, 2, 3, 4]))
    memory_unit_fixture._boot_rom_locked = True

    assert memory_unit_fixture.read_byte(0x00) == 117

    memory_unit_fixture._cartridge_rom = None

    with pytest.raises(ValueError):
        memory_unit_fixture.read_byte(0x00)


def test_enable_rom_ram(memory_unit_fixture):
    memory_unit_fixture._cartridge_ram_bank_enabled = False
    memory_unit_fixture.write_byte(0x00, 0x0A)

    assert memory_unit_fixture._cartridge_ram_bank_enabled

    memory_unit_fixture._cartridge_ram_bank_enabled = False
    memory_unit_fixture.write_byte(0x00, 0x00)

    assert not memory_unit_fixture._cartridge_ram_bank_enabled


def test_set_rom_bank_mbc_1(memory_unit_fixture):
    memory_unit_fixture.write_byte(0x3000, 0)

    assert memory_unit_fixture._mbc_rom_bank == 1

    memory_unit_fixture.write_byte(0x3000, 0b11111111)

    assert memory_unit_fixture._mbc_rom_bank == 0b00011111


def test_set_ram_bank_mbc_1_rom(memory_unit_fixture):
    memory_unit_fixture.write_byte(0x4000, 0b00000011)

    assert memory_unit_fixture._mbc_rom_bank == 0b01100001

    memory_unit_fixture._mbc1_4_32_mode = True
    memory_unit_fixture.write_byte(0x4000, 0b00000011)

    assert memory_unit_fixture._mbc_ram_bank == 3


def test_set_mbc1_mode(memory_unit_fixture):
    memory_unit_fixture.write_byte(0x6000, 1)
    assert memory_unit_fixture._mbc1_4_32_mode

    memory_unit_fixture.write_byte(0x6000, 0)
    assert not memory_unit_fixture._mbc1_4_32_mode

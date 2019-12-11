import pytest

from gameboy.memory.io_ram import IORAM


@pytest.fixture()
def io_ram_fixture() -> IORAM:
    return IORAM()


def test_io_ram_init(io_ram_fixture):
    assert len(io_ram_fixture._data) == 128
    assert io_ram_fixture._base_address == 0xFF00


def test_lock_boot_rom(io_ram_fixture):
    io_ram_fixture.write_byte(0xFF50, 1)

    assert io_ram_fixture._boot_rom_locked


def test_read_locked_boot_rom(io_ram_fixture):
    assert io_ram_fixture.read_byte(0xFF50) == 0b11111110

    io_ram_fixture._boot_rom_locked = True
    assert io_ram_fixture.read_byte(0xFF50) == 0b11111111


def test_set_lcd_state(io_ram_fixture):
    io_ram_fixture.write_byte(0xFF41, 0b11111111)

    assert io_ram_fixture.read_byte(0xFF41) == 0b11111100


def test_reset_lcd_y(io_ram_fixture):
    io_ram_fixture._data[0x44] = 110
    assert io_ram_fixture.read_byte(0x44) == 110

    io_ram_fixture.write_byte(0xFF44, 0b11111111)
    assert io_ram_fixture.read_byte(0xFF44) == 0


def test_get_sprite_height(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x04

    assert io_ram_fixture.get_sprite_height() == 16

    io_ram_fixture._data[0x40] = 0x00

    assert io_ram_fixture.get_sprite_height() == 8

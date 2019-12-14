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


def test_set_lcd_stat_bits(io_ram_fixture):
    io_ram_fixture.set_lcd_stat_bits(0x04)

    assert io_ram_fixture.read_byte(0xFF41) == 0x04

    io_ram_fixture.clear_lcd_stat_bits(0x04)

    assert io_ram_fixture.read_byte(0xFF41) == 0x00


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


def test_get_window_enable(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x20

    assert io_ram_fixture.get_lcd_window_enable()

    io_ram_fixture._data[0x40] = 0x00

    assert not io_ram_fixture.get_lcd_window_enable()


def test_get_sprite_enable(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x02

    assert io_ram_fixture.get_lcd_sprite_enable()

    io_ram_fixture._data[0x40] = 0x00

    assert not io_ram_fixture.get_lcd_sprite_enable()


def test_get_bg_enable(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x01

    assert io_ram_fixture.get_lcd_background_enable()

    io_ram_fixture._data[0x40] = 0x00

    assert not io_ram_fixture.get_lcd_background_enable()


def test_get_hi_win(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x40

    assert io_ram_fixture.get_lcd_high_map_window()

    io_ram_fixture._data[0x40] = 0x00

    assert not io_ram_fixture.get_lcd_high_map_window()


def test_get_hi_bg(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x08

    assert io_ram_fixture.get_lcd_high_map_background()

    io_ram_fixture._data[0x40] = 0x00

    assert not io_ram_fixture.get_lcd_high_map_background()


def test_get_low_tiles(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x10

    assert io_ram_fixture.get_lcd_low_tiles()

    io_ram_fixture._data[0x40] = 0x00

    assert not io_ram_fixture.get_lcd_low_tiles()


def test_get_lcd_on(io_ram_fixture):
    io_ram_fixture._data[0x40] = 0x80

    assert io_ram_fixture.get_lcd_on()

    io_ram_fixture._data[0x40] = 0x00

    assert not io_ram_fixture.get_lcd_on()


def test_get_lcd_y_compare(io_ram_fixture):
    io_ram_fixture._data[0x45] = 0x01

    assert io_ram_fixture.get_lcd_y_compare() == 0x01


def test_get_lcd_stat(io_ram_fixture):
    io_ram_fixture._data[0x41] = 0x01

    assert io_ram_fixture.get_lcd_stat() == 0x01


def test_get_coincidence_bit_set(io_ram_fixture):
    io_ram_fixture._data[0x41] = 0x04

    assert io_ram_fixture.is_lcd_y_coincidence_bit_set()

    io_ram_fixture._data[0x41] = 0x00

    assert not io_ram_fixture.is_lcd_y_coincidence_bit_set()


def test_get_lcd_win_x(io_ram_fixture):
    io_ram_fixture._data[0x4B] = 0x01

    assert io_ram_fixture.get_lcd_window_x() == 1

    io_ram_fixture._data[0x4B] = 0x02

    assert io_ram_fixture.get_lcd_window_x() == 2


def test_get_lcd_win_y(io_ram_fixture):
    io_ram_fixture._data[0x4A] = 0x01

    assert io_ram_fixture.get_lcd_window_y() == 1

    io_ram_fixture._data[0x4A] = 0x02

    assert io_ram_fixture.get_lcd_window_y() == 2


def test_get_lcd_scroll_x(io_ram_fixture):
    io_ram_fixture._data[0x43] = 0x01

    assert io_ram_fixture.get_lcd_scroll_x() == 1

    io_ram_fixture._data[0x43] = 0x02

    assert io_ram_fixture.get_lcd_scroll_x() == 2


def test_get_lcd_scroll_y(io_ram_fixture):
    io_ram_fixture._data[0x42] = 0x01

    assert io_ram_fixture.get_lcd_scroll_y() == 1

    io_ram_fixture._data[0x42] = 0x02

    assert io_ram_fixture.get_lcd_scroll_y() == 2


def test_get_lcd_background_palette(io_ram_fixture):
    io_ram_fixture._data[0x47] = 0x01

    assert io_ram_fixture.get_lcd_background_palette() == 1

    io_ram_fixture._data[0x47] = 0x02

    assert io_ram_fixture.get_lcd_background_palette() == 2


def test_get_lcd_object_palette0(io_ram_fixture):
    io_ram_fixture._data[0x48] = 0x01

    assert io_ram_fixture.get_lcd_object_palette0() == 1

    io_ram_fixture._data[0x48] = 0x02

    assert io_ram_fixture.get_lcd_object_palette0() == 2


def test_get_lcd_object_palette1(io_ram_fixture):
    io_ram_fixture._data[0x49] = 0x01

    assert io_ram_fixture.get_lcd_object_palette1() == 1

    io_ram_fixture._data[0x49] = 0x02

    assert io_ram_fixture.get_lcd_object_palette1() == 2

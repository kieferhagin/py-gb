from unittest import mock

import pytest

from gameboy.gpu.gpu import GPU
from gameboy.gpu.gpu_sprite import GPUSprite
from gameboy.memory.interrupt_flag_register import InterruptFlagRegister
from gameboy.memory.io_ram import IORAM
from gameboy.memory.memory_unit import MemoryUnit


@pytest.fixture()
def gpu_fixture() -> GPU:
    return GPU(MemoryUnit())


def test_gpu_init(gpu_fixture):
    assert len(gpu_fixture._buffer) == 160
    assert len(gpu_fixture._buffer[0]) == 144
    assert gpu_fixture._frame_progress == 0
    assert gpu_fixture._new_frame_available is False
    assert len(gpu_fixture._sprite_buffer) == 0
    assert gpu_fixture._current_x == 0


def test_get_tile_line_address(gpu_fixture):
    tile_index_byte = 0
    y = 0
    use_lower_bank = False

    assert gpu_fixture._get_tile_line_address(tile_index_byte, y, use_lower_bank) == 0x9000

    tile_index_byte = 1
    y = 0
    use_lower_bank = False

    assert gpu_fixture._get_tile_line_address(tile_index_byte, y, use_lower_bank) == 0x9010

    tile_index_byte = 1
    y = 1
    use_lower_bank = False

    assert gpu_fixture._get_tile_line_address(tile_index_byte, y, use_lower_bank) == 0x9012

    tile_index_byte = 1
    y = 1
    use_lower_bank = True

    assert gpu_fixture._get_tile_line_address(tile_index_byte, y, use_lower_bank) == 0x8012


def test_get_line_pixel(gpu_fixture):
    line_byte_0 = 0b01111100
    line_byte_1 = 0b01111100
    x = 0

    assert gpu_fixture._get_line_pixel(line_byte_0, line_byte_1, x) == 0

    line_byte_0 = 0b11111100
    line_byte_1 = 0b01111100
    x = 0

    assert gpu_fixture._get_line_pixel(line_byte_0, line_byte_1, x) == 1

    line_byte_0 = 0b01111100
    line_byte_1 = 0b11111100
    x = 0

    assert gpu_fixture._get_line_pixel(line_byte_0, line_byte_1, x) == 2

    line_byte_0 = 0b11111100
    line_byte_1 = 0b11111100
    x = 0

    assert gpu_fixture._get_line_pixel(line_byte_0, line_byte_1, x) == 3

    line_byte_0 = 0b01111100
    line_byte_1 = 0b01111100
    x = 1

    assert gpu_fixture._get_line_pixel(line_byte_0, line_byte_1, x) == 3

    line_byte_0 = 0b00111100
    line_byte_1 = 0b01111100
    x = 1

    assert gpu_fixture._get_line_pixel(line_byte_0, line_byte_1, x) == 2

    line_byte_0 = 0b01111100
    line_byte_1 = 0b00111100
    x = 1

    assert gpu_fixture._get_line_pixel(line_byte_0, line_byte_1, x) == 1


def test_get_map_pixel(gpu_fixture):
    high_map = False
    low_tiles = True
    x = 1
    y = 0

    gpu_fixture._memory_unit.write_byte(0x8000, 0b01111100)
    gpu_fixture._memory_unit.write_byte(0x8001, 0b00111100)

    gpu_fixture._memory_unit.write_byte(0x9800, 0)

    assert gpu_fixture._get_map_pixel(high_map, low_tiles, x, y) == 1

    high_map = False
    low_tiles = True
    x = 1
    y = 0

    gpu_fixture._memory_unit.write_byte(0x8000, 0b01111100)
    gpu_fixture._memory_unit.write_byte(0x8001, 0b01111100)

    gpu_fixture._memory_unit.write_byte(0x9800, 0)

    assert gpu_fixture._get_map_pixel(high_map, low_tiles, x, y) == 3


def test_get_scanline_sprites(gpu_fixture):
    scanline_number = 1
    y_pos = 17
    x_pos = 10
    tile = 0
    attributes = 1

    gpu_fixture._memory_unit.write_byte(0x8000, 0b01111100)
    gpu_fixture._memory_unit.write_byte(0x8001, 0b00111100)

    gpu_fixture._memory_unit._oam._data[0] = y_pos
    gpu_fixture._memory_unit._oam._data[1] = x_pos
    gpu_fixture._memory_unit._oam._data[2] = tile
    gpu_fixture._memory_unit._oam._data[3] = attributes

    sprites = gpu_fixture._get_scanline_sprites(scanline_number)

    assert len(sprites) == 1
    assert sprites[0].get_x() == x_pos
    assert sprites[0].get_y() == y_pos
    assert sprites[0].get_attributes_byte() == attributes
    assert sprites[0].get_pixels() == [0b01111100, 0b00111100]


def test_lcdy_compare(gpu_fixture):
    scanline_number = 40
    gpu_fixture._lcdy_compare(scanline_number)

    assert gpu_fixture._memory_unit._io_ram.read_byte(0xFF41) & 0x04 == 0
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[0] & InterruptFlagRegister.INTERRUPT_LCDC == 0

    gpu_fixture._memory_unit._io_ram.write_byte(0xFF45, scanline_number)
    gpu_fixture._lcdy_compare(scanline_number)

    assert gpu_fixture._memory_unit._io_ram.read_byte(0xFF41) & 0x04 == 0x04
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[0] & InterruptFlagRegister.INTERRUPT_LCDC == 0

    gpu_fixture._memory_unit._io_ram.clear_lcd_stat_bits(0x04)
    gpu_fixture._memory_unit._io_ram.set_lcd_stat_bits(0x40)
    gpu_fixture._memory_unit._io_ram.write_byte(0xFF45, scanline_number)
    gpu_fixture._lcdy_compare(scanline_number)

    assert gpu_fixture._memory_unit._io_ram.read_byte(0xFF41) & 0x04 == 0x04
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[0] & InterruptFlagRegister.INTERRUPT_LCDC == InterruptFlagRegister.INTERRUPT_LCDC

    gpu_fixture._lcdy_compare(scanline_number+1)

    assert gpu_fixture._memory_unit._io_ram.read_byte(0xFF41) & 0x04 == 0


def test_vblank(gpu_fixture):
    gpu_fixture._vblank()

    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 1
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[
               0] & InterruptFlagRegister.INTERRUPT_VBLANK == InterruptFlagRegister.INTERRUPT_VBLANK
    assert gpu_fixture._new_frame_available


def test_oam_read(gpu_fixture):
    sprite_buffer = [GPUSprite(0, 0, [0, 0], 0)]

    gpu_fixture._get_scanline_sprites = mock.Mock()
    gpu_fixture._get_scanline_sprites.return_value = sprite_buffer
    gpu_fixture._current_x = 10

    gpu_fixture._oam_read(40)

    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 2
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[0] & InterruptFlagRegister.INTERRUPT_LCDC == 0
    assert gpu_fixture._current_x == 0
    gpu_fixture._get_scanline_sprites.assert_called_once_with(40)
    assert gpu_fixture._sprite_buffer == sprite_buffer

    gpu_fixture._memory_unit._io_ram.set_lcd_stat_bits(0x20)

    gpu_fixture._oam_read(40)

    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 2
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[0] & InterruptFlagRegister.INTERRUPT_LCDC == InterruptFlagRegister.INTERRUPT_LCDC
    assert gpu_fixture._current_x == 0


def test_transfer_data(gpu_fixture):
    gpu_fixture.draw_pixel = mock.Mock()
    scanline_progress = 200
    scanline_number = 50
    gpu_fixture._memory_unit._io_ram._data[0x40] |= 0x80

    gpu_fixture._transfer_data_to_buffer(scanline_progress, scanline_number)

    assert gpu_fixture.draw_pixel.call_count == scanline_progress - 92
    assert gpu_fixture._current_x == scanline_progress - 92
    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 3

    gpu_fixture.draw_pixel = mock.Mock()
    scanline_progress = 200
    scanline_number = 50
    gpu_fixture._memory_unit._io_ram._data[0x40] = 0
    gpu_fixture._memory_unit._io_ram.set_lcd_mode(IORAM.LCDMode.LCD_VBLANK)
    gpu_fixture._current_x = 0

    gpu_fixture._transfer_data_to_buffer(scanline_progress, scanline_number)

    assert gpu_fixture.draw_pixel.call_count == 0
    assert gpu_fixture._current_x == 0
    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 3


def test_hblank(gpu_fixture):
    gpu_fixture.draw_pixel = mock.Mock()
    scanline_number = 50
    gpu_fixture._memory_unit._io_ram._data[0x40] |= 0x80

    gpu_fixture._hblank(scanline_number)

    assert gpu_fixture.draw_pixel.call_count == 160
    assert gpu_fixture._current_x == 160
    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 0

    gpu_fixture.draw_pixel = mock.Mock()
    scanline_number = 50
    gpu_fixture._memory_unit._io_ram._data[0x40] = 0
    gpu_fixture._memory_unit._io_ram.set_lcd_mode(IORAM.LCDMode.LCD_VBLANK)
    gpu_fixture._current_x = 0

    gpu_fixture._hblank(scanline_number)

    assert gpu_fixture.draw_pixel.call_count == 0
    assert gpu_fixture._current_x == 0
    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 0
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[
               0] & InterruptFlagRegister.INTERRUPT_LCDC == 0

    gpu_fixture.draw_pixel = mock.Mock()
    scanline_number = 50
    gpu_fixture._memory_unit._io_ram._data[0x40] = 0
    gpu_fixture._memory_unit._io_ram.set_lcd_mode(IORAM.LCDMode.LCD_VBLANK)
    gpu_fixture._memory_unit._io_ram.set_lcd_stat_bits(0x08)
    gpu_fixture._current_x = 0

    gpu_fixture._hblank(scanline_number)

    assert gpu_fixture.draw_pixel.call_count == 0
    assert gpu_fixture._current_x == 0
    assert gpu_fixture._memory_unit._io_ram.get_lcd_stat() & 0x03 == 0
    assert gpu_fixture._memory_unit._interrupt_flag_register._data[
               0] & InterruptFlagRegister.INTERRUPT_LCDC == InterruptFlagRegister.INTERRUPT_LCDC

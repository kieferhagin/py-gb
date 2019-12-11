import pytest

from gameboy.gpu.gpu import GPU
from gameboy.memory.memory_unit import MemoryUnit


@pytest.fixture()
def gpu_fixture() -> GPU:
    return GPU(MemoryUnit())


def test_gpu_init(gpu_fixture):
    assert len(gpu_fixture._buffer) == 160
    assert len(gpu_fixture._buffer[0]) == 144
    assert gpu_fixture._frame_progress == 0
    assert gpu_fixture._new_frame_available is False


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

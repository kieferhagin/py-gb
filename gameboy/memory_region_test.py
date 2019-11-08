import pytest

from gameboy.memory_region import MemoryRegion


@pytest.fixture()
def memory_region_fixture() -> MemoryRegion:
    return MemoryRegion(bytearray(10), 0xFFFF)


def test_memory_region_init(memory_region_fixture):
    assert len(memory_region_fixture._data) == 10
    assert memory_region_fixture._base_address == 0xFFFF


def test_read_byte(memory_region_fixture):
    memory_region_fixture._data[7] = 124
    assert memory_region_fixture.read_byte(0xFFFF + 8) == 124


def test_write_byte(memory_region_fixture):
    memory_region_fixture.write_byte(0xFFFF + 8, 124)
    assert memory_region_fixture._data[7] == 124


def test_write_byte_overflow_error(memory_region_fixture):
    with pytest.raises(ValueError):
        memory_region_fixture.write_byte(0xFFFF + 8, 256)


def test_read_word(memory_region_fixture):
    memory_region_fixture._data[7] = 244
    memory_region_fixture._data[8] = 1

    assert memory_region_fixture.read_word(0xFFFF + 8) == 500


def test_write_word(memory_region_fixture):
    memory_region_fixture.write_word(0xFFFF + 8, 500)

    assert memory_region_fixture._data[7] == 244
    assert memory_region_fixture._data[8] == 1

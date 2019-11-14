import pytest

from gameboy.memory.high_ram import HighRAM


@pytest.fixture()
def high_ram_fixture() -> HighRAM:
    return HighRAM()


def test_video_ram_init(high_ram_fixture):
    assert len(high_ram_fixture._data) == 127
    assert high_ram_fixture._base_address == 0xFF80

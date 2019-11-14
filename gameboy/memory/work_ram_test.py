import pytest

from gameboy.memory.work_ram import WorkRAM


@pytest.fixture()
def work_ram_fixture() -> WorkRAM:
    return WorkRAM()


def test_video_ram_init(work_ram_fixture):
    assert len(work_ram_fixture._data) == 8192
    assert work_ram_fixture._base_address == 0xC000

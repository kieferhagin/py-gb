import pytest

from gameboy.memory.video_ram import VideoRAM


@pytest.fixture()
def video_ram_fixture() -> VideoRAM:
    return VideoRAM()


def test_video_ram_init(video_ram_fixture):
    assert len(video_ram_fixture._data) == 8192
    assert video_ram_fixture._base_address == 0x8000

import pytest

from gameboy.gameboy import GameBoy
from gameboy.rom import ROM


@pytest.fixture()
def gameboy_fixture() -> GameBoy:
    gameboy = GameBoy()

    return gameboy


def test_gameboy_init(gameboy_fixture):
    assert gameboy_fixture._memory_unit is not None
    assert gameboy_fixture._cpu is not None
    assert gameboy_fixture._cpu._memory_unit == gameboy_fixture._memory_unit


def test_gameboy_get_memory_unit(gameboy_fixture):
    assert gameboy_fixture.get_memory_unit() == gameboy_fixture._memory_unit


def test_gameboy_it_should_load_rom(gameboy_fixture, test_rom_fixture):
    gameboy_fixture.load_rom(test_rom_fixture)

    assert gameboy_fixture._rom == test_rom_fixture
    assert gameboy_fixture._memory_unit._cartridge_rom == test_rom_fixture

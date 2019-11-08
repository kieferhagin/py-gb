import pytest

from gameboy.gameboy import GameBoy
from gameboy.rom import ROM


@pytest.fixture()
def gameboy_fixture() -> GameBoy:
    gameboy = GameBoy()

    return gameboy


def test_gameboy_it_should_load_rom(gameboy_fixture):
    rom = ROM(bytearray())
    gameboy_fixture.load_rom(rom)

    assert gameboy_fixture._rom == rom

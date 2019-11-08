import pytest

from gameboy.rom import ROM


@pytest.fixture()
def test_rom_fixture() -> ROM:
    with open("../test_roms/instr_timing.gb", "rb") as binary_file:
        return ROM(bytearray(binary_file.read()))


def test_rom_get_title(test_rom_fixture):
    assert test_rom_fixture.get_title()[:12] == "INSTR_TIMING"

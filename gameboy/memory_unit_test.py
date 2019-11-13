import pytest

from gameboy.memory_unit import MemoryUnit


@pytest.fixture()
def memory_unit_fixture() -> MemoryUnit:
    return MemoryUnit()


def test_memory_unit_init(memory_unit_fixture):
    assert memory_unit_fixture._interrupt_flag_register is not None
    assert memory_unit_fixture._interrupt_enable_register is not None


def test_memory_unit_read_byte_interrupt_flags(memory_unit_fixture):
    memory_unit_fixture._interrupt_flag_register.set_vblank_interrupt()
    assert memory_unit_fixture.read_byte(0xFF0F) == 0xE1


def test_memory_unit_read_byte_interrupt_enable(memory_unit_fixture):
    memory_unit_fixture._interrupt_enable_register.enable_vblank_interrupt()
    assert memory_unit_fixture.read_byte(0xFFFF) == 0x01


def test_memory_unit_write_byte_interrupt_flags(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xFF0F, 0x01)
    assert memory_unit_fixture.read_byte(0xFF0F) == 0xE1


def test_memory_unit_write_byte_interrupt_enable(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xFFFF, 0x01)
    assert memory_unit_fixture.read_byte(0xFFFF) == 0x01



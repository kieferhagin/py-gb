import pytest

from gameboy.memory.memory_unit import MemoryUnit


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


def test_memory_unit_get_interrupt_flag_register(memory_unit_fixture):
    assert memory_unit_fixture.get_interrupt_flag_register() == memory_unit_fixture._interrupt_flag_register


def test_memory_unit_get_interrupt_enable_register(memory_unit_fixture):
    assert memory_unit_fixture.get_interrupt_enable_register() == memory_unit_fixture._interrupt_enable_register


def test_memory_unit_read_video_ram(memory_unit_fixture):
    memory_unit_fixture._video_ram.write_byte(0x8000, 15)
    assert memory_unit_fixture.read_byte(0x8000) == 15


def test_memory_unit_read_work_ram(memory_unit_fixture):
    memory_unit_fixture._work_ram.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xC000) == 15


def test_memory_unit_read_work_ram_mirror(memory_unit_fixture):
    memory_unit_fixture._work_ram.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xE000) == 15


def test_memory_unit_read_high_ram(memory_unit_fixture):
    memory_unit_fixture._high_ram.write_byte(0xFF80, 15)
    assert memory_unit_fixture.read_byte(0xFF80) == 15


def test_memory_unit_write_video_ram(memory_unit_fixture):
    memory_unit_fixture.write_byte(0x8000, 15)
    assert memory_unit_fixture.read_byte(0x8000) == 15


def test_memory_unit_write_work_ram(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xC000) == 15


def test_memory_unit_write_work_ram_mirror(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xC000, 15)
    assert memory_unit_fixture.read_byte(0xE000) == 15


def test_memory_unit_write_high_ram(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xFF80, 15)
    assert memory_unit_fixture.read_byte(0xFF80) == 15


def test_read_word(memory_unit_fixture):
    memory_unit_fixture.write_byte(0xC000, 244)
    memory_unit_fixture.write_byte(0xC001, 1)

    assert memory_unit_fixture.read_word(0xC000) == 500


def test_write_word(memory_unit_fixture):
    memory_unit_fixture.write_word(0xC000, 500)

    assert memory_unit_fixture.read_byte(0xC000) == 244
    assert memory_unit_fixture.read_byte(0xC001) == 1


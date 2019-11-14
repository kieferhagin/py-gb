import pytest

from gameboy.memory.interrupt_flag_register import InterruptFlagRegister


@pytest.fixture()
def interrupt_flag_register_fixture():
    return InterruptFlagRegister()


def test_interrupt_flag_register_init(interrupt_flag_register_fixture):
    assert len(interrupt_flag_register_fixture._data) == 1
    assert interrupt_flag_register_fixture._data[0] == 0xE0
    assert interrupt_flag_register_fixture._base_address == 0xFF0F


def test_interrupt_flag_register_set_vblank(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_vblank_interrupt()
    assert interrupt_flag_register_fixture.read_byte(0xFF0F) == 0xE1
    
    
def test_interrupt_flag_register_set_lcdc(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_lcdc_interrupt()
    assert interrupt_flag_register_fixture.read_byte(0xFF0F) == 0xE2


def test_interrupt_flag_register_set_tima(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_tima_interrupt()
    assert interrupt_flag_register_fixture.read_byte(0xFF0F) == 0xE4


def test_interrupt_flag_register_set_serial(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_serial_interrupt()
    assert interrupt_flag_register_fixture.read_byte(0xFF0F) == 0xE8


def test_interrupt_flag_register_set_joypad(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_joypad_interrupt()
    assert interrupt_flag_register_fixture.read_byte(0xFF0F) == 0xF0


def test_clear_interrupt_flag_register_vblank(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_vblank_interrupt()
    interrupt_flag_register_fixture.clear_vblank_interrupt()

    assert not interrupt_flag_register_fixture.read_byte(0xFF0F) & 0x01


def test_clear_interrupt_flag_register_lcdc(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_lcdc_interrupt()
    interrupt_flag_register_fixture.clear_lcdc_interrupt()

    assert not interrupt_flag_register_fixture.read_byte(0xFF0F) & 0x02
    
    
def test_clear_interrupt_flag_register_tima(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_tima_interrupt()
    interrupt_flag_register_fixture.clear_tima_interrupt()

    assert not interrupt_flag_register_fixture.read_byte(0xFF0F) & 0x04
    
    
def test_clear_interrupt_flag_register_serial(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_serial_interrupt()
    interrupt_flag_register_fixture.clear_serial_interrupt()

    assert not interrupt_flag_register_fixture.read_byte(0xFF0F) & 0x08
    
    
def test_clear_interrupt_flag_register_joypad(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_joypad_interrupt()
    interrupt_flag_register_fixture.clear_joypad_interrupt()

    assert not interrupt_flag_register_fixture.read_byte(0xFF0F) & 0x10


def test_interrupt_register_write_byte_maintains_top_4_bit_1s(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.write_byte(0xFF0F, 0x10)

    assert interrupt_flag_register_fixture._data[0] == 0xF0


def test_interrupt_register_get_interrupt(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_vblank_interrupt()

    assert interrupt_flag_register_fixture.get_interrupt_bits() == 0x01

    interrupt_flag_register_fixture.set_lcdc_interrupt()

    assert interrupt_flag_register_fixture.get_interrupt_bits() == 0x03


def test_interrupt_flag_register_clear_by_bit(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_vblank_interrupt()

    interrupt_flag_register_fixture.clear_interrupt_by_bit(interrupt_flag_register_fixture.INTERRUPT_VBLANK)

    assert interrupt_flag_register_fixture.get_interrupt_bits() == 0

    interrupt_flag_register_fixture.set_lcdc_interrupt()

    interrupt_flag_register_fixture.clear_interrupt_by_bit(interrupt_flag_register_fixture.INTERRUPT_LCDC)

    assert interrupt_flag_register_fixture.get_interrupt_bits() == 0

    interrupt_flag_register_fixture.set_tima_interrupt()

    interrupt_flag_register_fixture.clear_interrupt_by_bit(interrupt_flag_register_fixture.INTERRUPT_TIMA)

    assert interrupt_flag_register_fixture.get_interrupt_bits() == 0

    interrupt_flag_register_fixture.set_serial_interrupt()

    interrupt_flag_register_fixture.clear_interrupt_by_bit(interrupt_flag_register_fixture.INTERRUPT_SERIAL)

    assert interrupt_flag_register_fixture.get_interrupt_bits() == 0

    interrupt_flag_register_fixture.set_joypad_interrupt()

    interrupt_flag_register_fixture.clear_interrupt_by_bit(interrupt_flag_register_fixture.INTERRUPT_JOYPAD)

    assert interrupt_flag_register_fixture.get_interrupt_bits() == 0

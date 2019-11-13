import pytest

from gameboy.interrupt_enable_register import InterruptEnableRegister
from gameboy.interrupt_flag_register import InterruptFlagRegister


@pytest.fixture()
def interrupt_enable_register_fixture() -> InterruptEnableRegister:
    return InterruptEnableRegister()


def test_interrupt_flag_register_init(interrupt_enable_register_fixture):
    assert len(interrupt_enable_register_fixture._data) == 1
    assert interrupt_enable_register_fixture._data[0] == 0
    assert interrupt_enable_register_fixture._base_address == 0xFFFF


def test_interrupt_flag_register_enable_vblank(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_vblank_interrupt()
    assert interrupt_enable_register_fixture.read_byte(0xFFFF) == 0x01
    
    
def test_interrupt_flag_register_enable_lcdc(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_lcdc_interrupt()
    assert interrupt_enable_register_fixture.read_byte(0xFFFF) == 0x02


def test_interrupt_flag_register_enable_tima(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_tima_interrupt()
    assert interrupt_enable_register_fixture.read_byte(0xFFFF) == 0x04


def test_interrupt_flag_register_enable_serial(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_serial_interrupt()
    assert interrupt_enable_register_fixture.read_byte(0xFFFF) == 0x08


def test_interrupt_flag_register_enable_joypad(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_joypad_interrupt()
    assert interrupt_enable_register_fixture.read_byte(0xFFFF) == 0x10


def test_disable_interrupt_flag_register_vblank(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_vblank_interrupt()
    interrupt_enable_register_fixture.disable_vblank_interrupt()

    assert not interrupt_enable_register_fixture.read_byte(0xFFFF) & 0x01


def test_disable_interrupt_flag_register_lcdc(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_lcdc_interrupt()
    interrupt_enable_register_fixture.disable_lcdc_interrupt()

    assert not interrupt_enable_register_fixture.read_byte(0xFFFF) & 0x02
    
    
def test_disable_interrupt_flag_register_tima(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_tima_interrupt()
    interrupt_enable_register_fixture.disable_tima_interrupt()

    assert not interrupt_enable_register_fixture.read_byte(0xFFFF) & 0x04
    
    
def test_disable_interrupt_flag_register_serial(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_serial_interrupt()
    interrupt_enable_register_fixture.disable_serial_interrupt()

    assert not interrupt_enable_register_fixture.read_byte(0xFFFF) & 0x08
    
    
def test_disable_interrupt_flag_register_joypad(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_joypad_interrupt()
    interrupt_enable_register_fixture.disable_joypad_interrupt()

    assert not interrupt_enable_register_fixture.read_byte(0xFFFF) & 0x10


def test_interrupt_register_get_interrupt(interrupt_enable_register_fixture):
    interrupt_enable_register_fixture.enable_vblank_interrupt()

    assert interrupt_enable_register_fixture.get_interrupt_enabled_bits() == 0x01

    interrupt_enable_register_fixture.enable_lcdc_interrupt()

    assert interrupt_enable_register_fixture.get_interrupt_enabled_bits() == 0x03

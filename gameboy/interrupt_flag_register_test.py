import pytest

from gameboy.interrupt_flag_register import InterruptFlagRegister


@pytest.fixture()
def interrupt_flag_register_fixture():
    return InterruptFlagRegister()


def test_interrupt_flag_register_init(interrupt_flag_register_fixture):
    assert len(interrupt_flag_register_fixture._data) == 1


def test_interrupt_flag_register_set_tima(interrupt_flag_register_fixture):
    interrupt_flag_register_fixture.set_tima_interrupt()
    assert interrupt_flag_register_fixture.read_byte(0xFF0F) == 0x04

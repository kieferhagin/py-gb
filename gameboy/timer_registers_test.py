from unittest import mock

import pytest

from gameboy.timer_registers import TimerRegisters


@pytest.fixture()
def timer_registers_fixture() -> TimerRegisters:
    return TimerRegisters(on_set_tima_interrupt=mock.Mock())


def test_timer_registers_init(timer_registers_fixture):
    assert len(timer_registers_fixture._data) == 4
    assert timer_registers_fixture._divider_cycle_clock is not None
    assert timer_registers_fixture._timer_overflow is False
    assert timer_registers_fixture._timer_loading_modulo is False


def test_timer_registers_rest(timer_registers_fixture):
    divider_clock_mock = mock.Mock()

    timer_registers_fixture._divider_cycle_clock = divider_clock_mock

    timer_registers_fixture.reset()

    divider_clock_mock.reset.assert_called_once()


def test_timer_registers_write_byte(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 4)

    assert timer_registers_fixture._data[3] == 4


def test_timer_registers_tick(timer_registers_fixture):
    cycle_clock_mock = mock.Mock()
    cycle_clock_mock.get_total_machine_cycles.return_value = 4
    cycle_clock_mock.get_total_clock_cycles.return_value = 16

    timer_registers_fixture._divider_cycle_clock = cycle_clock_mock
    timer_registers_fixture._timer_cycle_clock = cycle_clock_mock

    total_machine_cycles = timer_registers_fixture.tick(4)

    timer_registers_fixture._divider_cycle_clock.tick.assert_called_once_with(4)

    assert total_machine_cycles == 4


def test_timer_registers_write_byte_divider_resets_clocks(timer_registers_fixture):
    timer_registers_fixture._divider_cycle_clock.tick(5)
    timer_registers_fixture._increment_timer_counter()
    timer_registers_fixture.write_byte(timer_registers_fixture.DIVIDER_ADDRESS, 100)

    assert timer_registers_fixture._divider_cycle_clock.get_total_machine_cycles() == 0
    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0


def test_timer_registers_get_divider_returns_64th_machine_clock(timer_registers_fixture):
    timer_registers_fixture.tick()

    assert timer_registers_fixture.get_divider_timer_value() == 0

    timer_registers_fixture.tick(63)

    assert timer_registers_fixture.get_divider_timer_value() == 1

    timer_registers_fixture.tick()

    assert timer_registers_fixture.get_divider_timer_value() == 1

    timer_registers_fixture.tick(63)

    assert timer_registers_fixture.get_divider_timer_value() == 2


def test_timer_registers_read_byte_divider(timer_registers_fixture):
    timer_registers_fixture.tick(64)
    assert timer_registers_fixture.read_byte(timer_registers_fixture.DIVIDER_ADDRESS) == 1


def test_timer_registers_divider_overflows_255(timer_registers_fixture):
    timer_registers_fixture.tick(64 * 255)
    assert timer_registers_fixture.read_byte(timer_registers_fixture.DIVIDER_ADDRESS) == 255

    timer_registers_fixture.tick(64)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.DIVIDER_ADDRESS) == 0

    timer_registers_fixture.tick(64)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.DIVIDER_ADDRESS) == 1


def test_timer_registers_get_timer_enabled(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 4)

    assert timer_registers_fixture.get_timer_clock_enabled() is True


def test_timer_registers_get_timer_disbled(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 3)

    assert timer_registers_fixture.get_timer_clock_enabled() is False


def test_timer_get_falling_edge_bit_1024(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 0)
    timer_registers_fixture.tick(1)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 0

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 0)
    timer_registers_fixture.tick(127)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 0

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 0)
    timer_registers_fixture.tick(128)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 512

    timer_registers_fixture.reset()


def test_timer_get_falling_edge_bit_16(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 1)
    timer_registers_fixture.tick(1)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 0

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 1)
    timer_registers_fixture.tick(2)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 8

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 1)
    timer_registers_fixture.tick(127)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 8

    timer_registers_fixture.reset()


def test_timer_get_falling_edge_bit_64(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 2)
    timer_registers_fixture.tick(2)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 0

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 2)
    timer_registers_fixture.tick(4)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 0

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 2)
    timer_registers_fixture.tick(10)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 32

    timer_registers_fixture.reset()


def test_timer_get_falling_edge_bit_256(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 3)
    timer_registers_fixture.tick(2)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 0

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 3)
    timer_registers_fixture.tick(31)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 0

    timer_registers_fixture.reset()

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 3)
    timer_registers_fixture.tick(32)

    assert timer_registers_fixture.get_timer_falling_edge_bit() == 128

    timer_registers_fixture.reset()


def test_timer_registers_write_timer_control(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_CONTROL, 10)

    assert timer_registers_fixture.get_timer_control_value() == 10


def test_timer_registers_falling_edge_write_timer_control(timer_registers_fixture):
    timer_registers_fixture._data[3] = 0b00000110  # Enabled, 64
    timer_registers_fixture.tick(8)

    timer_registers_fixture.update_timer_control(0b00000111)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 1


def test_timer_registers_increment_timer_clock(timer_registers_fixture):
    timer_registers_fixture._data[3] = 0b00000110  # Enabled, 64
    timer_registers_fixture.tick(63)

    old_falling_edge_bit = timer_registers_fixture.get_timer_falling_edge_bit()

    timer_registers_fixture.tick(1)

    assert timer_registers_fixture.try_increment_timer_counter(old_falling_edge_bit)


def test_timer_registers_tick_increments_timer_clock_falling_edge(timer_registers_fixture):
    timer_registers_fixture._data[3] = 0b00000110  # Enabled, 64
    timer_registers_fixture.tick(63)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0

    timer_registers_fixture.tick(1)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 1


def test_timer_registers_tick_no_increments_timer_clock_no_falling_edge(timer_registers_fixture):
    timer_registers_fixture._data[3] = 0b00000110  # Enabled, 64
    timer_registers_fixture.tick(62)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0

    timer_registers_fixture.tick(1)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0


def test_timer_register_clear_timer(timer_registers_fixture):
    timer_registers_fixture._increment_timer_counter()

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 1

    timer_registers_fixture._clear_timer_counter()

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0


def test_timer_register_set_timer_overflow(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_ADDRESS, 255)

    timer_registers_fixture._increment_timer_counter()

    assert timer_registers_fixture.get_timer_overflow()
    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0


def test_timer_register_clear_timer_overflow(timer_registers_fixture):
    timer_registers_fixture._timer_overflow = True
    timer_registers_fixture.clear_timer_overflow()

    assert timer_registers_fixture._timer_overflow is False


def test_timer_register_write_to_timer_counter_clears_overflow_state(timer_registers_fixture):
    timer_registers_fixture._timer_overflow = True

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_ADDRESS, 100)

    assert timer_registers_fixture._timer_overflow is False


def test_timer_register_ignore_timer_counter_writes_loading_modulo(timer_registers_fixture):
    timer_registers_fixture._timer_loading_modulo = True

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_ADDRESS, 100)

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0


def test_timer_register_writing_to_modulo_loading(timer_registers_fixture):
    timer_registers_fixture._timer_loading_modulo = False

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_MODULO, 100)
    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 0
    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_MODULO) == 100

    timer_registers_fixture._timer_loading_modulo = True

    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_MODULO, 100)
    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 100
    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_MODULO) == 100


def test_timer_register_tick_clears_modulo_loading(timer_registers_fixture):
    timer_registers_fixture._timer_loading_modulo = True
    timer_registers_fixture.tick()
    assert not timer_registers_fixture._timer_loading_modulo


def test_timer_register_tick_clears_overflow(timer_registers_fixture):
    timer_registers_fixture._timer_overflow = True
    timer_registers_fixture.tick()
    assert not timer_registers_fixture._timer_overflow


def test_timer_register_tick_overflowed_sets_timer_to_modulo(timer_registers_fixture):
    timer_registers_fixture.write_byte(timer_registers_fixture.TIMER_MODULO, 100)

    timer_registers_fixture._timer_overflow = True
    timer_registers_fixture.tick()

    assert timer_registers_fixture.read_byte(timer_registers_fixture.TIMER_ADDRESS) == 100
    assert timer_registers_fixture._timer_loading_modulo
    timer_registers_fixture._on_set_tima_interrupt.assert_called_once()

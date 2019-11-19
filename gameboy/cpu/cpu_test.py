from unittest import mock
from unittest.mock import call

import pytest

from gameboy.cpu.cpu import CPU
from gameboy.memory.interrupt_flag_register import InterruptFlagRegister
from gameboy.memory.memory_unit import MemoryUnit


@pytest.fixture()
def cpu_fixture() -> CPU:
    return CPU(MemoryUnit())


def test_cpu_init(cpu_fixture):
    assert cpu_fixture._registers is not None
    assert cpu_fixture._cycle_clock is not None
    assert cpu_fixture._cpu_instructions is not None
    assert cpu_fixture._cpu_instructions._cpu == cpu_fixture
    assert cpu_fixture._is_halted is False
    assert cpu_fixture._interrupt_enable_pending is False


def test_cpu_reset(cpu_fixture):
    cpu_fixture._registers = mock.Mock()
    cpu_fixture._cycle_clock = mock.Mock()
    cpu_fixture._is_halted = True

    cpu_fixture.reset()

    cpu_fixture._registers.reset.assert_called_once()
    cpu_fixture._cycle_clock.reset.assert_called_once()
    assert not cpu_fixture._is_halted


def test_cpu_get_registers(cpu_fixture):
    assert cpu_fixture.get_registers() == cpu_fixture._registers


def test_cpu_get_memory_unit(cpu_fixture):
    assert cpu_fixture.get_memory_unit() == cpu_fixture._memory_unit


def test_cpu_get_cycle_clock(cpu_fixture):
    assert cpu_fixture.get_cycle_clock() == cpu_fixture._cycle_clock


def test_cpu_get_raised_enabled_interrupt_bits(cpu_fixture):
    assert cpu_fixture._get_raised_enabled_interrupt_bits() == 0

    cpu_fixture._memory_unit \
        .get_interrupt_flag_register() \
        .set_tima_interrupt()

    cpu_fixture._memory_unit \
        .get_interrupt_enable_register() \
        .enable_tima_interrupt()

    assert cpu_fixture._get_raised_enabled_interrupt_bits() == InterruptFlagRegister.INTERRUPT_TIMA

    cpu_fixture._memory_unit \
        .get_interrupt_flag_register() \
        .set_lcdc_interrupt()

    assert cpu_fixture._get_raised_enabled_interrupt_bits() == InterruptFlagRegister.INTERRUPT_TIMA

    cpu_fixture._memory_unit \
        .get_interrupt_enable_register() \
        .enable_lcdc_interrupt()

    assert cpu_fixture._get_raised_enabled_interrupt_bits() == InterruptFlagRegister.INTERRUPT_TIMA | InterruptFlagRegister.INTERRUPT_LCDC


def test_cpu_clear_halted(cpu_fixture):
    cpu_fixture._is_halted = True
    cpu_fixture.clear_halted()

    assert not cpu_fixture._is_halted


def test_cpu_set_halted(cpu_fixture):
    cpu_fixture._is_halted = False
    cpu_fixture.set_halted()

    assert cpu_fixture._is_halted


def test_cpu_handle_interrupts_no_interrupts_no_execute(cpu_fixture):
    cpu_fixture.set_halted()
    cpu_fixture._handle_interrupts()

    assert cpu_fixture._is_halted


def test_cpu_handle_interrupts_clears_halted(cpu_fixture):
    cpu_fixture.set_halted()

    cpu_fixture._memory_unit.get_interrupt_flag_register().set_vblank_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_vblank_interrupt()

    cpu_fixture._handle_interrupts()

    assert not cpu_fixture._is_halted


def test_cpu_handle_interrupts_no_handle_if_global_disable(cpu_fixture):
    cpu_fixture._registers.disable_interrupts()

    cpu_fixture._memory_unit.get_interrupt_flag_register().set_vblank_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_vblank_interrupt()

    cpu_fixture._handle_interrupt = mock.Mock()

    cpu_fixture._handle_interrupts()

    cpu_fixture._handle_interrupt.assert_not_called()


def test_cpu_handle_interrupts_iterates_all_interrupts(cpu_fixture):
    cpu_fixture._registers.enable_interrupts()

    cpu_fixture._memory_unit.get_interrupt_flag_register().set_joypad_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_joypad_interrupt()

    cpu_fixture._handle_interrupt = mock.Mock()
    cpu_fixture._handle_interrupt.return_value = False

    cpu_fixture._handle_interrupts()

    assert cpu_fixture._handle_interrupt.call_count == 5

    cpu_fixture._handle_interrupt.assert_has_calls([
        call(0),
        call(1),
        call(2),
        call(3),
        call(4),
    ])


def test_cpu_handle_interrupts_iterates_until_one_processed(cpu_fixture):
    cpu_fixture._registers.enable_interrupts()

    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    cpu_fixture._handle_interrupt = mock.Mock()
    cpu_fixture._handle_interrupt.side_effect = [False, False, True]

    cpu_fixture._handle_interrupts()

    assert cpu_fixture._handle_interrupt.call_count == 3

    cpu_fixture._handle_interrupt.assert_has_calls([
        call(0),
        call(1),
        call(2)
    ])


def test_cpu_handle_interrupt_returns_true_if_processed(cpu_fixture):
    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    assert cpu_fixture._handle_interrupt(2)


def test_cpu_handle_interrupt_returns_false_if_not_processed(cpu_fixture):
    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    assert not cpu_fixture._handle_interrupt(0)


def test_cpu_handle_interrupt_disabled_interrupts_if_processed(cpu_fixture):
    cpu_fixture._registers.enable_interrupts()

    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    cpu_fixture._handle_interrupt(2)

    assert not cpu_fixture._registers.get_interrupts_enabled()


def test_cpu_handle_interrupt_not_disabled_interrupts_if_not_processed(cpu_fixture):
    cpu_fixture._registers.enable_interrupts()

    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    cpu_fixture._handle_interrupt(0)

    assert cpu_fixture._registers.get_interrupts_enabled()


def test_cpu_handle_interrupt_clears_bit_if_processed(cpu_fixture):
    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    cpu_fixture._handle_interrupt(2)

    assert not cpu_fixture._memory_unit.get_interrupt_flag_register().get_interrupt_bits()


def test_cpu_handle_interrupt_not_clears_bit_if_not_processed(cpu_fixture):
    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    cpu_fixture._handle_interrupt(0)

    assert cpu_fixture._memory_unit.get_interrupt_flag_register().get_interrupt_bits() == 0x04


def test_cpu_handle_interrupt_call_40_if_processed(cpu_fixture):
    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    cpu_fixture._cpu_instructions = mock.Mock()

    cpu_fixture._handle_interrupt(2)

    cpu_fixture._cpu_instructions.call.assert_called_once_with(0x50)


def test_cpu_handle_interrupt_not_call_40_if_not_processed(cpu_fixture):
    cpu_fixture._memory_unit.get_interrupt_flag_register().set_tima_interrupt()
    cpu_fixture._memory_unit.get_interrupt_enable_register().enable_tima_interrupt()

    cpu_fixture._cpu_instructions = mock.Mock()

    cpu_fixture._handle_interrupt(1)

    cpu_fixture._cpu_instructions.call.assert_not_called()


def test_cpu_read_immediate_byte(cpu_fixture):
    cpu_fixture._memory_unit.write_byte(0xC000, 15)
    cpu_fixture._registers._program_counter = 0xC000

    assert cpu_fixture.read_immediate_byte() == 15
    assert cpu_fixture._registers._program_counter == 0xC001


def test_cpu_read_immediate_word(cpu_fixture):
    cpu_fixture._memory_unit.write_word(0xC000, 500)
    cpu_fixture._registers._program_counter = 0xC000

    assert cpu_fixture.read_immediate_word() == 500
    assert cpu_fixture._registers._program_counter == 0xC002


def test_cpu_read_immediate_signed_byte(cpu_fixture):
    cpu_fixture._memory_unit.write_byte(0xC000, 255)
    cpu_fixture._registers._program_counter = 0xC000

    assert cpu_fixture.read_immediate_signed_byte() == -1
    assert cpu_fixture._registers._program_counter == 0xC001


def test_cpu_push_word_to_stack(cpu_fixture):
    cpu_fixture.push_word_to_stack(500)
    assert cpu_fixture._memory_unit.read_word(cpu_fixture._registers._stack_pointer) == 500
    assert cpu_fixture._registers._stack_pointer == 0xFFFE - 2


def test_cpu_pop_word_from_stack(cpu_fixture):
    cpu_fixture.push_word_to_stack(500)
    assert cpu_fixture.pop_word_from_stack() == 500
    assert cpu_fixture._registers._stack_pointer == 0xFFFE


def test_cpu_step_halted(cpu_fixture):
    cpu_fixture._is_halted = True
    cpu_fixture._execute_operation = mock.Mock()

    cpu_fixture.step()

    assert cpu_fixture._cycle_clock.get_total_machine_cycles() == 1
    cpu_fixture._execute_operation.assert_not_called()


def test_cpu_step_interrupt_enable_pending(cpu_fixture):
    cpu_fixture._registers.set_program_counter(0xC000)
    cpu_fixture._registers.disable_interrupts()
    cpu_fixture._interrupt_enable_pending = True

    cpu_fixture.step()

    assert cpu_fixture._registers.get_interrupts_enabled()
    assert not cpu_fixture._interrupt_enable_pending


def test_cpu_step_interrupt_enable_not_pending(cpu_fixture):
    cpu_fixture._registers.set_program_counter(0xC000)
    cpu_fixture._registers.disable_interrupts()
    cpu_fixture._interrupt_enable_pending = False

    cpu_fixture.step()

    assert not cpu_fixture._registers.get_interrupts_enabled()


def test_cpu_step_executes_next_op_code(cpu_fixture):
    cpu_fixture._execute_operation = mock.Mock()
    cpu_fixture._registers.set_program_counter(0xC000)
    cpu_fixture._memory_unit.write_byte(0xC000, 0x01)

    cpu_fixture.step()

    cpu_fixture._execute_operation.assert_called_once_with(0x01)

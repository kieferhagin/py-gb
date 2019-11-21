from unittest import mock

import pytest

from gameboy.cpu.cpu import CPU
from gameboy.cpu.cpu_instructions import CPUInstructions
from gameboy.memory.memory_unit import MemoryUnit


@pytest.fixture()
def cpu_instructions_fixture():
    return CPUInstructions(CPU(MemoryUnit()))


def test_cpu_instructions_init(cpu_instructions_fixture):
    assert cpu_instructions_fixture._cpu is not None


def test_cpu_instructions_is_half_carry(cpu_instructions_fixture):
    result = 0b00010000
    input_ = 0b00001000

    assert cpu_instructions_fixture._is_half_carry(result=result, input_=input_)

    result = 0b00001000
    input_ = 0b00000100

    assert not cpu_instructions_fixture._is_half_carry(result=result, input_=input_)


def test_cpu_instructions_is_carry(cpu_instructions_fixture):
    result = 0b0000000100000000
    input_ = 0b0000000010000000

    assert cpu_instructions_fixture._is_carry(result=result, input_=input_)

    result = 0b0000000010000000
    input_ = 0b0000000001000000

    assert not cpu_instructions_fixture._is_carry(result=result, input_=input_)


def test_cpu_instructions_call(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._program_counter = 1

    cpu_instructions_fixture.call(0x0040)
    assert cpu_instructions_fixture._cpu._memory_unit.read_word(cpu_instructions_fixture._cpu._registers._stack_pointer) == 1
    assert cpu_instructions_fixture._cpu._registers._program_counter == 0x0040
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 5


def test_cpu_instructions_load(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 100
    cpu_instructions_fixture._cpu._registers._register_b = 0

    cpu_instructions_fixture.load(from_register='a', to_register='b')

    assert cpu_instructions_fixture._cpu._registers._register_b == 100
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 1

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load(from_register='z', to_register='b')

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load(from_register='b', to_register='z')

    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 1


def test_cpu_instructions_load_16_bit(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers.write_hl(100)

    cpu_instructions_fixture.load_16_bit(from_register='hl', to_register='sp')

    assert cpu_instructions_fixture._cpu._registers.get_stack_pointer() == 100
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2

    cpu_instructions_fixture._cpu._registers.write_bc(100)

    cpu_instructions_fixture.load_16_bit(from_register='bc', to_register='de')

    assert cpu_instructions_fixture._cpu._registers.read_de() == 100

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load(from_register='bb', to_register='hl')

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load(from_register='zz', to_register='sp')


def test_cpu_instructions_load_16_bit_offset(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers.write_hl(145)
    cpu_instructions_fixture._cpu._registers._stack_pointer = 144
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 16)  # -16 when signed
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._registers.update_flag_zero(True)
    cpu_instructions_fixture._cpu._registers.update_flag_subtract(True)
    cpu_instructions_fixture._cpu._registers.update_flag_half_carry(False)
    cpu_instructions_fixture._cpu._registers.update_flag_carry(False)

    cpu_instructions_fixture.load_16_bit(from_register='hl', to_register='sp', immediate_signed_offset=True)

    assert cpu_instructions_fixture._cpu._registers.get_stack_pointer() == 161
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 3
    assert not cpu_instructions_fixture._cpu._registers.read_flag_zero()
    assert not cpu_instructions_fixture._cpu._registers.read_flag_subtract()
    assert not cpu_instructions_fixture._cpu._registers.read_flag_half_carry()
    assert not cpu_instructions_fixture._cpu._registers.read_flag_carry()


def test_cpu_instructions_load_register_with_memory_hl(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers.write_hl(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 114)

    cpu_instructions_fixture.load_register_with_memory('b')

    assert cpu_instructions_fixture._cpu._registers._register_b == 114
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load_register_with_memory('z')

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load_register_with_memory('d', 'pz')

    cpu_instructions_fixture._cpu._registers.write_bc(0xC000)

    cpu_instructions_fixture.load_register_with_memory('d', 'bc', increment_memory_register=True)

    assert cpu_instructions_fixture._cpu._registers._register_d == 114
    assert cpu_instructions_fixture._cpu._registers.read_bc() == 0xC001

    cpu_instructions_fixture._cpu._registers.write_de(0xC000)

    cpu_instructions_fixture.load_register_with_memory('c', 'de', decrement_memory_register=True)

    assert cpu_instructions_fixture._cpu._registers._register_c == 114
    assert cpu_instructions_fixture._cpu._registers.read_de() == 0xBFFF


def test_cpu_instructions_load_memory_with_register(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers.write_hl(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0)
    cpu_instructions_fixture._cpu._registers._register_b = 114

    cpu_instructions_fixture.load_memory_with_register('b')

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xC000) == 114
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load_memory_with_register('z')

    with pytest.raises(AttributeError):
        cpu_instructions_fixture.load_memory_with_register('d', 'pz')

    cpu_instructions_fixture._cpu._registers.write_bc(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0)
    cpu_instructions_fixture._cpu._registers._register_d = 115

    cpu_instructions_fixture.load_memory_with_register('d', 'bc', increment_memory_register=True)

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xC000) == 115
    assert cpu_instructions_fixture._cpu._registers.read_bc() == 0xC001

    cpu_instructions_fixture._cpu._registers.write_de(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0)
    cpu_instructions_fixture._cpu._registers._register_b = 116

    cpu_instructions_fixture.load_memory_with_register('b', 'de', decrement_memory_register=True)

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xC000) == 116
    assert cpu_instructions_fixture._cpu._registers.read_de() == 0xBFFF


def test_cpu_instructions_load_memory_with_immediate(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers.write_hl(0xC005)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 115)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000

    cpu_instructions_fixture.load_memory_with_immediate()

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xC005) == 115
    assert cpu_instructions_fixture._cpu._registers._program_counter == 0xC001
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 3


def test_cpu_instructions_load_immediate_memory_with_register(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_word(0xC000, 0xC005)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._registers._register_a = 144

    cpu_instructions_fixture.load_immediate_memory_with_register('a')

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xC005) == 144
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 4


def test_cpu_instructions_load_immediate_memory_with_register_high_memory(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0x80)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._registers._register_a = 144

    cpu_instructions_fixture.load_immediate_memory_with_register('a', high_memory_load=True)

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xFF00 + 0x80) == 144
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 3


def test_cpu_instructions_load_immediate_memory_with_16_bit_register(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_word(0xC000, 0xC005)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._registers._stack_pointer = 0xF1F2

    cpu_instructions_fixture.load_immediate_memory_with_16_bit_register('sp')

    assert cpu_instructions_fixture._cpu._memory_unit.read_word(0xC005) == 0xF1F2
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 5


def test_cpu_instructions_load_register_with_immediate_memory(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_word(0xC000, 0xC005)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC005, 123)

    cpu_instructions_fixture.load_register_with_immediate_memory('a')

    assert cpu_instructions_fixture._cpu._registers._register_a == 123
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 4


def test_cpu_instructions_load_register_with_immediate_memory_high_memory(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0x80)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xFF80, 123)

    cpu_instructions_fixture.load_register_with_immediate_memory('a', high_memory_read=True)

    assert cpu_instructions_fixture._cpu._registers._register_a == 123
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 3


def test_cpu_instructions_load_offset_memory_at_register_with_register(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_c = 0x80
    cpu_instructions_fixture._cpu._registers._register_a = 115

    cpu_instructions_fixture.load_offset_memory_at_register_with_register('c', 'a')

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xFF80) == 115
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2


def test_cpu_instructions_load_register_with_offset_memory_at_register(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_c = 0x80
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xFF80, 115)

    cpu_instructions_fixture.load_register_with_offset_memory_at_register('a', 'c')

    assert cpu_instructions_fixture._cpu._registers._register_a == 115
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2


def test_cpu_instructions_load_register_with_immediate_byte(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0x0F)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000

    cpu_instructions_fixture.load_register_with_immediate_byte('b')

    assert cpu_instructions_fixture._cpu._registers._register_b == 0x0F
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2


def test_cpu_instructions_load_register_with_immediate_word(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_word(0xC000, 0x1234)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000

    cpu_instructions_fixture.load_register_with_immediate_word('sp')

    assert cpu_instructions_fixture._cpu._registers._stack_pointer == 0x1234
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 3


def test_cpu_instructions_pop_stack(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu.push_word_to_stack(0x1234)

    cpu_instructions_fixture.pop_stack_to_register('bc')

    assert cpu_instructions_fixture._cpu._registers.read_bc() == 0x1234
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 3


def test_cpu_instructions_push_stack(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers.write_hl(0x1234)

    cpu_instructions_fixture.push_register_to_stack('hl')

    assert cpu_instructions_fixture._cpu.pop_word_from_stack() == 0x1234
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 3


def test_cpu_instructions_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 0x00
    cpu_instructions_fixture._cpu._registers._register_b = 0x0F

    cpu_instructions_fixture.add_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x0F
    assert cpu_instructions_fixture._cpu._registers._register_b == 0x0F
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 1


def test_cpu_instructions_add_8_flags(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 0xFF
    cpu_instructions_fixture._cpu._registers._register_b = 0x01

    cpu_instructions_fixture.add_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x00
    assert cpu_instructions_fixture._cpu._registers.read_flag_zero()
    assert not cpu_instructions_fixture._cpu._registers.read_flag_subtract()

    cpu_instructions_fixture._cpu._registers._register_a = 0xFF
    cpu_instructions_fixture._cpu._registers._register_b = 0x02

    cpu_instructions_fixture.add_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x01
    assert cpu_instructions_fixture._cpu._registers.read_flag_carry()
    assert not cpu_instructions_fixture._cpu._registers.read_flag_subtract()

    cpu_instructions_fixture._cpu._registers._register_a = 0x7F
    cpu_instructions_fixture._cpu._registers._register_b = 0x01

    cpu_instructions_fixture.add_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x80
    assert cpu_instructions_fixture._cpu._registers.read_flag_half_carry()
    assert not cpu_instructions_fixture._cpu._registers.read_flag_subtract()


def test_cpu_instructions_add_8_with_carry(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 0xFF
    cpu_instructions_fixture._cpu._registers._register_b = 0x02

    cpu_instructions_fixture.add_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x01
    assert cpu_instructions_fixture._cpu._registers.read_flag_carry()
    assert not cpu_instructions_fixture._cpu._registers.read_flag_subtract()

    cpu_instructions_fixture.add_8_bit_registers('a', 'b', with_carry_bit=True)

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x04
    assert not cpu_instructions_fixture._cpu._registers.read_flag_carry()


def test_cpu_instructions_add_8_bit_hl(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 0x05
    cpu_instructions_fixture._cpu._registers.write_hl(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0x12)

    cpu_instructions_fixture.add_8_bit_hl_memory_to_register('a')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x17
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2

    cpu_instructions_fixture._cpu._registers._register_a = 0x05
    cpu_instructions_fixture._cpu._registers.write_hl(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0x12)
    cpu_instructions_fixture._cpu._registers.update_flag_carry(True)

    cpu_instructions_fixture.add_8_bit_hl_memory_to_register('a', with_carry_bit=True)

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x18


def test_cpu_instructions_add_8_bit_immediate(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 0x05
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0x12)

    cpu_instructions_fixture.add_8_bit_immediate_to_register('a')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x17
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2

    cpu_instructions_fixture._cpu._registers._register_a = 0x05
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0x12)
    cpu_instructions_fixture._cpu._registers.update_flag_carry(True)

    cpu_instructions_fixture.add_8_bit_immediate_to_register('a', with_carry_bit=True)

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x18


def test_cpu_instructions_subtract_8_flags(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 0x01
    cpu_instructions_fixture._cpu._registers._register_b = 0x01

    cpu_instructions_fixture.subtract_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0x00
    assert cpu_instructions_fixture._cpu._registers.read_flag_zero()
    assert cpu_instructions_fixture._cpu._registers.read_flag_subtract()

    cpu_instructions_fixture._cpu._registers._register_a = 0x00
    cpu_instructions_fixture._cpu._registers._register_b = 0x01

    cpu_instructions_fixture.subtract_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 0xFF
    assert cpu_instructions_fixture._cpu._registers.read_flag_carry()
    assert cpu_instructions_fixture._cpu._registers.read_flag_subtract()

    cpu_instructions_fixture._cpu._registers._register_a = 0b00000100
    cpu_instructions_fixture._cpu._registers._register_b = 0b00001100

    cpu_instructions_fixture.subtract_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers.read_flag_half_carry()
    assert cpu_instructions_fixture._cpu._registers._register_a == 248
    assert cpu_instructions_fixture._cpu._registers.read_flag_subtract()


def test_cpu_instructions_subtract_8_with_carry(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 32
    cpu_instructions_fixture._cpu._registers._register_b = 33

    cpu_instructions_fixture.subtract_8_bit_registers('a', 'b')

    assert cpu_instructions_fixture._cpu._registers._register_a == 255
    assert cpu_instructions_fixture._cpu._registers.read_flag_carry()
    assert cpu_instructions_fixture._cpu._registers.read_flag_subtract()

    cpu_instructions_fixture.subtract_8_bit_registers('a', 'b', with_carry_bit=True)

    assert cpu_instructions_fixture._cpu._registers._register_a == 221
    assert not cpu_instructions_fixture._cpu._registers.read_flag_carry()


def test_cpu_instructions_subtract_8_bit_hl(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 12
    cpu_instructions_fixture._cpu._registers.write_hl(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 5)

    cpu_instructions_fixture.subtract_8_bit_hl_memory_to_register('a')

    assert cpu_instructions_fixture._cpu._registers._register_a == 7
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2

    cpu_instructions_fixture._cpu._registers._register_a = 12
    cpu_instructions_fixture._cpu._registers.write_hl(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 7)
    cpu_instructions_fixture._cpu._registers.update_flag_carry(True)

    cpu_instructions_fixture.subtract_8_bit_hl_memory_to_register('a', with_carry_bit=True)

    assert cpu_instructions_fixture._cpu._registers._register_a == 4


def test_cpu_instructions_subtract_8_bit_immediate(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._registers._register_a = 12
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 7)

    cpu_instructions_fixture.subtract_8_bit_immediate_to_register('a')

    assert cpu_instructions_fixture._cpu._registers._register_a == 5
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 2

    cpu_instructions_fixture._cpu._registers._register_a = 12
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 5)
    cpu_instructions_fixture._cpu._registers.update_flag_carry(True)

    cpu_instructions_fixture.subtract_8_bit_immediate_to_register('a', with_carry_bit=True)

    assert cpu_instructions_fixture._cpu._registers._register_a == 6



def test_cpu_instructions_0x40_ld_b_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x40)

    cpu_instructions_fixture.load.assert_called_once_with('b', 'b')


def test_cpu_instructions_0x41_ld_b_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x41)

    cpu_instructions_fixture.load.assert_called_once_with('b', 'c')


def test_cpu_instructions_0x42_ld_b_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x42)

    cpu_instructions_fixture.load.assert_called_once_with('b', 'd')


def test_cpu_instructions_0x43_ld_b_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x43)

    cpu_instructions_fixture.load.assert_called_once_with('b', 'e')


def test_cpu_instructions_0x44_ld_b_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x44)

    cpu_instructions_fixture.load.assert_called_once_with('b', 'h')


def test_cpu_instructions_0x45_ld_b_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x45)

    cpu_instructions_fixture.load.assert_called_once_with('b', 'l')


def test_cpu_instructions_0x47_ld_b_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x47)

    cpu_instructions_fixture.load.assert_called_once_with('b', 'a')


def test_cpu_instructions_0x48_ld_c_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x48)

    cpu_instructions_fixture.load.assert_called_once_with('c', 'b')


def test_cpu_instructions_0x49_ld_c_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x49)

    cpu_instructions_fixture.load.assert_called_once_with('c', 'c')


def test_cpu_instructions_0x4A_ld_c_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x4A)

    cpu_instructions_fixture.load.assert_called_once_with('c', 'd')


def test_cpu_instructions_0x4B_ld_c_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x4B)

    cpu_instructions_fixture.load.assert_called_once_with('c', 'e')


def test_cpu_instructions_0x4C_ld_c_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x4C)

    cpu_instructions_fixture.load.assert_called_once_with('c', 'h')


def test_cpu_instructions_0x4D_ld_c_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x4D)

    cpu_instructions_fixture.load.assert_called_once_with('c', 'l')


def test_cpu_instructions_0x4F_ld_c_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x4F)

    cpu_instructions_fixture.load.assert_called_once_with('c', 'a')

def test_cpu_instructions_0x50_ld_d_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x50)

    cpu_instructions_fixture.load.assert_called_once_with('d', 'b')


def test_cpu_instructions_0x51_ld_d_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x51)

    cpu_instructions_fixture.load.assert_called_once_with('d', 'c')


def test_cpu_instructions_0x52_ld_d_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x52)

    cpu_instructions_fixture.load.assert_called_once_with('d', 'd')


def test_cpu_instructions_0x53_ld_d_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x53)

    cpu_instructions_fixture.load.assert_called_once_with('d', 'e')


def test_cpu_instructions_0x54_ld_d_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x54)

    cpu_instructions_fixture.load.assert_called_once_with('d', 'h')


def test_cpu_instructions_0x55_ld_d_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x55)

    cpu_instructions_fixture.load.assert_called_once_with('d', 'l')


def test_cpu_instructions_0x57_ld_d_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x57)

    cpu_instructions_fixture.load.assert_called_once_with('d', 'a')


def test_cpu_instructions_0x58_ld_e_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x58)

    cpu_instructions_fixture.load.assert_called_once_with('e', 'b')


def test_cpu_instructions_0x59_ld_e_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x59)

    cpu_instructions_fixture.load.assert_called_once_with('e', 'c')


def test_cpu_instructions_0x5A_ld_e_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x5A)

    cpu_instructions_fixture.load.assert_called_once_with('e', 'd')


def test_cpu_instructions_0x5B_ld_e_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x5B)

    cpu_instructions_fixture.load.assert_called_once_with('e', 'e')


def test_cpu_instructions_0x5C_ld_e_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x5C)

    cpu_instructions_fixture.load.assert_called_once_with('e', 'h')


def test_cpu_instructions_0x5D_ld_e_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x5D)

    cpu_instructions_fixture.load.assert_called_once_with('e', 'l')


def test_cpu_instructions_0x5F_ld_e_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x5F)

    cpu_instructions_fixture.load.assert_called_once_with('e', 'a')


def test_cpu_instructions_0x60_ld_h_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x60)

    cpu_instructions_fixture.load.assert_called_once_with('h', 'b')


def test_cpu_instructions_0x61_ld_h_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x61)

    cpu_instructions_fixture.load.assert_called_once_with('h', 'c')


def test_cpu_instructions_0x62_ld_h_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x62)

    cpu_instructions_fixture.load.assert_called_once_with('h', 'd')


def test_cpu_instructions_0x63_ld_h_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x63)

    cpu_instructions_fixture.load.assert_called_once_with('h', 'e')


def test_cpu_instructions_0x64_ld_h_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x64)

    cpu_instructions_fixture.load.assert_called_once_with('h', 'h')


def test_cpu_instructions_0x65_ld_h_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x65)

    cpu_instructions_fixture.load.assert_called_once_with('h', 'l')


def test_cpu_instructions_0x67_ld_h_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x67)

    cpu_instructions_fixture.load.assert_called_once_with('h', 'a')


def test_cpu_instructions_0x68_ld_l_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x68)

    cpu_instructions_fixture.load.assert_called_once_with('l', 'b')


def test_cpu_instructions_0x69_ld_l_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x69)

    cpu_instructions_fixture.load.assert_called_once_with('l', 'c')


def test_cpu_instructions_0x6A_ld_l_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x6A)

    cpu_instructions_fixture.load.assert_called_once_with('l', 'd')


def test_cpu_instructions_0x6B_ld_l_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x6B)

    cpu_instructions_fixture.load.assert_called_once_with('l', 'e')


def test_cpu_instructions_0x6C_ld_l_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x6C)

    cpu_instructions_fixture.load.assert_called_once_with('l', 'h')


def test_cpu_instructions_0x6D_ld_l_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x6D)

    cpu_instructions_fixture.load.assert_called_once_with('l', 'l')


def test_cpu_instructions_0x6F_ld_l_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x6F)

    cpu_instructions_fixture.load.assert_called_once_with('l', 'a')


def test_cpu_instructions_0x78_ld_a_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x78)

    cpu_instructions_fixture.load.assert_called_once_with('a', 'b')


def test_cpu_instructions_0x79_ld_a_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x79)

    cpu_instructions_fixture.load.assert_called_once_with('a', 'c')


def test_cpu_instructions_0x7A_ld_a_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x7A)

    cpu_instructions_fixture.load.assert_called_once_with('a', 'd')


def test_cpu_instructions_0x7B_ld_a_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x7B)

    cpu_instructions_fixture.load.assert_called_once_with('a', 'e')


def test_cpu_instructions_0x7C_ld_a_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x7C)

    cpu_instructions_fixture.load.assert_called_once_with('a', 'h')


def test_cpu_instructions_0x7D_ld_a_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x7D)

    cpu_instructions_fixture.load.assert_called_once_with('a', 'l')


def test_cpu_instructions_0x7F_ld_a_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x7F)

    cpu_instructions_fixture.load.assert_called_once_with('a', 'a')


def test_cpu_instructions_0x46_ld_b_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x46)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('b')


def test_cpu_instructions_0x4E_ld_c_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x4E)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('c')


def test_cpu_instructions_0x56_ld_d_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x56)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('d')


def test_cpu_instructions_0x5E_ld_e_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x5E)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('e')


def test_cpu_instructions_0x66_ld_h_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x66)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('h')


def test_cpu_instructions_0x6E_ld_l_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x6E)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('l')


def test_cpu_instructions_0x7E_ld_a_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x7E)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('a')


def test_cpu_instructions_0x70_ld_hl_b(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x70)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('b')


def test_cpu_instructions_0x71_ld_hl_c(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x71)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('c')


def test_cpu_instructions_0x72_ld_hl_d(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x72)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('d')


def test_cpu_instructions_0x73_ld_hl_e(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x73)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('e')


def test_cpu_instructions_0x74_ld_hl_h(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x74)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('h')


def test_cpu_instructions_0x75_ld_hl_l(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x75)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('l')


def test_cpu_instructions_0x77_ld_hl_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x77)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('a')


def test_cpu_instructions_0x36_ld_hl_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_immediate = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x36)

    cpu_instructions_fixture.load_memory_with_immediate.assert_called_once()


def test_cpu_instructions_0x0A_ld_a_bc(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x0A)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('a', memory_register_16='bc')


def test_cpu_instructions_0x1A_ld_a_de(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x1A)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('a', memory_register_16='de')


def test_cpu_instructions_0x02_ld_bc_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x02)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('a', memory_register_16='bc')


def test_cpu_instructions_0x12_ld_de_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x12)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('a', memory_register_16='de')


def test_cpu_instructions_0xEA_ld_imm16_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_immediate_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xEA)

    cpu_instructions_fixture.load_immediate_memory_with_register.assert_called_once_with('a')


def test_cpu_instructions_0xFA_ld_a_imm16(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xFA)

    cpu_instructions_fixture.load_register_with_immediate_memory.assert_called_once_with('a')


def test_cpu_instructions_0x22_ld_hlincr_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x22)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('a', increment_memory_register=True)


def test_cpu_instructions_0x2A_ld_a_hlincr(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x2A)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('a', increment_memory_register=True)


def test_cpu_instructions_0x32_ld_hldecr_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x32)

    cpu_instructions_fixture.load_memory_with_register.assert_called_once_with('a', decrement_memory_register=True)


def test_cpu_instructions_0x3A_ld_a_hldecr(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x3A)

    cpu_instructions_fixture.load_register_with_memory.assert_called_once_with('a', decrement_memory_register=True)


def test_cpu_instructions_0xE0_ld_0xff00imm8_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_immediate_memory_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xE0)

    cpu_instructions_fixture.load_immediate_memory_with_register.assert_called_once_with('a', high_memory_load=True)


def test_cpu_instructions_0xE2_ld_0xff00_c_a(cpu_instructions_fixture):
    cpu_instructions_fixture.load_offset_memory_at_register_with_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xE2)

    cpu_instructions_fixture.load_offset_memory_at_register_with_register \
        .assert_called_once_with('c', 'a')


def test_cpu_instructions_0xF0_ld_a_0xf00imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_memory = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xF0)

    cpu_instructions_fixture.load_register_with_immediate_memory.assert_called_once_with('a', high_memory_read=True)


def test_cpu_instructions_0xF2_ld_a_0xFF00c(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_offset_memory_at_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xF2)

    cpu_instructions_fixture.load_register_with_offset_memory_at_register.assert_called_once_with('a', 'c')


def test_cpu_instructions_0x06_ld_b_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_byte = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x06)

    cpu_instructions_fixture.load_register_with_immediate_byte.assert_called_once_with('b')


def test_cpu_instructions_0x0E_ld_b_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_byte = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0X0E)

    cpu_instructions_fixture.load_register_with_immediate_byte.assert_called_once_with('c')


def test_cpu_instructions_0x16_ld_b_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_byte = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0X16)

    cpu_instructions_fixture.load_register_with_immediate_byte.assert_called_once_with('d')


def test_cpu_instructions_0x1E_ld_b_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_byte = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0X1E)

    cpu_instructions_fixture.load_register_with_immediate_byte.assert_called_once_with('e')


def test_cpu_instructions_0x26_ld_b_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_byte = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0X26)

    cpu_instructions_fixture.load_register_with_immediate_byte.assert_called_once_with('h')


def test_cpu_instructions_0x2E_ld_b_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_byte = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x2E)

    cpu_instructions_fixture.load_register_with_immediate_byte.assert_called_once_with('l')


def test_cpu_instructions_0x3E_ld_a_imm8(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_byte = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x3E)

    cpu_instructions_fixture.load_register_with_immediate_byte.assert_called_once_with('a')


def test_cpu_instructions_0x01_ld_bc_imm16(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_word = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x01)

    cpu_instructions_fixture.load_register_with_immediate_word.assert_called_once_with('bc')


def test_cpu_instructions_0x11_ld_bc_imm16(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_word = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x11)

    cpu_instructions_fixture.load_register_with_immediate_word.assert_called_once_with('de')


def test_cpu_instructions_0x21_ld_bc_imm16(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_word = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x21)

    cpu_instructions_fixture.load_register_with_immediate_word.assert_called_once_with('hl')


def test_cpu_instructions_0x31_ld_bc_imm16(cpu_instructions_fixture):
    cpu_instructions_fixture.load_register_with_immediate_word = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x31)

    cpu_instructions_fixture.load_register_with_immediate_word.assert_called_once_with('sp')


def test_cpu_instructions_0x08_ld_imm16_sp(cpu_instructions_fixture):
    cpu_instructions_fixture.load_immediate_memory_with_16_bit_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x08)

    cpu_instructions_fixture.load_immediate_memory_with_16_bit_register.assert_called_once_with('sp')


def test_cpu_instructions_0xF9_ld_sp_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.load_16_bit = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xF9)

    cpu_instructions_fixture.load_16_bit.assert_called_once_with('hl', 'sp')


def test_cpu_instructions_0xF8_ld_hl_sp_imm8signed(cpu_instructions_fixture):
    cpu_instructions_fixture.load_16_bit = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xF8)

    cpu_instructions_fixture.load_16_bit.assert_called_once_with('sp', 'hl', immediate_signed_offset=True)


def test_cpu_instructions_0xC1_pop_bc(cpu_instructions_fixture):
    cpu_instructions_fixture.pop_stack_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xC1)

    cpu_instructions_fixture.pop_stack_to_register.assert_called_once_with('bc')


def test_cpu_instructions_0xD1_pop_de(cpu_instructions_fixture):
    cpu_instructions_fixture.pop_stack_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xD1)

    cpu_instructions_fixture.pop_stack_to_register.assert_called_once_with('de')


def test_cpu_instructions_0xE1_pop_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.pop_stack_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xE1)

    cpu_instructions_fixture.pop_stack_to_register.assert_called_once_with('hl')


def test_cpu_instructions_0xF1_pop_af(cpu_instructions_fixture):
    cpu_instructions_fixture.pop_stack_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xF1)

    cpu_instructions_fixture.pop_stack_to_register.assert_called_once_with('af')


def test_cpu_instructions_0xC5_push_bc(cpu_instructions_fixture):
    cpu_instructions_fixture.push_register_to_stack = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xC5)

    cpu_instructions_fixture.push_register_to_stack.assert_called_once_with('bc')


def test_cpu_instructions_0xD5_push_de(cpu_instructions_fixture):
    cpu_instructions_fixture.push_register_to_stack = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xD5)

    cpu_instructions_fixture.push_register_to_stack.assert_called_once_with('de')


def test_cpu_instructions_0xE5_push_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.push_register_to_stack = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xE5)

    cpu_instructions_fixture.push_register_to_stack.assert_called_once_with('hl')


def test_cpu_instructions_0xF5_push_af(cpu_instructions_fixture):
    cpu_instructions_fixture.push_register_to_stack = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xF5)

    cpu_instructions_fixture.push_register_to_stack.assert_called_once_with('af')


def test_cpu_instructions_0x80_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x80)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'b')


def test_cpu_instructions_0x81_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x81)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'c')


def test_cpu_instructions_0x82_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x82)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'd')


def test_cpu_instructions_0x83_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x83)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'e')


def test_cpu_instructions_0x84_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x84)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'h')


def test_cpu_instructions_0x85_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x85)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'l')


def test_cpu_instructions_0x87_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x87)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'a')


def test_cpu_instructions_0x86_add_8_bit_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_hl_memory_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x86)

    cpu_instructions_fixture.add_8_bit_hl_memory_to_register.assert_called_once_with('a')


def test_cpu_instructions_0xC6_add_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_immediate_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xC6)

    cpu_instructions_fixture.add_8_bit_immediate_to_register.assert_called_once_with('a')


def test_cpu_instructions_0x88_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x88)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'b', with_carry_bit=True)


def test_cpu_instructions_0x89_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x89)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'c', with_carry_bit=True)


def test_cpu_instructions_0x8A_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x8A)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'd', with_carry_bit=True)


def test_cpu_instructions_0x8B_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x8B)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'e', with_carry_bit=True)


def test_cpu_instructions_0x8C_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x8C)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'h', with_carry_bit=True)


def test_cpu_instructions_0x8D_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x8D)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'l', with_carry_bit=True)


def test_cpu_instructions_0x8F_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x8F)

    cpu_instructions_fixture.add_8_bit_registers.assert_called_once_with('a', 'a', with_carry_bit=True)


def test_cpu_instructions_0x8E_add_8_bit_hl_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_hl_memory_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x8E)

    cpu_instructions_fixture.add_8_bit_hl_memory_to_register.assert_called_once_with('a', with_carry_bit=True)


def test_cpu_instructions_0xCE_add_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.add_8_bit_immediate_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xCE)

    cpu_instructions_fixture.add_8_bit_immediate_to_register.assert_called_once_with('a', with_carry_bit=True)


def test_cpu_instructions_0x90_sub_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x90)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'b')


def test_cpu_instructions_0x91_sub_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x91)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'c')


def test_cpu_instructions_0x92_sub_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x92)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'd')


def test_cpu_instructions_0x93_sub_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x93)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'e')


def test_cpu_instructions_0x94_sub_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x94)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'h')


def test_cpu_instructions_0x95_sub_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x95)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'l')


def test_cpu_instructions_0x97_sub_8_bit(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x97)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'a')


def test_cpu_instructions_0x96_sub_8_bit_hl(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_hl_memory_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x96)

    cpu_instructions_fixture.subtract_8_bit_hl_memory_to_register.assert_called_once_with('a')


def test_cpu_instructions_0xD6_sub_8_bit_immediate(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_immediate_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xD6)

    cpu_instructions_fixture.subtract_8_bit_immediate_to_register.assert_called_once_with('a')


def test_cpu_instructions_0x98_sub_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x98)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'b', with_carry_bit=True)


def test_cpu_instructions_0x99_sub_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x99)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'c', with_carry_bit=True)


def test_cpu_instructions_0x9A_sub_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x9A)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'd', with_carry_bit=True)


def test_cpu_instructions_0x9B_sub_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x9B)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'e', with_carry_bit=True)


def test_cpu_instructions_0x9C_sub_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x9C)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'h', with_carry_bit=True)


def test_cpu_instructions_0x9D_sub_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x9D)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'l', with_carry_bit=True)


def test_cpu_instructions_0x9F_sub_8_bit_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_registers = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x9F)

    cpu_instructions_fixture.subtract_8_bit_registers.assert_called_once_with('a', 'a', with_carry_bit=True)


def test_cpu_instructions_0x9E_sub_8_bit_hl_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_hl_memory_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0x9E)

    cpu_instructions_fixture.subtract_8_bit_hl_memory_to_register.assert_called_once_with('a', with_carry_bit=True)


def test_cpu_instructions_0xDE_sub_8_bit_immediate_carry(cpu_instructions_fixture):
    cpu_instructions_fixture.subtract_8_bit_immediate_to_register = mock.Mock()
    cpu_instructions_fixture.execute_instruction(0xDE)

    cpu_instructions_fixture.subtract_8_bit_immediate_to_register.assert_called_once_with('a', with_carry_bit=True)



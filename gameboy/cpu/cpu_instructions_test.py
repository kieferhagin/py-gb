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

    cpu_instructions_fixture.load_register_with_memory('c', 'bc')

    assert cpu_instructions_fixture._cpu._registers._register_c == 114

    cpu_instructions_fixture._cpu._registers.write_de(0xC000)

    cpu_instructions_fixture.load_register_with_memory('d', 'de')

    assert cpu_instructions_fixture._cpu._registers._register_d == 114


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

    cpu_instructions_fixture.load_memory_with_register('d', 'bc')

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xC000) == 115

    cpu_instructions_fixture._cpu._registers.write_de(0xC000)
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC000, 0)
    cpu_instructions_fixture._cpu._registers._register_b = 116

    cpu_instructions_fixture.load_memory_with_register('b', 'de')

    assert cpu_instructions_fixture._cpu._memory_unit.read_byte(0xC000) == 116


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


def test_cpu_instructions_load_register_with_immediate_memory(cpu_instructions_fixture):
    cpu_instructions_fixture._cpu._memory_unit.write_word(0xC000, 0xC005)
    cpu_instructions_fixture._cpu._registers._program_counter = 0xC000
    cpu_instructions_fixture._cpu._memory_unit.write_byte(0xC005, 123)

    cpu_instructions_fixture.load_register_with_immediate_memory('a')

    assert cpu_instructions_fixture._cpu._registers._register_a == 123
    assert cpu_instructions_fixture._cpu._cycle_clock.get_total_machine_cycles() == 4


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


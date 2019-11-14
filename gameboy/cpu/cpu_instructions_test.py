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

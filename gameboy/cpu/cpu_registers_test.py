import pytest

from gameboy.cpu.cpu_registers import CPURegisters


@pytest.fixture()
def cpu_registers_fixture() -> CPURegisters:
    return CPURegisters()


def test_cpu_registers_init(cpu_registers_fixture):
    assert cpu_registers_fixture._register_a == 0
    assert cpu_registers_fixture._register_b == 0
    assert cpu_registers_fixture._register_c == 0
    assert cpu_registers_fixture._register_d == 0
    assert cpu_registers_fixture._register_e == 0
    assert cpu_registers_fixture._register_h == 0
    assert cpu_registers_fixture._register_l == 0

    assert cpu_registers_fixture._flags == 0

    assert cpu_registers_fixture._program_counter == 0
    assert cpu_registers_fixture._stack_pointer == 0

def test_cpu_registers_reset(cpu_registers_fixture):
    cpu_registers_fixture._register_a = 1
    cpu_registers_fixture._register_b = 1
    cpu_registers_fixture._register_c = 1
    cpu_registers_fixture._register_d = 1
    cpu_registers_fixture._register_e = 1
    cpu_registers_fixture._register_h = 1
    cpu_registers_fixture._register_l = 1

    cpu_registers_fixture._flags = 1

    cpu_registers_fixture._program_counter = 1
    cpu_registers_fixture._stack_pointer = 1

    cpu_registers_fixture.reset()

    assert cpu_registers_fixture._register_a == 0
    assert cpu_registers_fixture._register_b == 0
    assert cpu_registers_fixture._register_c == 0
    assert cpu_registers_fixture._register_d == 0
    assert cpu_registers_fixture._register_e == 0
    assert cpu_registers_fixture._register_h == 0
    assert cpu_registers_fixture._register_l == 0

    assert cpu_registers_fixture._flags == 0

    assert cpu_registers_fixture._program_counter == 0
    assert cpu_registers_fixture._stack_pointer == 0


def test_mask_program_counter(cpu_registers_fixture):
    cpu_registers_fixture._program_counter = 0xFFFF + 1
    cpu_registers_fixture.mask_program_counter()

    assert cpu_registers_fixture._program_counter == 0

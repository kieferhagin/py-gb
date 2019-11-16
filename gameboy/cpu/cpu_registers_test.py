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
    assert cpu_registers_fixture._stack_pointer == 0xFFFE
    assert cpu_registers_fixture._interrupts_enabled is False


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

    cpu_registers_fixture._interrupts_enabled = True

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
    assert cpu_registers_fixture._stack_pointer == 0xFFFE
    assert cpu_registers_fixture._interrupts_enabled is False


def test_mask_program_counter(cpu_registers_fixture):
    cpu_registers_fixture._program_counter = 0xFFFF + 1
    cpu_registers_fixture.mask_program_counter()

    assert cpu_registers_fixture._program_counter == 0


def test_cpu_registers_disable_interrupts(cpu_registers_fixture):
    cpu_registers_fixture._interrupts_enabled = True
    cpu_registers_fixture.disable_interrupts()

    assert not cpu_registers_fixture._interrupts_enabled


def test_cpu_registers_enable_interrupts(cpu_registers_fixture):
    cpu_registers_fixture._interrupts_enabled = False
    cpu_registers_fixture.enable_interrupts()

    assert cpu_registers_fixture._interrupts_enabled


def test_cpu_registers_increment_program_counter(cpu_registers_fixture):
    cpu_registers_fixture.increment_program_counter()

    assert cpu_registers_fixture._program_counter == 1

    cpu_registers_fixture.increment_program_counter(2)

    assert cpu_registers_fixture._program_counter == 3

    cpu_registers_fixture.increment_program_counter(0xFFFF)

    assert cpu_registers_fixture._program_counter == 2


def test_cpu_registers_get_program_counter(cpu_registers_fixture):
    cpu_registers_fixture.increment_program_counter()

    assert cpu_registers_fixture.get_program_counter() == 1


def test_cpu_registers_get_stack_pointer(cpu_registers_fixture):
    cpu_registers_fixture._stack_pointer = 1
    assert cpu_registers_fixture.get_stack_pointer() == 1


def test_cpu_registers_set_stack_pointer(cpu_registers_fixture):
    cpu_registers_fixture._stack_pointer = 1
    cpu_registers_fixture.set_stack_pointer(2)

    assert cpu_registers_fixture.get_stack_pointer() == 2


def test_cpu_registers_read_af(cpu_registers_fixture):
    cpu_registers_fixture._register_a = 1
    cpu_registers_fixture._flags = 244

    assert cpu_registers_fixture.read_af() == 500


def test_cpu_registers_read_bc(cpu_registers_fixture):
    cpu_registers_fixture._register_b = 1
    cpu_registers_fixture._register_c = 244

    assert cpu_registers_fixture.read_bc() == 500


def test_cpu_registers_read_de(cpu_registers_fixture):
    cpu_registers_fixture._register_d = 1
    cpu_registers_fixture._register_e = 244

    assert cpu_registers_fixture.read_de() == 500


def test_cpu_registers_read_hl(cpu_registers_fixture):
    cpu_registers_fixture._register_h = 1
    cpu_registers_fixture._register_l = 244

    assert cpu_registers_fixture.read_hl() == 500


def test_cpu_registers_write_af(cpu_registers_fixture):
    cpu_registers_fixture.write_af(496)

    assert cpu_registers_fixture.read_af() == 496


def test_cpu_registers_write_bc(cpu_registers_fixture):
    cpu_registers_fixture.write_bc(500)

    assert cpu_registers_fixture.read_bc() == 500


def test_cpu_registers_write_de(cpu_registers_fixture):
    cpu_registers_fixture.write_de(500)

    assert cpu_registers_fixture.read_de() == 500


def test_cpu_registers_write_hl(cpu_registers_fixture):
    cpu_registers_fixture.write_hl(500)

    assert cpu_registers_fixture.read_hl() == 500


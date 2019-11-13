from unittest import mock

import pytest

from gameboy.cpu.cpu import CPU


@pytest.fixture()
def cpu_fixture() -> CPU:
    return CPU()


def test_cpu_init(cpu_fixture):
    assert cpu_fixture._registers is not None
    assert cpu_fixture._cycle_clock is not None


def test_cpu_reset(cpu_fixture):
    cpu_fixture._registers = mock.Mock()
    cpu_fixture._cycle_clock = mock.Mock()

    cpu_fixture.reset()

    cpu_fixture._registers.reset.assert_called_once()
    cpu_fixture._cycle_clock.reset.assert_called_once()


# def test_cpu_step_masks_program_counter(cpu_fixture):
#     cpu_fixture._registers._program_counter = 0xFFFF
#     cpu_fixture.step()
#
#     assert cpu_fixture._registers._program_counter == 0x0000

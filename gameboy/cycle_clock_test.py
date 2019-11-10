import pytest

from gameboy.cycle_clock import CycleClock


@pytest.fixture()
def cycle_clock_fixture():
    return CycleClock()


def test_cycle_clock_init(cycle_clock_fixture):
    assert cycle_clock_fixture._total_clock_cycles == 0
    assert cycle_clock_fixture._last_machine_cycle_count == 0


def test_cycle_clock_reset(cycle_clock_fixture):
    cycle_clock_fixture._total_clock_cycles = 10
    cycle_clock_fixture._last_machine_cycle_count = 10

    cycle_clock_fixture.reset()

    assert cycle_clock_fixture._total_clock_cycles == 0
    assert cycle_clock_fixture._last_machine_cycle_count == 0


def test_tick(cycle_clock_fixture):
    cycle_clock_fixture.tick()

    assert cycle_clock_fixture._total_clock_cycles == 4
    assert cycle_clock_fixture._last_machine_cycle_count == 1

    cycle_clock_fixture.tick(2)

    assert cycle_clock_fixture._total_clock_cycles == 12
    assert cycle_clock_fixture._last_machine_cycle_count == 2


def test_get_total_machine_cycles(cycle_clock_fixture):
    cycle_clock_fixture._total_clock_cycles = 12

    assert cycle_clock_fixture.get_total_machine_cycles() == 3


def test_get_total_clock_cycles(cycle_clock_fixture):
    cycle_clock_fixture._total_clock_cycles = 12

    assert cycle_clock_fixture.get_total_clock_cycles() == 12


def test_get_last_machine_cycle_count(cycle_clock_fixture):
    cycle_clock_fixture.tick()

    assert cycle_clock_fixture.get_last_machine_cycle_count() == 1

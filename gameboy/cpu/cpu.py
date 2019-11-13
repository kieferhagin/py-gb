from gameboy.cpu.cpu_registers import CPURegisters
from gameboy.cycle_clock import CycleClock


class CPU:
    def __init__(self):
        self._registers = CPURegisters()
        self._cycle_clock = CycleClock()

    def reset(self):
        self._registers.reset()
        self._cycle_clock.reset()

    def step(self):
        pass

    def _handle_interrupts(self) -> None:
        if not self._registers.get_interrupts_enabled():
            return

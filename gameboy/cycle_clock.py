class CycleClock:
    def __init__(self):
        self._total_clock_cycles = 0
        self._last_machine_cycle_count = 0

    def tick(self, machine_cycles: int=1) -> int:
        self._total_clock_cycles += machine_cycles * 4
        self._last_machine_cycle_count = machine_cycles

        return self._total_clock_cycles

    def get_total_machine_cycles(self) -> int:
        return int(self.get_total_clock_cycles() / 4)

    def get_total_clock_cycles(self) -> int:
        return self._total_clock_cycles

    def get_last_machine_cycle_count(self) -> int:
        return self._last_machine_cycle_count

    def reset(self) -> None:
        self.__init__()

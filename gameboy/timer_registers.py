from gameboy.cycle_clock import CycleClock
from gameboy.memory_region import MemoryRegion


class TimerRegisters(MemoryRegion):
    DIVIDER_ADDRESS = 0xFF04
    TIMER_CONTROL = 0xFF07

    def __init__(self):
        super().__init__(bytearray(4), 0xFF04)

        self._divider_cycle_clock = CycleClock()
        self._timer_cycle_clock = CycleClock()

    def reset(self) -> None:
        self._divider_cycle_clock.reset()
        self._timer_cycle_clock.reset()

    def tick(self, machine_cycles: int=1) -> int:
        self._divider_cycle_clock.tick(machine_cycles)

        if self.get_divider_timer_value() >= 255:
            self._divider_cycle_clock.reset()

        return self._divider_cycle_clock.get_total_machine_cycles()

    def write_byte(self, address: int, value: int) -> None:
        # Writing to the divider register clears both clocks
        # This is because the Game Boy uses the same 16 bit register for both values
        if address == self.DIVIDER_ADDRESS:
            self._divider_cycle_clock.reset()
            self._timer_cycle_clock.reset()

            return

        # QUIRK
        # If we've changed the timer control speed or disabled it, we might be changing
        # the input to the falling edge detector used to increment timer.
        # If this happens we get an extra timer tick.
        if address == self.TIMER_CONTROL:
            self.update_timer_control(value)

            return

        super().write_byte(address, value)

    def update_timer_control(self, value: int) -> None:
        old_bit = self.get_timer_clock_enabled() and self.get_timer_falling_edge_bit()

        super().write_byte(self.TIMER_CONTROL, value)

        new_bit = self.get_timer_clock_enabled() and self.get_timer_falling_edge_bit()

        if old_bit and not new_bit:
            self._timer_cycle_clock.tick()

    def read_byte(self, address: int) -> int:
        # Divider increments once every 64 machine cycles, so we'll fake that here
        if address == self.DIVIDER_ADDRESS:
            return self.get_divider_timer_value()

        return super().read_byte(address)

    def get_divider_timer_value(self) -> int:
        return int(self._divider_cycle_clock.get_total_machine_cycles() / 64)

    def get_timer_clock_enabled(self) -> bool:
        return (self.get_timer_control_value() & 0x04) > 0

    def get_timer_falling_edge_bit(self) -> int:
        control_value = self.get_timer_control_value()

        timer_clock_setting = control_value & 0x03

        if timer_clock_setting == 0:  # 4.096 KHz (1024 cycles)
            return self._divider_cycle_clock.get_total_clock_cycles() & 512

        if timer_clock_setting == 1:  # 262.144 KHz (16 cycles)
            return self._divider_cycle_clock.get_total_clock_cycles() & 8

        if timer_clock_setting == 2:  # 65.536 KHz (64 cycles)
            return self._divider_cycle_clock.get_total_clock_cycles() & 32

        if timer_clock_setting == 3:  # 16.384 KHz (256 cycles)
            return self._divider_cycle_clock.get_total_clock_cycles() & 128

        raise Exception('Invalid timer speed setting: {}'.format(timer_clock_setting))

    def get_timer_control_value(self) -> int:
        return self.read_byte(self.TIMER_CONTROL)

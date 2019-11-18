from gameboy.cpu.cpu_registers import CPURegisters
from gameboy.cycle_clock import CycleClock
from gameboy.memory.memory_unit import MemoryUnit


class CPU:
    def __init__(self, memory_unit: MemoryUnit):
        self._memory_unit = memory_unit

        self._registers = CPURegisters()
        self._cycle_clock = CycleClock()
        self._cpu_instructions = CPUInstructions(self)

        self._is_halted = False
        self._interrupt_enable_pending = False

    def reset(self):
        self._registers.reset()
        self._cycle_clock.reset()

        self._is_halted = False

    def step(self):
        if self._is_halted:
            self._cycle_clock.tick()

            return

        if self._interrupt_enable_pending:
            self._registers.enable_interrupts()
            self._interrupt_enable_pending = False

        op_code = self.read_immediate_byte()

        # TODO: halt bug

        self._execute_operation(op_code)

    def _execute_operation(self, op_code: int):
        pass

    def get_registers(self):
        return self._registers

    def get_cycle_clock(self):
        return self._cycle_clock

    def _handle_interrupts(self) -> None:
        raised_enabled_interrupt_bits = self._get_raised_enabled_interrupt_bits()

        if not raised_enabled_interrupt_bits:
            return

        # When any enabled interrupt is raised it will bring the CPU out of halt mode to service it, if required.
        self.clear_halted()

        if not self._registers.get_interrupts_enabled():
            return

        for i in range(0, 5):
            processed_interrupt = self._handle_interrupt(i)

            # We only service one interrupt at a time
            if processed_interrupt:
                return

    def _handle_interrupt(self, interrupt_bit_index: int) -> bool:
        interrupt_bit = 1 << interrupt_bit_index

        raised_enabled_interrupt_bits = self._get_raised_enabled_interrupt_bits()

        if raised_enabled_interrupt_bits & interrupt_bit:
            # Disable interrupts before we "Call" into the handler. It is up to handler code to re-enable with reti
            self._registers.disable_interrupts()

            # Call to the interrupt handler
            self._cpu_instructions.call(0x40 + (interrupt_bit_index * 8))

            # TODO: execute "Call" Call(gb, 0x40 + (i * 8));
            self._memory_unit \
                .get_interrupt_flag_register() \
                .clear_interrupt_by_bit(interrupt_bit)

            return True

        return False

    def _get_raised_enabled_interrupt_bits(self) -> int:
        interrupt_flag_bits = self._memory_unit \
            .get_interrupt_flag_register() \
            .get_interrupt_bits()

        interrupt_enable_bits = self._memory_unit \
            .get_interrupt_enable_register() \
            .get_interrupt_enabled_bits()

        return interrupt_enable_bits & interrupt_flag_bits

    def clear_halted(self):
        self._is_halted = False

    def set_halted(self):
        self._is_halted = True

    def read_immediate_word(self) -> int:
        low_byte = self.read_immediate_byte()
        high_byte = self.read_immediate_byte()

        return (high_byte << 8) | low_byte

    def read_immediate_signed_byte(self) -> int:
        unsigned_byte = self.read_immediate_byte()

        return unsigned_byte if unsigned_byte <= 127 else unsigned_byte - 256

    def read_immediate_byte(self) -> int:
        self._registers.increment_program_counter()
        return self._memory_unit.read_byte(self._registers.get_program_counter() - 1)

    def push_word_to_stack(self, value):
        stack_pointer = self._registers.get_stack_pointer()
        new_stack_pointer = stack_pointer - 2

        self._memory_unit.write_word(new_stack_pointer, value)
        self._registers.set_stack_pointer(new_stack_pointer)

    def pop_word_from_stack(self) -> int:
        old_stack_pointer = self._registers.get_stack_pointer()
        new_stack_pointer = old_stack_pointer + 2

        self._registers.set_stack_pointer(new_stack_pointer)

        return self._memory_unit.read_word(old_stack_pointer)

# Down here to avoid circular dependency...you'd think we'd have figured that one out by now.
from gameboy.cpu.cpu_instructions import CPUInstructions

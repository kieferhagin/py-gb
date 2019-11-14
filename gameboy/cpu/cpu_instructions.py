from gameboy.cpu.cpu import CPU


class CPUInstructions:
    def __init__(self, cpu: CPU):
        self._cpu = cpu

    def call(self, address: int):
        self._cpu.push_word_to_stack(self._cpu.get_registers().get_program_counter())
        self._cpu.get_registers().set_program_counter(address)

        self._cpu.get_cycle_clock().tick(5)

from gameboy.cpu.cpu_registers import CPURegisters


class CPU:
    def __init__(self):
        self._registers = CPURegisters()

    def reset(self):
        self._registers.reset()

    def step(self):
        self._registers.mask_program_counter()

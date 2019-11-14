class CPURegisters:

    def __init__(self):
        self._register_a = 0
        self._register_b = 0
        self._register_c = 0
        self._register_d = 0
        self._register_e = 0
        self._register_h = 0
        self._register_l = 0

        self._flags = 0

        self._program_counter = 0
        self._stack_pointer = 0xFFFE  # top of HRAM

        self._interrupts_enabled = False

    def reset(self) -> None:
        self.__init__()

    def mask_program_counter(self) -> None:
        self._program_counter &= 0xFFFF

    def get_interrupts_enabled(self) -> bool:
        return self._interrupts_enabled

    def disable_interrupts(self):
        self._interrupts_enabled = False

    def enable_interrupts(self):
        self._interrupts_enabled = True

    def increment_program_counter(self, count: int=1) -> int:
        return self.set_program_counter(self._program_counter + count)

    def set_program_counter(self, value: int) -> int:
        self._program_counter = value
        self.mask_program_counter()

        return self._program_counter

    def get_program_counter(self) -> int:
        return self._program_counter

    def get_stack_pointer(self) -> int:
        return self._stack_pointer

    def set_stack_pointer(self, value):
        self._stack_pointer = value & 0xFFFF

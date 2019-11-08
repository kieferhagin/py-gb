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
        self._stack_pointer = 0

    def reset(self) -> None:
        self.__init__()

    def mask_program_counter(self) -> None:
        self._program_counter &= 0xFFFF

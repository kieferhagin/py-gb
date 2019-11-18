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

    def read_af(self) -> int:
        return (self._register_a << 8) | self._flags

    def read_bc(self) -> int:
        return (self._register_b << 8) | self._register_c

    def read_de(self) -> int:
        return (self._register_d << 8) | self._register_e

    def read_hl(self) -> int:
        return (self._register_h << 8) | self._register_l

    def write_af(self, value: int):
        self._register_a = value >> 8
        self._flags = value & 0xF0

    def write_bc(self, value: int):
        self._register_b = value >> 8
        self._register_c = value & 0xFF

    def write_de(self, value: int):
        self._register_d = value >> 8
        self._register_e = value & 0xFF

    def write_hl(self, value: int):
        self._register_h = value >> 8
        self._register_l = value & 0xFF

    def update_flags(self, zero: bool, subtract: bool, half_carry: bool, carry: bool):
        self.update_flag_zero(zero)
        self.update_flag_subtract(subtract)
        self.update_flag_half_carry(half_carry)
        self.update_flag_carry(carry)

    def update_flag_zero(self, value: bool):
        if value:
            self._flags |= 0x80
        else:
            self._flags &= ~0x80

    def update_flag_subtract(self, value: bool):
        if value:
            self._flags |= 0x40
        else:
            self._flags &= ~0x40

    def update_flag_half_carry(self, value: bool):
        if value:
            self._flags |= 0x20
        else:
            self._flags &= ~0x20

    def update_flag_carry(self, value: bool):
        if value:
            self._flags |= 0x10
        else:
            self._flags &= ~0x10

    def read_flag_zero(self) -> int:
        return self._flags & 0x80

    def read_flag_subtract(self) -> int:
        return self._flags & 0x40

    def read_flag_half_carry(self) -> int:
        return self._flags & 0x20

    def read_flag_carry(self) -> int:
        return self._flags & 0x10

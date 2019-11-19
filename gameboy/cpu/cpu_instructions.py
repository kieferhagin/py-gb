from gameboy.cpu.cpu import CPU


class CPUInstructions:
    def __init__(self, cpu: CPU):
        self._cpu = cpu

    def execute_instruction(self, op_code: int):
        # ~`~ Register-to-register loads ~`~
        if op_code == 0x40:
            return self.load('b', 'b')
        if op_code == 0x41:
            return self.load('b', 'c')
        if op_code == 0x42:
            return self.load('b', 'd')
        if op_code == 0x43:
            return self.load('b', 'e')
        if op_code == 0x44:
            return self.load('b', 'h')
        if op_code == 0x45:
            return self.load('b', 'l')
        if op_code == 0x47:
            return self.load('b', 'a')
        if op_code == 0x48:
            return self.load('c', 'b')
        if op_code == 0x49:
            return self.load('c', 'c')
        if op_code == 0x4A:
            return self.load('c', 'd')
        if op_code == 0x4B:
            return self.load('c', 'e')
        if op_code == 0x4C:
            return self.load('c', 'h')
        if op_code == 0x4D:
            return self.load('c', 'l')
        if op_code == 0x4F:
            return self.load('c', 'a')
        if op_code == 0x50:
            return self.load('d', 'b')
        if op_code == 0x51:
            return self.load('d', 'c')
        if op_code == 0x52:
            return self.load('d', 'd')
        if op_code == 0x53:
            return self.load('d', 'e')
        if op_code == 0x54:
            return self.load('d', 'h')
        if op_code == 0x55:
            return self.load('d', 'l')
        if op_code == 0x57:
            return self.load('d', 'a')
        if op_code == 0x58:
            return self.load('e', 'b')
        if op_code == 0x59:
            return self.load('e', 'c')
        if op_code == 0x5A:
            return self.load('e', 'd')
        if op_code == 0x5B:
            return self.load('e', 'e')
        if op_code == 0x5C:
            return self.load('e', 'h')
        if op_code == 0x5D:
            return self.load('e', 'l')
        if op_code == 0x5F:
            return self.load('e', 'a')
        if op_code == 0x60:
            return self.load('h', 'b')
        if op_code == 0x61:
            return self.load('h', 'c')
        if op_code == 0x62:
            return self.load('h', 'd')
        if op_code == 0x63:
            return self.load('h', 'e')
        if op_code == 0x64:
            return self.load('h', 'h')
        if op_code == 0x65:
            return self.load('h', 'l')
        if op_code == 0x67:
            return self.load('h', 'a')
        if op_code == 0x68:
            return self.load('l', 'b')
        if op_code == 0x69:
            return self.load('l', 'c')
        if op_code == 0x6A:
            return self.load('l', 'd')
        if op_code == 0x6B:
            return self.load('l', 'e')
        if op_code == 0x6C:
            return self.load('l', 'h')
        if op_code == 0x6D:
            return self.load('l', 'l')
        if op_code == 0x6F:
            return self.load('l', 'a')
        if op_code == 0x78:
            return self.load('a', 'b')
        if op_code == 0x79:
            return self.load('a', 'c')
        if op_code == 0x7A:
            return self.load('a', 'd')
        if op_code == 0x7B:
            return self.load('a', 'e')
        if op_code == 0x7C:
            return self.load('a', 'h')
        if op_code == 0x7D:
            return self.load('a', 'l')
        if op_code == 0x7F:
            return self.load('a', 'a')

        # ~`~ Memory-to-register loads ~`~
        if op_code == 0x46:
            return self.load_register_with_memory('b')
        if op_code == 0x4E:
            return self.load_register_with_memory('c')
        if op_code == 0x56:
            return self.load_register_with_memory('d')
        if op_code == 0x5E:
            return self.load_register_with_memory('e')
        if op_code == 0x66:
            return self.load_register_with_memory('h')
        if op_code == 0x6E:
            return self.load_register_with_memory('l')
        if op_code == 0x7E:
            return self.load_register_with_memory('a')

        # ~`~ Register-to-memory loads ~`~
        if op_code == 0x70:
            return self.load_memory_with_register('b')
        if op_code == 0x71:
            return self.load_memory_with_register('c')
        if op_code == 0x72:
            return self.load_memory_with_register('d')
        if op_code == 0x73:
            return self.load_memory_with_register('e')
        if op_code == 0x74:
            return self.load_memory_with_register('h')
        if op_code == 0x75:
            return self.load_memory_with_register('l')
        if op_code == 0x77:
            return self.load_memory_with_register('a')

        # ~`~ Immediate to HL address ~`~
        if op_code == 0x36:
            return self.load_memory_with_immediate()

        # ~`~ Special, "a" register only loads ~`~
        if op_code == 0x0A:
            return self.load_register_with_memory('a', memory_register_16='bc')
        if op_code == 0x1A:
            return self.load_register_with_memory('a', memory_register_16='de')
        if op_code == 0x02:
            return self.load_memory_with_register('a', memory_register_16='bc')
        if op_code == 0x12:
            return self.load_memory_with_register('a', memory_register_16='de')
        if op_code == 0xEA:
            return self.load_immediate_memory_with_register('a')
        if op_code == 0xFA:
            return self.load_register_with_immediate_memory('a')

        raise NotImplementedError(f'Opcode {op_code} not implemented.')

    # Move program counter to a address in memory unconditionally
    def call(self, address: int):
        self._cpu.push_word_to_stack(self._cpu.get_registers().get_program_counter())
        self._cpu.get_registers().set_program_counter(address)

        self._cpu.get_cycle_clock().tick(5)

    # ld $reg8, $reg8: Load 8 bit register with value of another
    def load(self, from_register: str, to_register: str):
        from_register_name = self._get_8_bit_register_name_from_key(from_register)
        to_register_name = self._get_8_bit_register_name_from_key(to_register)

        self._set_8_bit_register_value(to_register_name, getattr(self._cpu.get_registers(), from_register_name))

        self._cpu.get_cycle_clock().tick(1)

    # ld $reg8, ($reg16): Load 8 bit register with value of memory location at 16 bit register
    def load_register_with_memory(self, to_register: str, memory_register_16: str='hl'):
        to_register_name = self._get_8_bit_register_name_from_key(to_register)
        memory_location = self._get_16_bit_register_value(memory_register_16)
        memory_location_value = self._cpu.get_memory_unit().read_byte(memory_location)

        self._set_8_bit_register_value(to_register_name, memory_location_value)

        self._cpu.get_cycle_clock().tick(2)

    # ld ($reg16), $reg8: Load memory location at 16 bit register with value of 8 bit register
    def load_memory_with_register(self, from_register: str, memory_register_16: str='hl'):
        from_register_name = self._get_8_bit_register_name_from_key(from_register)
        memory_location = self._get_16_bit_register_value(memory_register_16)
        register_value = self._get_8_bit_register_value(from_register_name)

        self._cpu.get_memory_unit().write_byte(memory_location, register_value)

        self._cpu.get_cycle_clock().tick(2)

    # ld ($hl), imm8: Load memory location at HL with immediate byte
    def load_memory_with_immediate(self):
        memory_location = self._cpu.get_registers().read_hl()
        immediate_byte = self._cpu.read_immediate_byte()

        self._cpu.get_memory_unit().write_byte(memory_location, immediate_byte)

        self._cpu.get_cycle_clock().tick(3)

    # ld (imm16), $reg8: Load immediate memory address with 8 bit register
    def load_immediate_memory_with_register(self, from_register: str):
        immediate_memory_location = self._cpu.read_immediate_word()
        from_register_name = self._get_8_bit_register_name_from_key(from_register)
        register_value = self._get_8_bit_register_value(from_register_name)

        self._cpu.get_memory_unit().write_byte(immediate_memory_location, register_value)

        self._cpu.get_cycle_clock().tick(4)

    # ld $reg8, (imm16): Load 8 bit register with immediate memory value
    def load_register_with_immediate_memory(self, to_register: str):
        immediate_memory_location = self._cpu.read_immediate_word()
        to_register_name = self._get_8_bit_register_name_from_key(to_register)
        immediate_memory_location_value = self._cpu.get_memory_unit().read_byte(immediate_memory_location)

        self._set_8_bit_register_value(to_register_name, immediate_memory_location_value)

        self._cpu.get_cycle_clock().tick(4)

    def _get_8_bit_register_name_from_key(self, register_key: str) -> str:
        register_name = f'_register_{register_key}'

        if not hasattr(self._cpu.get_registers(), register_name):
            raise AttributeError(f'Invalid register {register_name}')

        return register_name

    def _set_8_bit_register_value(self, register_name: str, value: int):
        setattr(self._cpu.get_registers(), register_name, value)

    def _get_8_bit_register_value(self, register_name: str) -> int:
        return getattr(self._cpu.get_registers(), register_name)

    def _get_16_bit_register_value(self, register_name: str) -> int:
        register_getter_name = f'read_{register_name}'

        if not hasattr(self._cpu.get_registers(), register_getter_name):
            raise AttributeError(f'Invalid register {register_name}')

        return getattr(self._cpu.get_registers(), register_getter_name)()

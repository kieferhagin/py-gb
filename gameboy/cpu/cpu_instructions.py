from gameboy.cpu.cpu import CPU


class CPUInstructions:
    def __init__(self, cpu: CPU):
        self._cpu = cpu

    def execute_instruction(self, op_code: int):
        # ~`~ No-op ~`~
        if op_code == 0x00:
            return self.no_op()

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
        if op_code == 0x22:
            return self.load_memory_with_register('a', increment_memory_register=True)
        if op_code == 0x2A:
            return self.load_register_with_memory('a', increment_memory_register=True)
        if op_code == 0x32:
            return self.load_memory_with_register('a', decrement_memory_register=True)
        if op_code == 0x3A:
            return self.load_register_with_memory('a', decrement_memory_register=True)
        if op_code == 0xE0:
            return self.load_immediate_memory_with_register('a', high_memory_load=True)
        if op_code == 0xE2:
            return self.load_offset_memory_at_register_with_register('c', 'a')
        if op_code == 0xF0:
            return self.load_register_with_immediate_memory('a', high_memory_read=True)
        if op_code == 0xF2:
            return self.load_register_with_offset_memory_at_register('a', 'c')

        # ~`~ Immediate-to-register loads ~`~
        if op_code == 0x06:
            return self.load_register_with_immediate_byte('b')
        if op_code == 0x0E:
            return self.load_register_with_immediate_byte('c')
        if op_code == 0x16:
            return self.load_register_with_immediate_byte('d')
        if op_code == 0x1E:
            return self.load_register_with_immediate_byte('e')
        if op_code == 0x26:
            return self.load_register_with_immediate_byte('h')
        if op_code == 0x2E:
            return self.load_register_with_immediate_byte('l')
        if op_code == 0x3E:
            return self.load_register_with_immediate_byte('a')
        if op_code == 0x01:
            return self.load_register_with_immediate_word('bc')
        if op_code == 0x11:
            return self.load_register_with_immediate_word('de')
        if op_code == 0x21:
            return self.load_register_with_immediate_word('hl')
        if op_code == 0x31:
            return self.load_register_with_immediate_word('sp')

        # ~`~ Stack pointer ~`~
        if op_code == 0x08:
            return self.load_immediate_memory_with_16_bit_register('sp')
        if op_code == 0xF9:
            return self.load_16_bit('hl', 'sp')
        if op_code == 0xF8:
            return self.load_16_bit('sp', 'hl', immediate_signed_offset=True)

        # ~`~ Pop & push to stack ~`~
        if op_code == 0xC1:
            return self.pop_stack_to_register('bc')
        if op_code == 0xD1:
            return self.pop_stack_to_register('de')
        if op_code == 0xE1:
            return self.pop_stack_to_register('hl')
        if op_code == 0xF1:
            return self.pop_stack_to_register('af')
        if op_code == 0xC5:
            return self.push_register_to_stack('bc')
        if op_code == 0xD5:
            return self.push_register_to_stack('de')
        if op_code == 0xE5:
            return self.push_register_to_stack('hl')
        if op_code == 0xF5:
            return self.push_register_to_stack('af')

        # ~`~ Add ~`~
        if op_code == 0x80:
            return self.add_8_bit_registers('a', 'b')
        if op_code == 0x81:
            return self.add_8_bit_registers('a', 'c')
        if op_code == 0x82:
            return self.add_8_bit_registers('a', 'd')
        if op_code == 0x83:
            return self.add_8_bit_registers('a', 'e')
        if op_code == 0x84:
            return self.add_8_bit_registers('a', 'h')
        if op_code == 0x85:
            return self.add_8_bit_registers('a', 'l')
        if op_code == 0x87:
            return self.add_8_bit_registers('a', 'a')
        if op_code == 0x86:
            return self.add_8_bit_hl_memory_to_register('a')
        if op_code == 0xC6:
            return self.add_8_bit_immediate_to_register('a')

        # ~`~ Add with carry ~`~
        if op_code == 0x88:
            return self.add_8_bit_registers('a', 'b', with_carry_bit=True)
        if op_code == 0x89:
            return self.add_8_bit_registers('a', 'c', with_carry_bit=True)
        if op_code == 0x8A:
            return self.add_8_bit_registers('a', 'd', with_carry_bit=True)
        if op_code == 0x8B:
            return self.add_8_bit_registers('a', 'e', with_carry_bit=True)
        if op_code == 0x8C:
            return self.add_8_bit_registers('a', 'h', with_carry_bit=True)
        if op_code == 0x8D:
            return self.add_8_bit_registers('a', 'l', with_carry_bit=True)
        if op_code == 0x8F:
            return self.add_8_bit_registers('a', 'a', with_carry_bit=True)
        if op_code == 0x8E:
            return self.add_8_bit_hl_memory_to_register('a', with_carry_bit=True)
        if op_code == 0xCE:
            return self.add_8_bit_immediate_to_register('a', with_carry_bit=True)

        # ~`~ Subtract ~`~
        if op_code == 0x90:
            return self.subtract_8_bit_registers('a', 'b')
        if op_code == 0x91:
            return self.subtract_8_bit_registers('a', 'c')
        if op_code == 0x92:
            return self.subtract_8_bit_registers('a', 'd')
        if op_code == 0x93:
            return self.subtract_8_bit_registers('a', 'e')
        if op_code == 0x94:
            return self.subtract_8_bit_registers('a', 'h')
        if op_code == 0x95:
            return self.subtract_8_bit_registers('a', 'l')
        if op_code == 0x97:
            return self.subtract_8_bit_registers('a', 'a')
        if op_code == 0x96:
            return self.subtract_8_bit_hl_memory_to_register('a')
        if op_code == 0xD6:
            return self.subtract_8_bit_immediate_to_register('a')

        # ~`~ Subtract with carry ~`~
        if op_code == 0x98:
            return self.subtract_8_bit_registers('a', 'b', with_carry_bit=True)
        if op_code == 0x99:
            return self.subtract_8_bit_registers('a', 'c', with_carry_bit=True)
        if op_code == 0x9A:
            return self.subtract_8_bit_registers('a', 'd', with_carry_bit=True)
        if op_code == 0x9B:
            return self.subtract_8_bit_registers('a', 'e', with_carry_bit=True)
        if op_code == 0x9C:
            return self.subtract_8_bit_registers('a', 'h', with_carry_bit=True)
        if op_code == 0x9D:
            return self.subtract_8_bit_registers('a', 'l', with_carry_bit=True)
        if op_code == 0x9F:
            return self.subtract_8_bit_registers('a', 'a', with_carry_bit=True)
        if op_code == 0x9E:
            return self.subtract_8_bit_hl_memory_to_register('a', with_carry_bit=True)
        if op_code == 0xDE:
            return self.subtract_8_bit_immediate_to_register('a', with_carry_bit=True)

        # ~`~ Increment ~`~
        if op_code == 0x04:
            return self.increment_8_bit_register('b')
        if op_code == 0x0C:
            return self.increment_8_bit_register('c')
        if op_code == 0x14:
            return self.increment_8_bit_register('d')
        if op_code == 0x1C:
            return self.increment_8_bit_register('e')
        if op_code == 0x24:
            return self.increment_8_bit_register('h')
        if op_code == 0x2C:
            return self.increment_8_bit_register('l')
        if op_code == 0x3C:
            return self.increment_8_bit_register('a')

        # ~`~ Decrement ~`~
        if op_code == 0x05:
            return self.decrement_8_bit_register('b')
        if op_code == 0x0D:
            return self.decrement_8_bit_register('c')
        if op_code == 0x15:
            return self.decrement_8_bit_register('d')
        if op_code == 0x1D:
            return self.decrement_8_bit_register('e')
        if op_code == 0x25:
            return self.decrement_8_bit_register('h')
        if op_code == 0x2D:
            return self.decrement_8_bit_register('l')
        if op_code == 0x3D:
            return self.decrement_8_bit_register('a')

        # ~`~ Compare ~`~
        if op_code == 0xB8:
            return self.subtract_8_bit_registers('a', 'b', compare_only=True)
        if op_code == 0xB9:
            return self.subtract_8_bit_registers('a', 'c', compare_only=True)
        if op_code == 0xBA:
            return self.subtract_8_bit_registers('a', 'd', compare_only=True)
        if op_code == 0xBB:
            return self.subtract_8_bit_registers('a', 'e', compare_only=True)
        if op_code == 0xBC:
            return self.subtract_8_bit_registers('a', 'h', compare_only=True)
        if op_code == 0xBD:
            return self.subtract_8_bit_registers('a', 'l', compare_only=True)
        if op_code == 0xBF:
            return self.subtract_8_bit_registers('a', 'a', compare_only=True)
        if op_code == 0xBE:
            return self.subtract_8_bit_hl_memory_to_register('a', compare_only=True)
        if op_code == 0xFE:
            return self.subtract_8_bit_immediate_to_register('a', compare_only=True)

        # ~`~ Bitwise ~`~
        if op_code == 0xA0:
            return self.bitwise_and_8_bit_register('a', 'b')
        if op_code == 0xA1:
            return self.bitwise_and_8_bit_register('a', 'c')
        if op_code == 0xA2:
            return self.bitwise_and_8_bit_register('a', 'd')
        if op_code == 0xA3:
            return self.bitwise_and_8_bit_register('a', 'e')
        if op_code == 0xA4:
            return self.bitwise_and_8_bit_register('a', 'h')
        if op_code == 0xA5:
            return self.bitwise_and_8_bit_register('a', 'l')
        if op_code == 0xA7:
            return self.bitwise_and_8_bit_register('a', 'a')
        if op_code == 0xB0:
            return self.bitwise_or_8_bit_register('a', 'b')
        if op_code == 0xB1:
            return self.bitwise_or_8_bit_register('a', 'c')
        if op_code == 0xB2:
            return self.bitwise_or_8_bit_register('a', 'd')
        if op_code == 0xB3:
            return self.bitwise_or_8_bit_register('a', 'e')
        if op_code == 0xB4:
            return self.bitwise_or_8_bit_register('a', 'h')
        if op_code == 0xB5:
            return self.bitwise_or_8_bit_register('a', 'l')
        if op_code == 0xB7:
            return self.bitwise_or_8_bit_register('a', 'a')
        if op_code == 0xA8:
            return self.bitwise_xor_8_bit_register('a', 'b')
        if op_code == 0xA9:
            return self.bitwise_xor_8_bit_register('a', 'c')
        if op_code == 0xAA:
            return self.bitwise_xor_8_bit_register('a', 'd')
        if op_code == 0xAB:
            return self.bitwise_xor_8_bit_register('a', 'e')
        if op_code == 0xAC:
            return self.bitwise_xor_8_bit_register('a', 'h')
        if op_code == 0xAD:
            return self.bitwise_xor_8_bit_register('a', 'l')
        if op_code == 0xAF:
            return self.bitwise_xor_8_bit_register('a', 'a')
        if op_code == 0xA6:
            return self.bitwise_and_8_bit_register_with_memory('a', 'hl')
        if op_code == 0xB6:
            return self.bitwise_or_8_bit_register_with_memory('a', 'hl')
        if op_code == 0xAE:
            return self.bitwise_xor_8_bit_register_with_memory('a', 'hl')
        if op_code == 0xE6:
            return self.bitwise_and_8_bit_register_with_immediate_byte('a')
        if op_code == 0xF6:
            return self.bitwise_or_8_bit_register_with_immediate_byte('a')
        if op_code == 0xEE:
            return self.bitwise_xor_8_bit_register_with_immediate_byte('a')
        if op_code == 0x07:
            return self.rotate_8_bit_register_left('a')
        if op_code == 0x0F:
            return self.rotate_8_bit_register_right('a')
        if op_code == 0x17:
            return self.rotate_8_bit_register_left('a', with_carry_bit=True)
        if op_code == 0x1F:
            return self.rotate_8_bit_register_right('a', with_carry_bit=True)
        if op_code == 0x2F:
            return self.complement_8_bit_register('a')

        # ~`~ Extended operations ~`~
        if op_code == 0xCB:
            return self.execute_extended_operation()

        # ~`~ 16 bit math ~`~
        if op_code == 0x09:
            return self.add_16_bit_registers('hl', 'bc')
        if op_code == 0x19:
            return self.add_16_bit_registers('hl', 'de')
        if op_code == 0x29:
            return self.add_16_bit_registers('hl', 'hl')
        if op_code == 0x39:
            return self.add_16_bit_registers('hl', 'sp')
        if op_code == 0xE8:
            return self.add_signed_immediate_to_16_bit_register('sp')
        if op_code == 0x03:
            return self.increment_16_bit_register('bc')
        if op_code == 0x13:
            return self.increment_16_bit_register('de')
        if op_code == 0x23:
            return self.increment_16_bit_register('hl')
        if op_code == 0x33:
            return self.increment_16_bit_register('sp')
        if op_code == 0x0B:
            return self.decrement_16_bit_register('bc')
        if op_code == 0x1B:
            return self.decrement_16_bit_register('de')
        if op_code == 0x2B:
            return self.decrement_16_bit_register('hl')
        if op_code == 0x3B:
            return self.decrement_16_bit_register('sp')
        if op_code == 0x34:
            return self.increment_memory_at_register('hl')
        if op_code == 0x35:
            return self.decrement_memory_at_register('hl')

        # ~`~ Jump ~`~
        if op_code == 0xE9:
            return self.jump_to_16_bit_register('hl')
        if op_code == 0xC3:
            return self.jump_to_immediate()
        if op_code == 0xC2:
            return self.jump_to_immediate(conditional_zero_flag=False)
        if op_code == 0xCA:
            return self.jump_to_immediate(conditional_zero_flag=True)
        if op_code == 0xD2:
            return self.jump_to_immediate(conditional_carry_flag=False)
        if op_code == 0xDA:
            return self.jump_to_immediate(conditional_carry_flag=True)
        if op_code == 0x18:
            return self.jump_to_immediate(relative=True)
        if op_code == 0x20:
            return self.jump_to_immediate(relative=True, conditional_zero_flag=False)
        if op_code == 0x28:
            return self.jump_to_immediate(relative=True, conditional_zero_flag=True)
        if op_code == 0x30:
            return self.jump_to_immediate(relative=True, conditional_carry_flag=False)
        if op_code == 0x38:
            return self.jump_to_immediate(relative=True, conditional_carry_flag=True)

        # ~`~ Call ~`~
        if op_code == 0xC4:
            return self.call_immediate(conditional_zero_flag=False)
        if op_code == 0xCC:
            return self.call_immediate(conditional_zero_flag=True)
        if op_code == 0xD4:
            return self.call_immediate(conditional_carry_flag=False)
        if op_code == 0xDC:
            return self.call_immediate(conditional_carry_flag=True)
        if op_code == 0xCD:
            return self.call_immediate()

        # ~`~ Reset ~`~
        if op_code == 0xC7:
            return self.reset(0x00)
        if op_code == 0xCF:
            return self.reset(0x08)
        if op_code == 0xD7:
            return self.reset(0x10)
        if op_code == 0xDF:
            return self.reset(0x18)
        if op_code == 0xE7:
            return self.reset(0x20)
        if op_code == 0xEF:
            return self.reset(0x28)
        if op_code == 0xF7:
            return self.reset(0x30)
        if op_code == 0xFF:
            return self.reset(0x38)

        # ~`~ Return ~`~
        if op_code == 0xC9:
            return self.return_()
        if op_code == 0xC0:
            return self.return_(conditional_zero_flag=False)
        if op_code == 0xC8:
            return self.return_(conditional_zero_flag=True)
        if op_code == 0xD0:
            return self.return_(conditional_carry_flag=False)
        if op_code == 0xD8:
            return self.return_(conditional_carry_flag=True)
        if op_code == 0xD9:
            return self.return_(enable_interrupts=True)

        # ~`~ Enable/disable interrupts ~`~
        if op_code == 0xF3:
            return self.disable_interrupts()
        if op_code == 0xFB:
            return self.enable_interrupts()

        # ~`~ Halt ~`~
        if op_code == 0x76:
            return self.halt()

        # ~`~ DAA ~`~
        if op_code == 0x27:
            return self.decimal_adjust_accumulator()

        # ~`~ Stop ~`~
        if op_code == 0x10:
            return self.stop()

        # ~`~ Carry flag ops ~`~
        if op_code == 0x37:
            return self.set_carry_flag()
        if op_code == 0x3F:
            return self.complement_carry_flag()

        raise NotImplementedError(f'Opcode {op_code} not implemented.')

    def no_op(self):
        self._cpu.get_cycle_clock().tick()

    # di: disable interrupts
    def disable_interrupts(self):
        self._cpu.get_registers().disable_interrupts()
        self._cpu.set_interrupt_enable_pending(False)

        self._cpu.get_cycle_clock().tick()

    # ei: enable interrupts
    def enable_interrupts(self):
        self._cpu.set_interrupt_enable_pending(True)

        self._cpu.get_cycle_clock().tick()

    def halt(self):
        self._cpu.set_halted()
        self._cpu.get_cycle_clock().tick()

    def stop(self):
        self._cpu.stop()
        self._cpu.get_cycle_clock().tick()

    # Move program counter to a address in memory unconditionally
    def reset(self, address: int):
        self._cpu.push_word_to_stack(self._cpu.get_registers().get_program_counter())
        self._cpu.get_registers().set_program_counter(address)

        self._cpu.get_cycle_clock().tick(3)

    def return_(self, conditional_zero_flag: bool=None, conditional_carry_flag: bool=None, enable_interrupts=False):
        self._cpu.get_cycle_clock().tick(1)

        if conditional_zero_flag is not None:
            if not conditional_zero_flag == (self._cpu.get_registers().read_flag_zero() > 0):
                return

        if conditional_carry_flag is not None:
            if not conditional_carry_flag == (self._cpu.get_registers().read_flag_carry() > 0):
                return

        if enable_interrupts:
            self._cpu.get_registers().enable_interrupts()

        self._jump(self._cpu.pop_word_from_stack())

        self._cpu.get_cycle_clock().tick(2)

    def call_immediate(self, conditional_zero_flag: bool=None, conditional_carry_flag: bool=None):
        call_to_immediate = self._cpu.read_immediate_word()
        self._cpu.get_cycle_clock().tick(3)

        if conditional_zero_flag is not None:
            if not conditional_zero_flag == (self._cpu.get_registers().read_flag_zero() > 0):
                return

        if conditional_carry_flag is not None:
            if not conditional_carry_flag == (self._cpu.get_registers().read_flag_carry() > 0):
                return

        self._cpu.push_word_to_stack(self._cpu.get_registers().get_program_counter())
        self._cpu.get_registers().set_program_counter(call_to_immediate)

        self._cpu.get_cycle_clock().tick(2)

    # scf: set carry flag
    def set_carry_flag(self):
        self._cpu.get_registers().update_flag_subtract(False)
        self._cpu.get_registers().update_flag_half_carry(False)
        self._cpu.get_registers().update_flag_carry(True)

        self._cpu.get_cycle_clock().tick()

    # ccf: complement carry flag
    def complement_carry_flag(self):
        self._cpu.get_registers().update_flag_subtract(False)
        self._cpu.get_registers().update_flag_half_carry(False)
        self._cpu.get_registers().update_flag_carry(not self._cpu.get_registers().read_flag_carry())

        self._cpu.get_cycle_clock().tick()

    # ld $reg8, $reg8: Load 8 bit register with value of another
    def load(self, from_register: str, to_register: str):
        from_register_name = self._get_8_bit_register_name_from_key(from_register)
        to_register_name = self._get_8_bit_register_name_from_key(to_register)

        self._set_8_bit_register_value(to_register_name, getattr(self._cpu.get_registers(), from_register_name))

        self._cpu.get_cycle_clock().tick(1)

    # ld $reg16, $reg16: Load 16 bit register with value of another
    # immediate_offset will offset the from_register by SIGNED immediate byte and set flags
    def load_16_bit(self, from_register: str, to_register: str, immediate_signed_offset=False):
        from_register_value = self._get_16_bit_register_value(from_register)
        signed_offset = self._cpu.read_immediate_signed_byte() if immediate_signed_offset else 0
        offset_from_register_value = (from_register_value + signed_offset) & 0xFFFF

        self._set_16_bit_register_value(to_register, offset_from_register_value)

        if immediate_signed_offset:
            self._cpu.get_registers().update_flags(
                zero=False,
                subtract=False,
                carry=self._is_carry(offset_from_register_value, from_register_value),
                half_carry=self._is_half_carry(offset_from_register_value, from_register_value)
            )

            self._cpu.get_cycle_clock().tick(3)
        else:
            self._cpu.get_cycle_clock().tick(2)

    # ld $reg8, ($reg16(+,-)): Load 8 bit register with value of memory location at 16 bit register
    # Optionally increment or decrement 16 bit register
    def load_register_with_memory(self, to_register: str, memory_register_16: str='hl',
                                  increment_memory_register=False, decrement_memory_register=False):
        to_register_name = self._get_8_bit_register_name_from_key(to_register)
        memory_location = self._get_16_bit_register_value(memory_register_16)
        memory_location_value = self._cpu.get_memory_unit().read_byte(memory_location)

        self._set_8_bit_register_value(to_register_name, memory_location_value)

        if increment_memory_register:
            self._modify_16_bit_register_value(memory_register_16, 1)

        if decrement_memory_register:
            self._modify_16_bit_register_value(memory_register_16, -1)

        self._cpu.get_cycle_clock().tick(2)

    # ld ($reg16(+,-)), $reg8: Load memory location at 16 bit register with value of 8 bit register.
    # Optionally increment or decrement 16 bit register
    def load_memory_with_register(self, from_register: str, memory_register_16: str='hl',
                                  increment_memory_register: bool=False, decrement_memory_register: bool=False):
        from_register_name = self._get_8_bit_register_name_from_key(from_register)
        memory_location = self._get_16_bit_register_value(memory_register_16)
        register_value = self._get_8_bit_register_value(from_register_name)

        self._cpu.get_memory_unit().write_byte(memory_location, register_value)

        if increment_memory_register:
            self._modify_16_bit_register_value(memory_register_16, 1)

        if decrement_memory_register:
            self._modify_16_bit_register_value(memory_register_16, -1)

        self._cpu.get_cycle_clock().tick(2)

    # ld (0xFF00 + $reg8), $reg8: Load memory location at register+OxFF00 with another register
    def load_offset_memory_at_register_with_register(self, offset_memory_register: str, from_register: str):
        from_register_name = self._get_8_bit_register_name_from_key(from_register)
        offset_memory_register_name = self._get_8_bit_register_name_from_key(offset_memory_register)

        from_register_value = self._get_8_bit_register_value(from_register_name)
        offset_memory_address = self._get_8_bit_register_value(offset_memory_register_name) + 0xFF00

        self._cpu.get_memory_unit().write_byte(offset_memory_address, from_register_value)

        self._cpu.get_cycle_clock().tick(2)

    # ld ($hl), imm8: Load memory location at HL with immediate byte
    def load_memory_with_immediate(self):
        memory_location = self._cpu.get_registers().read_hl()
        immediate_byte = self._cpu.read_immediate_byte()

        self._cpu.get_memory_unit().write_byte(memory_location, immediate_byte)

        self._cpu.get_cycle_clock().tick(3)

    # ld (imm16), $reg8: Load immediate memory address with 8 bit register
    # High memory load uses an immediate 8 bit integer offset by 0xFF00 instead of imm16 (ld (imm8+0xFF00), $reg8)
    def load_immediate_memory_with_register(self, from_register: str, high_memory_load=False):
        if high_memory_load:
            immediate_memory_location = self._cpu.read_immediate_byte() + 0xFF00
        else:
            immediate_memory_location = self._cpu.read_immediate_word()

        from_register_name = self._get_8_bit_register_name_from_key(from_register)
        register_value = self._get_8_bit_register_value(from_register_name)

        self._cpu.get_memory_unit().write_byte(immediate_memory_location, register_value)

        if high_memory_load:
            self._cpu.get_cycle_clock().tick(3)
        else:
            self._cpu.get_cycle_clock().tick(4)

    # ld (imm16), $reg16: Load immediate memory address with 16 bit register
    def load_immediate_memory_with_16_bit_register(self, from_register: str):
        immediate_memory_location = self._cpu.read_immediate_word()
        register_value = self._get_16_bit_register_value(from_register)

        self._cpu.get_memory_unit().write_word(immediate_memory_location, register_value)
        self._cpu.get_cycle_clock().tick(5)

    # ld $reg8, imm8: Load 8 bit register with immediate byte
    def load_register_with_immediate_byte(self, to_register: str):
        immediate_byte_value = self._cpu.read_immediate_byte()
        to_register_name = self._get_8_bit_register_name_from_key(to_register)

        self._set_8_bit_register_value(to_register_name, immediate_byte_value)

        self._cpu.get_cycle_clock().tick(2)

    # ld $reg16, imm16: Load 16 bit register with immediate word
    def load_register_with_immediate_word(self, to_register: str):
        immediate_word_value = self._cpu.read_immediate_word()
        self._set_16_bit_register_value(to_register, immediate_word_value)

        self._cpu.get_cycle_clock().tick(3)

    # ld $reg8, (imm16): Load 8 bit register with immediate memory value
    # High memory read uses an immediate 8 bit integer offset by 0xFF00 instead of imm16 (ld $reg8, (imm8+0xFF00))
    def load_register_with_immediate_memory(self, to_register: str, high_memory_read: bool=False):
        if high_memory_read:
            immediate_memory_location = self._cpu.read_immediate_byte() + 0xFF00
        else:
            immediate_memory_location = self._cpu.read_immediate_word()

        to_register_name = self._get_8_bit_register_name_from_key(to_register)
        immediate_memory_location_value = self._cpu.get_memory_unit().read_byte(immediate_memory_location)

        self._set_8_bit_register_value(to_register_name, immediate_memory_location_value)

        if high_memory_read:
            self._cpu.get_cycle_clock().tick(3)
        else:
            self._cpu.get_cycle_clock().tick(4)

    # ld $reg8, (0xFF00 + $reg8): load 8 bit register with value of memory address at offset 8 bit register
    def load_register_with_offset_memory_at_register(self, to_register: str, offset_memory_register: str):
        to_register_name = self._get_8_bit_register_name_from_key(to_register)
        offset_memory_register_name = self._get_8_bit_register_name_from_key(offset_memory_register)

        offset_memory_address = self._get_8_bit_register_value(offset_memory_register_name) + 0xFF00
        offset_memory_address_value = self._cpu.get_memory_unit().read_byte(offset_memory_address)

        self._set_8_bit_register_value(to_register_name, offset_memory_address_value)

        self._cpu.get_cycle_clock().tick(2)

    # pop $reg16: pop value from stack into 16 bit register
    def pop_stack_to_register(self, to_register: str):
        self._set_16_bit_register_value(to_register, self._cpu.pop_word_from_stack())

        self._cpu.get_cycle_clock().tick(3)

    # push $reg16: push value from 16 bit register onto stack
    def push_register_to_stack(self, to_register: str):
        self._cpu.push_word_to_stack(self._get_16_bit_register_value(to_register))

        self._cpu.get_cycle_clock().tick(3)

    # add|c $reg8, $reg8: Add two registers together. Optionally add the carry flag bit as well.
    def add_8_bit_registers(self, result_register: str, add_register: str, with_carry_bit: bool=False):
        add_register_name = self._get_8_bit_register_name_from_key(add_register)
        add_register_value = self._get_8_bit_register_value(add_register_name)

        self._add_8_bit(add_register_value, result_register, with_carry_bit=with_carry_bit)

        self._cpu.get_cycle_clock().tick(1)

    # add|c $reg8, (hl): Add value of memory at hl to 8 bit register. Optional carry bit.
    def add_8_bit_hl_memory_to_register(self, result_register: str, with_carry_bit: bool=False):
        memory_address = self._cpu.get_registers().read_hl()
        memory_value_to_add = self._cpu.get_memory_unit().read_byte(memory_address)

        self._add_8_bit(memory_value_to_add, result_register, with_carry_bit=with_carry_bit)

        self._cpu.get_cycle_clock().tick(2)

    # add|c $reg8, imm8: Add value of immediate to 8 bit register. Optional carry bit.
    def add_8_bit_immediate_to_register(self, result_register: str, with_carry_bit: bool=False):
        immediate_value = self._cpu.read_immediate_byte()

        self._add_8_bit(immediate_value, result_register, with_carry_bit=with_carry_bit)

        self._cpu.get_cycle_clock().tick(2)

    def _add_8_bit(self, add_value: int, result_register: str, with_carry_bit: bool=False):
        result_register_name = self._get_8_bit_register_name_from_key(result_register)
        result_register_value = self._get_8_bit_register_value(result_register_name)

        sum_ = result_register_value + add_value
        half_sum = (result_register_value & 0xF) + (add_value & 0xF)

        if with_carry_bit and self._cpu.get_registers().read_flag_carry():
            sum_ += 1
            half_sum += 1

        self._cpu.get_registers().update_flags(
            zero=sum_ & 0xFF == 0,
            subtract=False,
            half_carry=half_sum > 0xF,
            carry=sum_ > 0xFF)

        self._set_8_bit_register_value(result_register_name, sum_ & 0xFF)

    # add $reg16, $reg16: add two 16 bit registers together
    def add_16_bit_registers(self, result_register_16: str, add_register_16: str):
        add_register_value = self._get_16_bit_register_value(add_register_16)

        self._add_16_bit(add_register_value, result_register_16)

        self._cpu.get_cycle_clock().tick(3)

    def _add_16_bit(self, add_value_16: int, result_register_16: str):
        result_register_value = self._get_16_bit_register_value(result_register_16)

        sum_ = result_register_value + add_value_16
        half_sum = (result_register_value & 0xFFF) + (add_value_16 & 0xFFF)

        self._cpu.get_registers().update_flag_subtract(False)
        self._cpu.get_registers().update_flag_half_carry(half_sum > 0xFFF)
        self._cpu.get_registers().update_flag_carry(sum_ > 0xFFFF)

        self._set_16_bit_register_value(result_register_16, sum_ & 0xFFFF)

    # add $reg16, imm8i: Add signed immediate to 16 bit register
    def add_signed_immediate_to_16_bit_register(self, result_register_16: str):
        result_register_value = self._get_16_bit_register_value(result_register_16)
        signed_immediate = self._cpu.read_immediate_signed_byte()

        offset_register_value = result_register_value + signed_immediate

        self._cpu.get_registers().update_flags(
            zero=False,
            subtract=False,
            half_carry=(offset_register_value & 0xF) < (result_register_value & 0xF),
            carry=(offset_register_value & 0xFF) < (result_register_value & 0xFF)
        )

        self._set_16_bit_register_value(result_register_16, offset_register_value)

        self._cpu.get_cycle_clock().tick(4)

    # sub|c $reg8, $reg8: Subtract two registers. Optionally subtract the carry flag bit as well.
    # Setting compare_only will only modify flags and not actually modify register
    def subtract_8_bit_registers(self, result_register: str, subtract_register: str,
                                 with_carry_bit: bool = False, compare_only: bool = False):
        subtract_register_name = self._get_8_bit_register_name_from_key(subtract_register)
        subtract_register_value = self._get_8_bit_register_value(subtract_register_name)

        self._subtract_8_bit(subtract_register_value, result_register,
                             with_carry_bit=with_carry_bit, compare_only=compare_only)

        self._cpu.get_cycle_clock().tick(1)

    # sub|c $reg8, (hl): Subtract value of memory at hl from 8 bit register. Optional carry bit.
    # Setting compare_only will only modify flags and not actually modify register
    def subtract_8_bit_hl_memory_to_register(self, result_register: str,
                                             with_carry_bit: bool = False, compare_only: bool = False):
        memory_address = self._cpu.get_registers().read_hl()
        memory_value_to_subtract = self._cpu.get_memory_unit().read_byte(memory_address)

        self._subtract_8_bit(memory_value_to_subtract, result_register,
                             with_carry_bit=with_carry_bit, compare_only=compare_only)

        self._cpu.get_cycle_clock().tick(2)

    # sub|c $reg8, imm8: Subtract value of immediate from 8 bit register. Optional carry bit.
    # Setting compare_only will only modify flags and not actually modify register
    def subtract_8_bit_immediate_to_register(self, result_register: str,
                                             with_carry_bit: bool = False, compare_only: bool = False):
        immediate_value = self._cpu.read_immediate_byte()

        self._subtract_8_bit(immediate_value, result_register, with_carry_bit=with_carry_bit, compare_only=compare_only)

        self._cpu.get_cycle_clock().tick(2)

    def _subtract_8_bit(self, subtract_value: int, result_register: str,
                        with_carry_bit: bool=False, compare_only: bool=False):
        result_register_name = self._get_8_bit_register_name_from_key(result_register)
        result_register_value = self._get_8_bit_register_value(result_register_name)

        sum_ = result_register_value - subtract_value

        if with_carry_bit and self._cpu.get_registers().read_flag_carry():
            sum_ -= 1
            subtract_value += 1

        self._cpu.get_registers().update_flags(
            zero=sum_ & 0xFF == 0,
            subtract=True,
            half_carry=(result_register_value & 0x0F) < (subtract_value & 0x0F),
            carry=subtract_value > result_register_value)

        if not compare_only:
            self._set_8_bit_register_value(result_register_name, sum_ & 0xFF)

    # inc $reg8: Increment 8 bit register
    def increment_8_bit_register(self, increment_register: str):
        register_name = self._get_8_bit_register_name_from_key(increment_register)
        register_value = self._get_8_bit_register_value(register_name)
        result = (register_value + 1) & 0xFF

        self._set_8_bit_register_value(register_name, result)

        self._cpu.get_registers().update_flags(
            zero=result == 0,
            subtract=False,
            half_carry=(register_value & 0xF) == 0xF,
            carry=self._cpu.get_registers().read_flag_carry() > 0
        )

        self._cpu.get_cycle_clock().tick(1)

    # dec $reg8: Decrement 8 bit register
    def decrement_8_bit_register(self, decrement_register: str):
        register_name = self._get_8_bit_register_name_from_key(decrement_register)
        register_value = self._get_8_bit_register_value(register_name)
        result = (register_value - 1) & 0xFF

        self._set_8_bit_register_value(register_name, result)

        self._cpu.get_registers().update_flags(
            zero=result == 0,
            subtract=True,
            half_carry=(register_value & 0xF) == 0x0,
            carry=self._cpu.get_registers().read_flag_carry() > 0
        )

        self._cpu.get_cycle_clock().tick(1)

    # inc $reg16: Increment 16 bit register
    def increment_16_bit_register(self, increment_register_16: str):
        register_value = self._get_16_bit_register_value(increment_register_16)
        self._set_16_bit_register_value(increment_register_16, (register_value + 1) & 0xFFFF)

        self._cpu.get_cycle_clock().tick(2)

    # dec $reg16: Decrement 16 bit register
    def decrement_16_bit_register(self, decrement_register_16: str):
        register_value = self._get_16_bit_register_value(decrement_register_16)
        self._set_16_bit_register_value(decrement_register_16, (register_value - 1) & 0xFFFF)

        self._cpu.get_cycle_clock().tick(2)

    # inc ($reg16): Increment memory at 16 bit register
    def increment_memory_at_register(self, memory_register_16_bit: str):
        memory_address = self._get_16_bit_register_value(memory_register_16_bit)
        memory_address_value = self._cpu.get_memory_unit().read_byte(memory_address)

        result = (memory_address_value + 1) & 0xFF

        self._cpu.get_memory_unit().write_byte(memory_address, result)

        self._cpu.get_registers().update_flags(
            zero=result == 0,
            subtract=False,
            half_carry=(memory_address_value & 0xF) == 0xF,
            carry=self._cpu.get_registers().read_flag_carry() > 0
        )

        self._cpu.get_cycle_clock().tick(3)

    # dec ($reg16): Decrement memory at 16 bit register
    def decrement_memory_at_register(self, memory_register_16_bit: str):
        memory_address = self._get_16_bit_register_value(memory_register_16_bit)
        memory_address_value = self._cpu.get_memory_unit().read_byte(memory_address)

        result = (memory_address_value - 1) & 0xFF

        self._cpu.get_memory_unit().write_byte(memory_address, result)

        self._cpu.get_registers().update_flags(
            zero=result == 0,
            subtract=True,
            half_carry=(memory_address_value & 0xF) == 0x0,
            carry=self._cpu.get_registers().read_flag_carry() > 0
        )

        self._cpu.get_cycle_clock().tick(3)

    # and $reg8, $reg8: bitwise AND two registers together
    def bitwise_and_8_bit_register(self, result_register: str, bitwise_register: str):
        bitwise_register_name = self._get_8_bit_register_name_from_key(bitwise_register)
        bitwise_register_value = self._get_8_bit_register_value(bitwise_register_name)

        self._bitwise_and_8_bit_register(result_register, bitwise_register_value)

        self._cpu.get_cycle_clock().tick(1)

    # and $reg8, ($reg16): bitwise AND 8 bit register and byte at memory location
    def bitwise_and_8_bit_register_with_memory(self, result_register: str, bitwise_register_16: str='hl'):
        bitwise_memory_address = self._get_16_bit_register_value(bitwise_register_16)
        bitwise_memory_address_value = self._cpu.get_memory_unit().read_byte(bitwise_memory_address)

        self._bitwise_and_8_bit_register(result_register, bitwise_memory_address_value)

        self._cpu.get_cycle_clock().tick(2)

    # and $reg8, imm8: bitwise AND 8 bit register with immediate
    def bitwise_and_8_bit_register_with_immediate_byte(self, result_register: str):
        self._bitwise_and_8_bit_register(result_register, self._cpu.read_immediate_byte())

        self._cpu.get_cycle_clock().tick(2)

    def _bitwise_and_8_bit_register(self, result_register: str, bitwise_value: int):
        result_register_name = self._get_8_bit_register_name_from_key(result_register)

        result_register_value = self._get_8_bit_register_value(result_register_name)
        bitwise_result = result_register_value & bitwise_value

        self._set_8_bit_register_value(result_register_name, bitwise_result)

        self._cpu.get_registers().update_flags(
            zero=bitwise_result == 0,
            subtract=False,
            half_carry=True,
            carry=False
        )

    # or $reg8, $reg8: bitwise OR two registers together
    def bitwise_or_8_bit_register(self, result_register: str, bitwise_register: str):
        bitwise_register_name = self._get_8_bit_register_name_from_key(bitwise_register)
        bitwise_register_value = self._get_8_bit_register_value(bitwise_register_name)

        self._bitwise_or_8_bit_register(result_register, bitwise_register_value)

        self._cpu.get_cycle_clock().tick(1)

    # or $reg8, $reg8: bitwise OR 8 bit register and byte at memory location
    def bitwise_or_8_bit_register_with_memory(self, result_register: str, bitwise_register_16: str='hl'):
        bitwise_memory_address = self._get_16_bit_register_value(bitwise_register_16)
        bitwise_memory_address_value = self._cpu.get_memory_unit().read_byte(bitwise_memory_address)

        self._bitwise_or_8_bit_register(result_register, bitwise_memory_address_value)

        self._cpu.get_cycle_clock().tick(2)

    # or $reg8, $reg8: bitwise OR 8 bit register with immediate
    def bitwise_or_8_bit_register_with_immediate_byte(self, result_register: str):
        self._bitwise_or_8_bit_register(result_register, self._cpu.read_immediate_byte())

        self._cpu.get_cycle_clock().tick(2)

    def _bitwise_or_8_bit_register(self, result_register: str, bitwise_register_value: int):
        result_register_name = self._get_8_bit_register_name_from_key(result_register)

        result_register_value = self._get_8_bit_register_value(result_register_name)
        bitwise_result = result_register_value | bitwise_register_value

        self._set_8_bit_register_value(result_register_name, bitwise_result)

        self._cpu.get_registers().update_flags(
            zero=bitwise_result == 0,
            subtract=False,
            half_carry=False,
            carry=False
        )

    # Xor $reg8, $reg8: bitwise XOR two registers together
    def bitwise_xor_8_bit_register(self, result_register: str, bitwise_register: str):
        bitwise_register_name = self._get_8_bit_register_name_from_key(bitwise_register)
        bitwise_register_value = self._get_8_bit_register_value(bitwise_register_name)

        self._bitwise_xor_8_bit_register(result_register, bitwise_register_value)

        self._cpu.get_cycle_clock().tick(1)

    # Xor $reg8, $reg8: bitwise XOR 8 bit register and byte at memory location
    def bitwise_xor_8_bit_register_with_memory(self, result_register: str, bitwise_register_16: str='hl'):
        bitwise_memory_address = self._get_16_bit_register_value(bitwise_register_16)
        bitwise_memory_address_value = self._cpu.get_memory_unit().read_byte(bitwise_memory_address)

        self._bitwise_xor_8_bit_register(result_register, bitwise_memory_address_value)

        self._cpu.get_cycle_clock().tick(2)

    # Xor $reg8, $reg8: bitwise XOR 8 bit register with immediate
    def bitwise_xor_8_bit_register_with_immediate_byte(self, result_register: str):
        self._bitwise_xor_8_bit_register(result_register, self._cpu.read_immediate_byte())

        self._cpu.get_cycle_clock().tick(2)

    def _bitwise_xor_8_bit_register(self, result_register: str, bitwise_value: int):
        result_register_name = self._get_8_bit_register_name_from_key(result_register)
        result_register_value = self._get_8_bit_register_value(result_register_name)

        bitwise_result = result_register_value ^ bitwise_value

        self._set_8_bit_register_value(result_register_name, bitwise_result)

        self._cpu.get_registers().update_flags(
            zero=bitwise_result == 0,
            subtract=False,
            half_carry=False,
            carry=False
        )

    # rl(c) $reg8: Rotate 8 bit register left
    # with_carry_bit will optionally consider the carry flag as an extra bit
    def rotate_8_bit_register_left(self, result_register: str, with_carry_bit: bool=False):
        result_register_name = self._get_8_bit_register_name_from_key(result_register)
        result_register_value = self._get_8_bit_register_value(result_register_name)
        carry_bit = self._cpu.get_registers().read_flag_carry()

        self._cpu.get_registers().update_flags(
            zero=False,
            subtract=False,
            half_carry=False,
            carry=(result_register_value & 0x80) > 0)

        if with_carry_bit:
            rotated_register_value = (result_register_value << 1) | (0x01 if carry_bit else 0x00)
        else:
            rotated_register_value = (result_register_value << 1) | (result_register_value >> 7)

        self._set_8_bit_register_value(result_register_name, rotated_register_value & 0xFF)

        self._cpu.get_cycle_clock().tick(1)

    # rrc $reg8: Rotate 8 bit register right
    def rotate_8_bit_register_right(self, result_register: str, with_carry_bit: bool=False):
        result_register_name = self._get_8_bit_register_name_from_key(result_register)
        result_register_value = self._get_8_bit_register_value(result_register_name)
        carry_bit = self._cpu.get_registers().read_flag_carry()

        self._cpu.get_registers().update_flags(
            zero=False,
            subtract=False,
            half_carry=False,
            carry=(result_register_value & 0x01) > 0)

        if with_carry_bit:
            rotated_register_value = (result_register_value >> 1) | (0x80 if carry_bit else 0x00)
        else:
            rotated_register_value = (result_register_value >> 1) | (result_register_value << 7)

        self._set_8_bit_register_value(result_register_name, rotated_register_value & 0xFF)

        self._cpu.get_cycle_clock().tick(1)

    # cpl reg8: invert all bits in a register
    def complement_8_bit_register(self, result_register: str):
        self._cpu.get_registers().update_flag_subtract(False)
        self._cpu.get_registers().update_flag_half_carry(False)

        register_name = self._get_8_bit_register_name_from_key(result_register)
        register_value = self._get_8_bit_register_value(register_name)

        self._set_8_bit_register_value(register_name, register_value ^ 0xFF)

    def jump_to_16_bit_register(self, register_16: str):
        self._jump(self._get_16_bit_register_value(register_16))

        self._cpu.get_cycle_clock().tick(1)

    def jump_to_immediate(self, conditional_zero_flag: bool=None, conditional_carry_flag: bool=None, relative=False):
        if relative:
            self._cpu.get_cycle_clock().tick(2)
            jump_to_input = self._cpu.read_immediate_signed_byte()
        else:
            self._cpu.get_cycle_clock().tick(3)
            jump_to_input = self._cpu.read_immediate_word()

        if conditional_zero_flag is not None:
            if not conditional_zero_flag == (self._cpu.get_registers().read_flag_zero() > 0):
                return

        if conditional_carry_flag is not None:
            if not conditional_carry_flag == (self._cpu.get_registers().read_flag_carry() > 0):
                return

        if relative:
            self._jump_relative(jump_to_input)
        else:
            self._jump(jump_to_input)

        if conditional_zero_flag is not None or conditional_carry_flag is not None:
            self._cpu.get_cycle_clock().tick(1)

    def _jump(self, address: int):
        self._cpu.get_registers().set_program_counter(address)

    def _jump_relative(self, offset: int):
        self._cpu.get_registers().set_program_counter(self._cpu.get_registers().get_program_counter() + offset)

    # daa: I...don't get it
    def decimal_adjust_accumulator(self):
        register_a_value = self._get_8_bit_register_value('_register_a')

        if self._cpu.get_registers().read_flag_subtract():
            if self._cpu.get_registers().read_flag_half_carry():
                register_a_value -= 0x06
                register_a_value &= 0xFF

            if self._cpu.get_registers().read_flag_carry():
                register_a_value -= 0x60
        else:
            if register_a_value & 0x0F > 0x09 or self._cpu.get_registers().read_flag_half_carry():
                register_a_value += 0x06

            if register_a_value > 0x9F or self._cpu.get_registers().read_flag_carry():
                register_a_value += 0x60

        self._cpu.get_registers().update_flag_zero(register_a_value & 0xFF == 0)
        self._cpu.get_registers().update_flag_half_carry(False)

        if register_a_value & 0x100:
            self._cpu.get_registers().update_flag_carry(True)

        self._set_8_bit_register_value('_register_a', register_a_value)

    def execute_extended_operation(self):
        operation, bit_index_or_sub_op, register = self._get_extended_operation_parts()

        if operation == 0:  # Shift/rotate and swap
            if bit_index_or_sub_op == 0:  # rlc rN
                return self._extended_op_rotate_left(register)
            if bit_index_or_sub_op == 1:  # rrc rN
                return self._extended_op_rotate_right(register)
            if bit_index_or_sub_op == 2:  # rl rN
                return self._extended_op_rotate_left(register, with_carry_bit=True)
            if bit_index_or_sub_op == 3:  # rr rN
                return self._extended_op_rotate_right(register, with_carry_bit=True)
            if bit_index_or_sub_op == 4:  # sla rN
                return self._extended_op_rotate_left(register, shift_only=True)
            if bit_index_or_sub_op == 5:  # sra rN
                return self._extended_op_rotate_right(register, shift_only_special=True)
            if bit_index_or_sub_op == 6:
                return self._extended_op_swap(register)
            if bit_index_or_sub_op == 7:
                return self._extended_op_rotate_right(register, shift_only=True)

        if operation == 1:  # Read bit from register: bit n, rN
            return self._extended_op_read_bit(register, bit_index_or_sub_op)

        if operation == 2:  # flip bit of register: res n, rN
            return self._extended_op_flip_bit(register, bit_index_or_sub_op)

        if operation == 3:  # set bit of register: set n, rN
            return self._extended_op_set_bit(register, bit_index_or_sub_op)

        raise NotImplementedError(f'Unidentified extended opcode: {operation}')

    def _get_extended_operation_parts(self) -> (int, int, int):
        opcode = self._cpu.read_immediate_byte()

        operation = opcode >> 6
        bit_index_or_sub_op = (opcode >> 3) & 0x07
        register = opcode & 0x07

        return operation, bit_index_or_sub_op, register

    def _extended_op_rotate_left(self, register_index: int, with_carry_bit=False, shift_only=False):
        value = self._get_extended_op_register_value(register_index)

        if shift_only:
            shifted_value = value << 1
        else:
            if with_carry_bit:
                shifted_value = (value << 1) | (1 if self._cpu.get_registers().read_flag_carry() else 0)
            else:
                shifted_value = (value << 1) | (value >> 7)

        self._cpu.get_registers().update_flags(
            zero=shifted_value == 0,
            subtract=False,
            half_carry=False,
            carry=(value & 0x80) > 0
        )

        self._set_extended_op_register_value(register_index, shifted_value & 255)

        self._cpu.get_cycle_clock().tick(4 if register_index == 6 else 2)  # writing to (HL) takes 2 extra cycles

    def _extended_op_rotate_right(self, register_index: int, with_carry_bit=False, shift_only=False,
                                  shift_only_special=False):
        value = self._get_extended_op_register_value(register_index)

        if shift_only:
            shifted_value = (value >> 1)
        elif shift_only_special:
            shifted_value = (value >> 1) | (value & 0x80)
        else:
            if with_carry_bit:
                shifted_value = (value >> 1) | (0x80 if self._cpu.get_registers().read_flag_carry() else 0)
            else:
                shifted_value = (value >> 1) | (value << 7)

        self._cpu.get_registers().update_flags(
            zero=shifted_value == 0,
            subtract=False,
            half_carry=False,
            carry=(value & 0x01) > 0
        )

        self._set_extended_op_register_value(register_index, shifted_value & 255)

        self._cpu.get_cycle_clock().tick(4 if register_index == 6 else 2)  # writing to (HL) takes 2 extra cycles

    def _extended_op_swap(self, register_index: int):
        value = self._get_extended_op_register_value(register_index)

        swapped_value = (value >> 4) | (value << 4)

        self._cpu.get_registers().update_flags(
            zero=swapped_value == 0,
            subtract=False,
            half_carry=False,
            carry=False
        )

        self._set_extended_op_register_value(register_index, swapped_value & 255)

        self._cpu.get_cycle_clock().tick(1)

    def _extended_op_read_bit(self, register_index: int, bit_index: int):
        value = self._get_extended_op_register_value(register_index)

        self._cpu.get_registers().update_flags(
            zero=(value & (1 << bit_index) == 0),
            subtract=False,
            half_carry=False,
            carry=self._cpu.get_registers().read_flag_carry() > 0
        )

        self._cpu.get_cycle_clock().tick(2 if register_index != 6 else 3)  # reading (HL) takes 1 extra cycle

    def _extended_op_flip_bit(self, register_index: int, bit_index: int):
        value = self._get_extended_op_register_value(register_index)
        flipped_bit_value = value & ~(1 << bit_index)

        self._set_extended_op_register_value(register_index, flipped_bit_value)

        self._cpu.get_cycle_clock().tick(2 if register_index != 6 else 4)  # writing (HL) takes 2 extra cycles

    def _extended_op_set_bit(self, register_index: int, bit_index: int):
        value = self._get_extended_op_register_value(register_index)
        set_bit_value = value | (1 << bit_index)

        self._set_extended_op_register_value(register_index, set_bit_value)

        self._cpu.get_cycle_clock().tick(2 if register_index != 6 else 4)  # writing (HL) takes 2 extra cycles

    def _get_extended_op_register_value(self, register_index: int) -> int:
        if register_index == 0:
            return self._get_8_bit_register_value('_register_b')
        if register_index == 1:
            return self._get_8_bit_register_value('_register_c')
        if register_index == 2:
            return self._get_8_bit_register_value('_register_d')
        if register_index == 3:
            return self._get_8_bit_register_value('_register_e')
        if register_index == 4:
            return self._get_8_bit_register_value('_register_h')
        if register_index == 5:
            return self._get_8_bit_register_value('_register_l')
        if register_index == 6:
            return self._cpu.get_memory_unit().read_byte(self._cpu.get_registers().read_hl())
        if register_index == 7:
            return self._get_8_bit_register_value('_register_a')

        raise NotImplementedError(f'register_index {register_index} is out of range')

    def _set_extended_op_register_value(self, register_index: int, register_value: int):
        if register_index == 0:
            self._set_8_bit_register_value('_register_b', register_value)
            return
        if register_index == 1:
            self._set_8_bit_register_value('_register_c', register_value)
            return
        if register_index == 2:
            self._set_8_bit_register_value('_register_d', register_value)
            return
        if register_index == 3:
            self._set_8_bit_register_value('_register_e', register_value)
            return
        if register_index == 4:
            self._set_8_bit_register_value('_register_h', register_value)
            return
        if register_index == 5:
            self._set_8_bit_register_value('_register_l', register_value)
            return
        if register_index == 6:
            self._cpu.get_memory_unit().write_byte(self._cpu.get_registers().read_hl(), register_value)
            return
        if register_index == 7:
            self._set_8_bit_register_value('_register_a', register_value)
            return

        raise NotImplementedError(f'register_index {register_index} is out of range')

    def _get_8_bit_register_name_from_key(self, register_key: str) -> str:
        register_name = f'_register_{register_key}'

        if not hasattr(self._cpu.get_registers(), register_name):
            raise AttributeError(f'Invalid register {register_name}')

        return register_name

    def _set_8_bit_register_value(self, register_name: str, value: int):
        setattr(self._cpu.get_registers(), register_name, value)

    def _get_8_bit_register_value(self, register_name: str) -> int:
        return getattr(self._cpu.get_registers(), register_name)

    def _modify_16_bit_register_value(self, register_name: str, change: int):
        register_setter_name = self._get_16_bit_register_setter_name(register_name)
        current_register_value = self._get_16_bit_register_value(register_name)

        getattr(self._cpu.get_registers(), register_setter_name)(current_register_value + change)

    def _set_16_bit_register_value(self, register_name: str, value: int):
        register_setter_name = self._get_16_bit_register_setter_name(register_name)

        getattr(self._cpu.get_registers(), register_setter_name)(value)

    def _get_16_bit_register_value(self, register_name: str) -> int:
        return getattr(self._cpu.get_registers(), self._get_16_bit_register_getter_name(register_name))()

    def _get_16_bit_register_getter_name(self, register_name: str) -> str:
        if register_name == 'sp':
            register_getter_name = 'get_stack_pointer'
        else:
            register_getter_name = f'read_{register_name}'

        if not hasattr(self._cpu.get_registers(), register_getter_name):
            raise AttributeError(f'Invalid register {register_name}')

        return register_getter_name

    def _get_16_bit_register_setter_name(self, register_name: str) -> str:
        if register_name == 'sp':
            register_setter_name = 'set_stack_pointer'
        else:
            register_setter_name = f'write_{register_name}'

        if not hasattr(self._cpu.get_registers(), register_setter_name):
            raise AttributeError(f'Invalid register {register_name}')

        return register_setter_name

    def _is_half_carry(self, result, input_):
        return (result & 0xF) < (input_ & 0xF)

    def _is_carry(self, result, input_):
        return (result & 0xFF) < (input_ & 0xFF)

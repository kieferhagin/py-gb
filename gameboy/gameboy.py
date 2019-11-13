from gameboy.memory_unit import MemoryUnit
from gameboy.rom import ROM


class GameBoy:
    def __init__(self):
        self._rom = None
        self._memory_unit = MemoryUnit()

    def load_rom(self, rom: ROM) -> bool:
        print('Loaded ROM: {}'.format(rom.get_title()))

        self._rom = rom

        return True

    def start(self) -> None:
        pass

    def step(self) -> None:
        pass

    def set_interrupt(self, interrupt_bit):
        pass

    def get_memory_unit(self) -> MemoryUnit:
        return self._memory_unit

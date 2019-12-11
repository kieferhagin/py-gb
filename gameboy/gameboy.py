from gameboy.cpu.cpu import CPU
from gameboy.memory.memory_unit import MemoryUnit
from gameboy.rom import ROM


class GameBoy:
    def __init__(self):
        self._rom = None
        self._memory_unit = MemoryUnit()

        self._cpu = CPU(self._memory_unit)

    def load_rom(self, rom: ROM) -> bool:
        print('Loaded ROM: {}'.format(rom.get_title()))

        self._rom = rom
        self._memory_unit.set_cartridge_rom(rom)

        return True

    def start(self) -> None:
        pass

    def step(self) -> None:
        # TODO: input update
        self._cpu.handle_interrupts()
        self._cpu.step()
        self._memory_unit.dma_update()

    def set_interrupt(self, interrupt_bit):
        pass

    def get_memory_unit(self) -> MemoryUnit:
        return self._memory_unit

    def reset(self):
        self._cpu.reset()


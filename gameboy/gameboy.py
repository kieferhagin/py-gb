from gameboy.rom import ROM


class GameBoy:
    def __init__(self):
        self._rom = None

    def load_rom(self, rom: ROM) -> bool:
        print('Loaded ROM: {}'.format(rom.get_title()))

        self._rom = rom

        return True

    def start(self) -> None:
        pass

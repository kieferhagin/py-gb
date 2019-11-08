from gameboy.gameboy import GameBoy
from gameboy.rom import ROM


def main():
    print("Hello World!")
    print("Starting emulator...")

    test_rom = load_test_rom()

    game_boy = GameBoy()
    game_boy.load_rom(rom=test_rom)


def load_test_rom():
    with open("test_roms/instr_timing.gb", "rb") as binary_file:
        return ROM(bytearray(binary_file.read()))


if __name__ == "__main__":
    main()


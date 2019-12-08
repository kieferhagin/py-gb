import time

from gameboy.gameboy import GameBoy
from gameboy.rom import ROM
from gameboy.timer_registers import TimerRegisters


def main():
    print("Hello World!")
    print("Starting emulator...")

    test_rom = load_tetris()

    game_boy = GameBoy()
    game_boy.load_rom(rom=test_rom)

    test_rom.validate_header_checksum()
    test_rom.validate_rom_checksum()
    memory_bank_model = test_rom.get_memory_bank_model()

    step_test(game_boy)

    # timer_test()


def load_test_rom():
    with open("test_roms/instr_timing.gb", "rb") as binary_file:
        return ROM(bytearray(binary_file.read()))

def load_tetris():
    with open("test_roms/TETRIS.GB", "rb") as binary_file:
        return ROM(bytearray(binary_file.read()))

def step_test(gameboy):
    print("Running timer test...")

    while True:
        gameboy.step()
        time.sleep(0.000001)

def timer_test():
    print("Running timer test...")

    def fake_set_interrupt():
        print("Interrupt set!")

    timer_registers = TimerRegisters(fake_set_interrupt)
    timer_registers._data[3] = 0b00000110  # Enabled, 64
    timer_registers._data[2] = 100  # Modulo

    while True:
        timer_registers.tick()
        print(', '.join('{:02x}'.format(x) for x in timer_registers._data))
        time.sleep(0.001)


if __name__ == "__main__":
    main()


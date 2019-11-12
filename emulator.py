import time

from gameboy.gameboy import GameBoy
from gameboy.rom import ROM
from gameboy.timer_registers import TimerRegisters


def main():
    print("Hello World!")
    print("Starting emulator...")

    test_rom = load_test_rom()

    game_boy = GameBoy()
    game_boy.load_rom(rom=test_rom)

    # timer_test()


def load_test_rom():
    with open("test_roms/instr_timing.gb", "rb") as binary_file:
        return ROM(bytearray(binary_file.read()))


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


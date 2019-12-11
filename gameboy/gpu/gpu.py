from math import floor

from gameboy.gpu.gpu_sprite import GPUSprite
from gameboy.memory.memory_unit import MemoryUnit


class GPU:
    def __init__(self, memory_unit: MemoryUnit):
        self._memory_unit = memory_unit
        self._frame_progress = 0
        self._buffer = [[0 for _ in range(0, 144)] for _ in range(0, 160)]
        self._new_frame_available = False

    def _get_map_pixel(self, high_map: bool, low_tiles: bool, x: int, y: int) -> int:
        base_tile_index_address = 0x9C00 if high_map else 0x9800
        tile_index_address = int(base_tile_index_address + ((floor(y / 8) * 32) + (floor(x / 8))))

        tile_index = self._memory_unit.read_byte(tile_index_address)

        address = self._get_tile_line_address(tile_index, (y % 8), low_tiles)

        line_0_byte = self._memory_unit.read_byte(address)
        line_1_byte = self._memory_unit.read_byte(address + 1)

        return self._get_line_pixel(line_0_byte, line_1_byte, x % 8)

    @staticmethod
    def _get_line_pixel(line_0_byte: int, line_1_byte: int, x: int) -> int:
        return (((line_0_byte << x) & 0x80) >> 7) | (((line_1_byte << x) & 0x80) >> 6)

    @staticmethod
    def _get_tile_line_address(tile_index_byte: int, y: int, use_lower_bank: bool) -> int:
        base_address = tile_index_byte * 16 if use_lower_bank else 0x1000 + (tile_index_byte * 16)

        return base_address + 0x8000 + (y * 2)

    @staticmethod
    def _get_pixel_palette(pixel_byte: int, palette_byte: int) -> int:
        if pixel_byte > 3:
            raise ValueError('Invalid pixel_byte')

        return (palette_byte >> (pixel_byte * 2)) & 0x03

    def _read_sprites(self, scanline_number: int):
        sprite_height = self._memory_unit\
            .get_io_ram()\
            .get_sprite_height()

        unordered_sprites = []

        for sprite_oam_offset in range(0, 160, 4):
            sprite_memory_address = 0xFE00 + sprite_oam_offset

            sprite_y_position = self._memory_unit.read_byte(sprite_memory_address)
            sprite_x_position = self._memory_unit.read_byte(sprite_memory_address + 1)

            sprite_off_screen = sprite_y_position <= 0 or sprite_y_position >= 160 or sprite_x_position >= 168

            if sprite_off_screen:
                continue

            sprite_in_scan_line = sprite_y_position <= scanline_number + 16 < sprite_y_position + sprite_height

            if not sprite_in_scan_line:
                continue

            sprite_tile = self._memory_unit.read_byte(sprite_memory_address + 2)
            sprite_attributes = self._memory_unit.read_byte(sprite_memory_address + 3)

            if sprite_height == 16:
                sprite_tile &= 0xFE

            sprite_tile_y = (scanline_number + 16) - sprite_y_position

            if sprite_attributes & 0x40:  # Flip Y
                sprite_tile_y = (sprite_height - 1) - sprite_tile_y

            sprite_tiles_address = self._get_tile_line_address(sprite_tile, sprite_tile_y, use_lower_bank=True)

            unordered_sprites.append(
                GPUSprite(
                    x=sprite_x_position,
                    y=sprite_y_position,
                    tiles=[
                        self._memory_unit.read_byte(sprite_tiles_address),
                        self._memory_unit.read_byte(sprite_tiles_address + 1)
                    ],
                    attributes=sprite_attributes
                )
            )

            # TODO: order sprites
            # TODO: limit to 10 sprites per scanline

        return unordered_sprites

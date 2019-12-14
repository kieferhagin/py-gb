from math import floor
from typing import List

from gameboy.gpu.gpu_sprite import GPUSprite
from gameboy.memory.io_ram import IORAM
from gameboy.memory.memory_unit import MemoryUnit


class GPU:
    def __init__(self, memory_unit: MemoryUnit):
        self._memory_unit = memory_unit
        self._frame_progress = 0
        self._buffer = [[0 for _ in range(0, 144)] for _ in range(0, 160)]
        self._new_frame_available = False
        self._sprite_buffer: List[GPUSprite] = []

        self._current_x = 0

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

    def _get_scanline_sprites(self, scanline_number: int):
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
                    pixels=[
                        self._memory_unit.read_byte(sprite_tiles_address),
                        self._memory_unit.read_byte(sprite_tiles_address + 1)
                    ],
                    attributes=sprite_attributes
                )
            )

            # TODO: order sprites
            # TODO: limit to 10 sprites per scanline

        return unordered_sprites

    def draw_pixel(self, scanline_number: int, x: int):
        io_ram = self._memory_unit.get_io_ram()

        window_enabled = io_ram.get_lcd_window_enable()
        sprites_enabled = io_ram.get_lcd_sprite_enable()
        background_enabled = io_ram.get_lcd_background_enable()
        high_map_window = io_ram.get_lcd_high_map_window()
        high_map_background = io_ram.get_lcd_high_map_background()
        low_tiles = io_ram.get_lcd_low_tiles()

        window_x = io_ram.get_lcd_window_x()
        window_y = io_ram.get_lcd_window_y()

        window_overlaps = window_x < 167 and window_y < 144 and window_y <= scanline_number
        has_sprites = len(self._sprite_buffer) > 0

        should_render_window = window_enabled and window_overlaps
        should_render_sprites = sprites_enabled and has_sprites

        should_render = should_render_window or background_enabled or should_render_sprites

        if not should_render:
            return

        scroll_x = io_ram.get_lcd_scroll_x()
        scroll_y = io_ram.get_lcd_scroll_y()

        if should_render_window and x + 7 > window_x:
            background_pixel = self._get_map_pixel(high_map_window, low_tiles,
                                                   (x + 7) - window_x, scanline_number - window_y)
        elif background_enabled:
            background_pixel = self._get_map_pixel(high_map_background, low_tiles,
                                                   (x + scroll_x) % 256, (scanline_number + scroll_y) % 256)
        else:
            background_pixel = 0x00

        background_pixel_color = self._get_pixel_palette(background_pixel, io_ram.get_lcd_background_palette())

        sprite_pixel_color = 0

        if sprites_enabled:
            object_palettes = [
                io_ram.get_lcd_object_palette0(),
                io_ram.get_lcd_object_palette1()
            ]

            for sprite in self._sprite_buffer:
                pixel_within_sprite = sprite.get_x() <= x + 8 < sprite.get_x() + 8

                if not pixel_within_sprite:
                    continue

                tile_x = (x + 8) - sprite.get_x()
                # TODO: mirroring

                sprite_pixel = self._get_line_pixel(sprite.get_pixels()[0], sprite.get_pixels()[1], tile_x)

                if sprite_pixel > 0:
                    # TODO: priority
                    sprite_pixel_color = self._get_pixel_palette(sprite_pixel, object_palettes[0])  # TODO: multiple palettes
                    break

        self._buffer[x][scanline_number] = sprite_pixel_color or background_pixel_color

    def video_update(self):
        io_ram = self._memory_unit.get_io_ram()
        scanline_number = int(floor(self._frame_progress / 456))

        lcd_on = io_ram.get_lcd_on()
        lcd_stat = io_ram.get_lcd_stat()

        if lcd_on:
            self._lcdy_compare(scanline_number)

        lcd_mode = lcd_stat & 0x03

        # Last 10 scan lines are VBlank, nothing is drawn
        if scanline_number >= 144:
            if lcd_mode != IORAM.LCDMode.LCD_VBLANK.value:
                self._vblank()

        else:
            scanline_progress = self._frame_progress % 456

            if scanline_progress < 92:
                if lcd_mode != IORAM.LCDMode.LCD_OAM_READ:
                    self._oam_read(scanline_number)

            elif scanline_progress < (160 + 92):
                self._transfer_data_to_buffer(scanline_progress, scanline_number)

            else:
                self._hblank(scanline_number)

        self._frame_progress = (self._frame_progress + 1) % 70224

    def _lcdy_compare(self, scanline_number: int):
        io_ram = self._memory_unit.get_io_ram()
        lcd_stat = io_ram.get_lcd_stat()

        if scanline_number == self._memory_unit.get_io_ram().get_lcd_y_compare():
            coincidence_bit_set = (lcd_stat & 0x04) > 0

            if not coincidence_bit_set:
                io_ram.set_lcd_stat_bits(0x04)

                is_coincidence_interrupt_enabled = (lcd_stat & 0x40) > 0

                if is_coincidence_interrupt_enabled:
                    self._memory_unit\
                        .get_interrupt_flag_register()\
                        .set_lcdc_interrupt()
        else:
            io_ram.clear_lcd_stat_bits(0x04)

    def _vblank(self):
        # Entering VBlank, trigger interrupt
        self._memory_unit.get_io_ram().set_lcd_mode(IORAM.LCDMode.LCD_VBLANK)
        self._memory_unit.get_interrupt_flag_register().set_vblank_interrupt()

        # TODO: clear buffer if LCD not on (?)
        self._new_frame_available = True

    def _oam_read(self, scanline_number: int):
        io_ram = self._memory_unit.get_io_ram()
        io_ram.set_lcd_mode(IORAM.LCDMode.LCD_OAM_READ)

        oam_read_interrupt_enabled = (io_ram.get_lcd_stat() & 0x20) > 0

        if oam_read_interrupt_enabled:
            self._memory_unit.get_interrupt_flag_register().set_lcdc_interrupt()

        self._sprite_buffer = self._get_scanline_sprites(scanline_number)
        self._current_x = 0

    def _transfer_data_to_buffer(self, scanline_progress: int, scanline_number: int):
        self._memory_unit.get_io_ram().set_lcd_mode(IORAM.LCDMode.LCD_TRANSFER)

        if self._memory_unit.get_io_ram().get_lcd_on():
            while self._current_x < scanline_progress - 92:
                self.draw_pixel(scanline_number, self._current_x)
                self._current_x += 1

    def _hblank(self, scanline_number: int):
        self._memory_unit.get_io_ram().set_lcd_mode(IORAM.LCDMode.LCD_HBLANK)

        if self._memory_unit.get_io_ram().get_lcd_on():
            while self._current_x < 160:
                self.draw_pixel(scanline_number, self._current_x)
                self._current_x += 1

        hblank_interrupt_enabled = (self._memory_unit.get_io_ram().get_lcd_stat() & 0x08) > 0

        if hblank_interrupt_enabled:
            self._memory_unit.get_interrupt_flag_register().set_lcdc_interrupt()

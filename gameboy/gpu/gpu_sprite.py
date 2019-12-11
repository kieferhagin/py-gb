class GPUSprite:
    def __init__(self, x: int, y: int, tiles: list, attributes: int):
        self._x = x
        self._y = y
        self._tiles = tiles
        self._attributes = attributes

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def get_tiles(self) -> list:
        return self._tiles

    def get_attributes_byte(self) -> int:
        return self._attributes

    def get_flip_y(self) -> bool:
        return self._attributes & 0x40 > 0

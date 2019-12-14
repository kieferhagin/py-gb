import pytest

from gameboy.gpu.gpu_sprite import GPUSprite


@pytest.fixture()
def gpu_sprite_fixture() -> GPUSprite:
    return GPUSprite(x=0, y=0, pixels=[0, 0], attributes=0)


def test_gpu_sprite_get_x(gpu_sprite_fixture):
    gpu_sprite_fixture._x = 1

    assert gpu_sprite_fixture.get_x() == 1


def test_gpu_sprite_get_y(gpu_sprite_fixture):
    gpu_sprite_fixture._y = 1

    assert gpu_sprite_fixture.get_y() == 1


def test_gpu_sprite_get_pixels(gpu_sprite_fixture):
    gpu_sprite_fixture._pixels = [1, 2]

    assert gpu_sprite_fixture.get_pixels() == [1, 2]


def test_gpu_sprite_get_attributes_byte(gpu_sprite_fixture):
    gpu_sprite_fixture._attributes = 1

    assert gpu_sprite_fixture.get_attributes_byte() == 1


def test_gpu_sprite_get_flip_y(gpu_sprite_fixture):
    gpu_sprite_fixture._attributes = 0b01000000

    assert gpu_sprite_fixture.get_flip_y()

    gpu_sprite_fixture._attributes = 0b00000000

    assert not gpu_sprite_fixture.get_flip_y()

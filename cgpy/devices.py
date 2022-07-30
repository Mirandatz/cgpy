import dataclasses

from cgpy.colors import Color, ColorId
from cgpy.universes import NormalizedPoint2D


@dataclasses.dataclass
class DevicePoint:
    x: int
    y: int

    def __post_init__(self) -> None:
        assert self.x >= 0
        assert self.y >= 0


class Device:
    def __init__(
        self,
        height: int,
        width: int,
    ) -> None:
        assert height > 0
        assert width > 0

        self._height = height
        self._width = width
        self._buffer = [ColorId(0) for _ in range(width * height)]

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def __contains__(self, point: DevicePoint) -> bool:
        return point.x < self.width and point.y < self.height

    def set(self, x: int, y: int, color_id: ColorId) -> None:
        assert 0 <= x < self.width
        assert 0 <= y < self.height

        self._buffer[(y * self.width) + x] = color_id

    def get(self, x: int, y: int) -> ColorId:
        assert 0 <= x < self.width
        assert 0 <= y < self.height

        return self._buffer[(y * self.width) + x]


@dataclasses.dataclass(frozen=True, slots=True)
class Viewport:
    lower_left: DevicePoint
    upper_right: DevicePoint
    device: Device

    def __post_init__(self) -> None:
        assert self.lower_left.x < self.upper_right.x
        assert self.lower_left.y < self.upper_right.y
        assert self.lower_left in self.device
        assert self.upper_right in self.device

    def __contains__(self, pt: DevicePoint) -> bool:
        return (
            pt.x > self.lower_left.x
            and pt.x < self.upper_right.x
            and pt.y > self.lower_left.y
            and pt.y < self.upper_right.y
        )

    def set(self, x: int, y: int, color_id: ColorId) -> None:
        assert DevicePoint(x, y) in self
        self.device.set(x, y, color_id)

    def get(self, x: int, y: int) -> ColorId:
        assert DevicePoint(x, y) in self
        return self.device.get(x, y)


def create_device_with_max_size() -> Device:
    import pygame

    pygame.init()

    info = pygame.display.Info()
    return Device(height=info.current_h, width=info.current_w)


def normalized_point2d_to_device_point(
    pt: NormalizedPoint2D,
    port: Viewport,
) -> DevicePoint:
    raise NotImplementedError()


def draw_line_bresenham(
    pt0: DevicePoint,
    pt1: DevicePoint,
    color_id: ColorId,
    port: Viewport,
) -> None:
    raise NotImplementedError()


def fill_scanline(
    polygon: list[NormalizedPoint2D],
    color_id: ColorId,
    port: Viewport,
) -> None:
    raise NotImplementedError()


def fill_floodfill(
    polygon: list[NormalizedPoint2D],
    seed: DevicePoint,
    color_id: ColorId,
    port: Viewport,
) -> None:
    raise NotImplementedError()


def show_device(
    device: Device,
    palette: list[Color],
    close_after_seconds: int = 2,
) -> None:
    assert close_after_seconds > 0
    assert len(palette) > 0

    import pygame

    surface = pygame.display.set_mode((device.width, device.height), pygame.NOFRAME)

    pixel_array = pygame.PixelArray(surface)

    for y in range(device.height):
        for x in range(device.width):
            color_id = device.get(x, y)
            assert color_id >= 0
            r_g_b = palette[color_id].as_rgb_ints()
            pixel_array[x, y] = r_g_b  # type: ignore
    pixel_array.close()

    pygame.display.flip()
    clock = pygame.time.Clock()
    for _ in range(close_after_seconds):
        clock.tick(1)

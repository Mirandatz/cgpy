import dataclasses

import cgpy.colors as colors


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
        self._buffer = [0 for _ in range(width * height)]

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def set(self, x: int, y: int, color_id: int) -> None:
        assert 0 <= x < self.width
        assert 0 <= y < self.height

        self._buffer[y * self.width + x] = color_id

    def get(self, x: int, y: int) -> int:
        assert 0 <= x < self.width
        assert 0 <= y < self.height

        return self._buffer[y * self.width + x]

    def __contains__(self, point: DevicePoint) -> bool:
        return point.x < self.width and point.y < self.height


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


def create_device_with_max_size() -> Device:
    import pygame

    pygame.init()

    info = pygame.display.Info()
    return Device(height=info.current_h, width=info.current_w)


def show_device(
    device: Device,
    palette: list[colors.Color],
    close_after_seconds: int = 2,
) -> None:
    assert close_after_seconds > 0
    assert len(palette) > 0

    import pygame

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    dat_pink = (255, 0, 255)
    screen.fill(dat_pink)

    y_offset = int((screen.get_height() - device.height) / 2)
    x_offset = int((screen.get_width() - device.width) / 2)

    if y_offset < 0 or x_offset < 0:
        raise ValueError("pow, seu 'device' é maior que a tela real do computador :(")

    surface = screen.subsurface(
        (x_offset, y_offset),
        (device.width, device.height),
    )

    for y in range(device.height):
        for x in range(device.width):
            color_id = device.get(x, y)
            assert color_id >= 0
            r_g_b = palette[color_id].as_rgb_ints()

            surface.set_at((x, y), r_g_b)

    pygame.display.flip()
    clock = pygame.time.Clock()
    for _ in range(close_after_seconds):
        clock.tick(1)

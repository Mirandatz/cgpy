import dataclasses
import typing

import numpy as np
import numpy.typing as npt

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
        num_rows: int,
        num_columns: int,
    ) -> None:
        assert num_columns > 0
        assert num_rows > 0

        self._num_rows = num_rows
        self._num_columns = num_columns
        self._buffer: npt.NDArray[np.float32] = np.zeros(
            shape=(num_rows, num_columns),
            dtype=colors.ColorId,
        )

    @property
    def num_rows(self) -> int:
        return self._num_rows

    @property
    def num_columns(self) -> int:
        return self._num_columns

    @property
    def raw_buffer(self) -> npt.NDArray[colors.ColorId]:
        return self._buffer

    def __contains__(self, point: DevicePoint) -> bool:
        return point.x < self.num_columns and point.y < self.num_rows

    def set(self, x: int, y: int, color_id: colors.ColorId) -> None:
        assert 0 <= x < self.num_columns
        assert 0 <= y < self.num_rows

        self._buffer[y, x] = color_id

    def get(self, x: int, y: int) -> colors.ColorId:
        assert 0 <= x < self.num_columns
        assert 0 <= y < self.num_rows

        return self._buffer[y, x]  # type: ignore


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

    def set(self, x: int, y: int, color_id: colors.ColorId) -> None:
        assert DevicePoint(x, y) in self
        self.device.set(x, y, color_id)

    def get(self, x: int, y: int) -> colors.ColorId:
        assert DevicePoint(x, y) in self
        return self.device.get(x, y)


def create_device_with_max_size() -> Device:
    import pygame

    pygame.init()

    info = pygame.display.Info()
    return Device(num_columns=info.current_h, num_rows=info.current_w)


# def normalized_point2d_to_device_point(
#     pt: NormalizedPoint2D,
#     port: Viewport,
# ) -> DevicePoint:
#     raise NotImplementedError()


def draw_line_bresenham(
    pt0: DevicePoint,
    pt1: DevicePoint,
    color_id: colors.ColorId,
    port: Viewport,
) -> None:
    raise NotImplementedError()


# def fill_scanline(
#     polygon: list[NormalizedPoint2D],
#     color_id: colors.ColorId,
#     port: Viewport,
# ) -> None:
#     raise NotImplementedError()


# def fill_floodfill(
#     polygon: list[NormalizedPoint2D],
#     seed: DevicePoint,
#     color_id: colors.ColorId,
#     port: Viewport,
# ) -> None:
#     raise NotImplementedError()


def show_device(
    device: Device,
    palette: list[colors.Color],
    close_after_milliseconds: int = 2000,
) -> None:
    assert close_after_milliseconds > 0
    assert len(palette) > 0

    # validating 'color_ids'
    if np.min(device.raw_buffer) < 0 or np.max(device.raw_buffer) >= len(palette):
        raise ValueError("dispositivo contem `ColorId`s fora da `palette`")

    import pygame

    screen = pygame.display.set_mode(
        (device.num_rows, device.num_columns), pygame.NOFRAME
    )

    # decoding "float colors" to "byte colors"
    red_palette = np.asarray([colors.extract_red_channel(c) for c in palette]).flatten()  # type: ignore
    green_palette = np.asarray([colors.extract_green_channel(c) for c in palette]).flatten()  # type: ignore
    blue_palette = np.asarray([colors.extract_blue_channel(c) for c in palette]).flatten()  # type: ignore

    flattened_buffer: npt.NDArray[np.float32] = device.raw_buffer.flatten()

    red_buffer = red_palette[flattened_buffer].reshape(
        device.num_rows, device.num_columns
    )
    green_buffer = green_palette[flattened_buffer].reshape(
        device.num_rows, device.num_columns
    )
    blue_buffer = blue_palette[flattened_buffer].reshape(
        device.num_rows, device.num_columns
    )

    # creating surface arrray
    pixel_array = np.stack((red_buffer, green_buffer, blue_buffer), axis=-1).astype(np.uint8)  # type: ignore

    surface = pygame.surfarray.make_surface(pixel_array)

    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock = pygame.time.Clock()
    for _ in range(close_after_milliseconds):
        clock.tick(1000)

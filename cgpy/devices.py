import dataclasses
import pathlib

import numpy as np
import numpy.typing as npt
import pygame

import cgpy.colors as cc
import cgpy.universes as cu


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

        self._buffer: npt.NDArray[cc.ColorId] = np.zeros(
            shape=(num_rows, num_columns),
            dtype=cc.ColorId,
        )

    @property
    def num_rows(self) -> int:
        return self._buffer.shape[0]

    @property
    def num_columns(self) -> int:
        return self._buffer.shape[1]

    @property
    def raw_buffer(self) -> npt.NDArray[cc.ColorId]:
        return self._buffer

    def __repr__(self) -> str:
        return f"rows={self.num_rows}, columns={self.num_columns}"

    def __contains__(self, point: DevicePoint) -> bool:
        return point.x < self.num_columns and point.y < self.num_rows

    def set(self, x: int, y: int, color_id: cc.ColorId) -> None:
        assert 0 <= x < self.num_columns
        assert 0 <= y < self.num_rows

        self._buffer[y, x] = color_id

    def get(self, x: int, y: int) -> cc.ColorId:
        assert 0 <= x < self.num_columns
        assert 0 <= y < self.num_rows

        return self._buffer[y, x]  # type: ignore


@dataclasses.dataclass(frozen=True, slots=True)
class Viewport:
    lower_left: DevicePoint
    num_rows: int
    num_columns: int
    device: Device

    def __post_init__(self) -> None:
        assert self.num_rows >= 1
        assert self.num_columns >= 1
        assert self.lower_left in self.device

        inclusive_upper_right = DevicePoint(
            x=self.exclusive_right - 1,
            y=self.exclusive_top - 1,
        )
        assert inclusive_upper_right in self.device

    @property
    def inclusive_left(self) -> int:
        return self.lower_left.x

    @property
    def exclusive_top(self) -> int:
        return self.lower_left.y + self.num_rows

    @property
    def exclusive_right(self) -> int:
        return self.lower_left.x + self.num_columns

    @property
    def inclusive_bottom(self) -> int:
        return self.lower_left.y

    def __contains__(self, pt: DevicePoint) -> bool:
        return (
            self.inclusive_left <= pt.x < self.exclusive_right
            and self.inclusive_bottom <= pt.y < self.exclusive_top
        )

    def __repr__(self) -> str:
        return f"x={self.lower_left.x}, y={self.lower_left.y}, rows={self.num_rows}, columns={self.num_columns}"

    def set(self, x: int, y: int, color_id: cc.ColorId) -> None:
        assert DevicePoint(x, y) in self
        self.device.set(x, y, color_id)

    def get(self, x: int, y: int) -> cc.ColorId:
        assert DevicePoint(x, y) in self
        return self.device.get(x, y)


def create_device_with_max_size() -> Device:
    import pygame

    pygame.init()

    info = pygame.display.Info()
    return Device(num_columns=info.current_h, num_rows=info.current_w)


def normalized_point_to_device_point(
    pt: cu.NormalizedPoint2D, port: Viewport
) -> DevicePoint:
    column_range = port.num_columns - 1
    row_range = port.num_rows - 1

    x_offset = int(pt.x * column_range)
    y_offset = int(pt.y * row_range)

    return DevicePoint(x=port.lower_left.x + x_offset, y=port.lower_left.y + y_offset)


def _draw_vertical_line(
    pt0: DevicePoint, pt1: DevicePoint, color_id: cc.ColorId, port: Viewport
) -> None:
    assert pt0 in port
    assert pt1 in port
    assert pt0.x == pt1.x

    x = pt0.x
    for y in range(min(pt0.y, pt1.y), max(pt0.y, pt1.y) + 1):
        port.set(x=x, y=y, color_id=color_id)


def draw_line_bresenham(
    pt0: DevicePoint,
    pt1: DevicePoint,
    color_id: cc.ColorId,
    port: Viewport,
) -> None:
    assert pt0 in port
    assert pt1 in port

    if pt0 == pt1:
        port.set(pt0.x, pt0.y, color_id)
        return

    if pt0.x == pt1.x:
        _draw_vertical_line(pt0, pt1, color_id, port)
        return

    x_inc = 1 if pt0.x < pt1.x else -1
    y_inc = 1 if pt0.y < pt1.y else -1

    delta_x = abs(pt1.x - pt0.x)
    delta_y = abs(pt1.y - pt0.y)

    error = int(delta_x if delta_x > delta_y else (-delta_y / 2))

    x = pt0.x
    y = pt0.y
    while x != pt1.x and y != pt1.y:
        port.set(x=x, y=y, color_id=color_id)

        previous_error = error
        if previous_error > -delta_x:
            error -= delta_y
            x += x_inc

        if previous_error < delta_y:
            error += delta_x
            y += y_inc


def _device_to_surface(
    device: Device,
    palette: list[cc.Color],
) -> pygame.surface.Surface:
    assert len(palette) > 0

    # validating 'color_ids'
    if np.min(device.raw_buffer) < 0 or np.max(device.raw_buffer) >= len(palette):
        raise ValueError("dispositivo contem `ColorId`s fora da `palette`")

    # decoding "float colors" to "byte colors"
    red_palette = np.asarray([cc.extract_red_channel(c) for c in palette]).flatten()
    green_palette = np.asarray([cc.extract_green_channel(c) for c in palette]).flatten()
    blue_palette = np.asarray([cc.extract_blue_channel(c) for c in palette]).flatten()

    tranposed_buffer = device.raw_buffer.transpose()
    flattened_buffer: npt.NDArray[cc.ColorId] = tranposed_buffer.flatten()

    red_buffer = red_palette[flattened_buffer].reshape(tranposed_buffer.shape)
    green_buffer = green_palette[flattened_buffer].reshape(tranposed_buffer.shape)
    blue_buffer = blue_palette[flattened_buffer].reshape(tranposed_buffer.shape)

    pixel_array = np.stack((red_buffer, green_buffer, blue_buffer), axis=-1).astype(
        np.uint8
    )

    # place origin on the bottom-left part of the screen
    mirrored_array = np.flip(pixel_array, axis=1)

    surface = pygame.surfarray.make_surface(mirrored_array)
    return surface


def device_to_png(device: Device, palette: list[cc.Color], path: pathlib.Path) -> None:
    assert len(palette) > 0
    surface = _device_to_surface(device, palette)
    pygame.image.save(surface, path)


def show_device(
    device: Device,
    palette: list[cc.Color],
    close_after_milliseconds: int = 2000,
) -> None:
    assert close_after_milliseconds > 0
    assert len(palette) > 0

    screen = pygame.display.set_mode(
        (device.num_columns, device.num_rows), pygame.NOFRAME
    )

    surface = _device_to_surface(device, palette)

    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock = pygame.time.Clock()
    for _ in range(close_after_milliseconds):
        clock.tick(1000)

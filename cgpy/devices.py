import dataclasses
import itertools
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

    @property
    def buffer_view(self) -> npt.NDArray[cc.ColorId]:
        buffer = self.device.raw_buffer
        return buffer[
            self.inclusive_bottom : self.exclusive_top,
            self.inclusive_left : self.exclusive_right,
        ]

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


def make_viewport_from_corners(
    pt0: DevicePoint,
    pt1: DevicePoint,
    device: Device,
) -> Viewport:
    assert pt0 in device
    assert pt1 in device

    lower_left = DevicePoint(x=min(pt0.x, pt1.x), y=min(pt0.y, pt1.y))
    num_columns = abs(pt1.x - pt0.x) + 1
    num_rows = abs(pt1.y - pt0.y) + 1

    return Viewport(
        lower_left=lower_left, num_rows=num_rows, num_columns=num_columns, device=device
    )


def normalized_point_to_device_point(
    pt: cu.NormalizedPoint2D, port: Viewport
) -> DevicePoint:
    column_range = port.num_columns - 1
    row_range = port.num_rows - 1

    x_offset = int(pt.x * column_range)
    y_offset = int(pt.y * row_range)

    return DevicePoint(x=port.lower_left.x + x_offset, y=port.lower_left.y + y_offset)


def draw_viewport(port: Viewport, color_id: cc.ColorId) -> None:
    for x in range(0, port.num_columns):
        port.set(x=x, y=port.inclusive_bottom, color_id=color_id)
        port.set(x=x, y=port.exclusive_top - 1, color_id=color_id)
    for y in range(0, port.num_rows):
        port.set(x=port.inclusive_left, y=y, color_id=color_id)
        port.set(x=port.exclusive_right - 1, y=y, color_id=color_id)


def draw_line_bresenham(
    pt0: DevicePoint,
    pt1: DevicePoint,
    color_id: cc.ColorId,
    port: Viewport,
) -> None:
    # based on:
    # http://www.roguebasin.com/index.php/Bresenham%27s_Line_Algorithm#Python

    x0 = pt0.x
    y0 = pt0.y
    x1 = pt1.x
    y1 = pt1.y
    dx = x1 - x0
    dy = y1 - y0

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    # Recalculate differentials
    dx = x1 - x0
    dy = y1 - y0

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y0 < y1 else -1

    # Iterate over bounding box generating points between start and end
    y = y0
    for x in range(x0, x1 + 1):
        if is_steep:
            port.set(x=y, y=x, color_id=color_id)
        else:
            port.set(x=x, y=y, color_id=color_id)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx


def draw_polygon(
    poly: list[cu.NormalizedPoint2D], port: Viewport, color_id: cc.ColorId
) -> None:
    assert len(poly) >= 2

    connected = itertools.chain(poly, [poly[0]])
    for a, b in itertools.pairwise(connected):
        dev_a = normalized_point_to_device_point(a, port)
        dev_b = normalized_point_to_device_point(b, port)
        draw_line_bresenham(dev_a, dev_b, color_id, port)


def _flood_fill(
    seed: DevicePoint,
    new_color: cc.ColorId,
    border_color: cc.ColorId,
    buffer: npt.NDArray[cc.ColorId],
) -> None:

    to_visit = [(seed.x, seed.y)]
    height, width = buffer.shape

    while to_visit:
        x, y = to_visit.pop()

        if not (0 < x < width):
            continue
        if not (0 < y < height):
            continue
        if buffer[y, x] in (new_color, border_color):
            continue

        buffer[y, x] = new_color
        to_visit.append((x - 1, y))
        to_visit.append((x + 1, y))
        to_visit.append((x, y - 1))
        to_visit.append((x, y + 1))


def fill_polygon_flood(
    poly: list[cu.NormalizedPoint2D],
    seed: cu.NormalizedPoint2D,
    color_id: cc.ColorId,
    port: Viewport,
) -> None:
    fake_color = cc.ColorId(-1)
    draw_polygon(poly, port, fake_color)

    buffer = port.buffer_view
    device_seed = normalized_point_to_device_point(seed, port)
    _flood_fill(
        device_seed,
        new_color=fake_color,
        border_color=fake_color,
        buffer=buffer,
    )

    buffer[buffer == fake_color] = color_id


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

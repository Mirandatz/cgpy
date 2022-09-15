import numba
import numpy as np
import numpy.typing as npt

import cgpy.colors as cc
import cgpy.universes_mk2 as cu_mk2

# Shape = (a, b, c), dtype = np.int32
# a = number of line of  segments
# b = 2 = number of points in line segment = `start` and `end`
# c = 2 = number of coordinates in point = `x` and `y`
DevicePolygon = npt.NDArray[np.int32]

# Shape = (num_rows, num_columns), dtype = cc.ColorID
DeviceBuffer = npt.NDArray[cc.ColorId]


@numba.njit(fastmath=True)  # type: ignore
def validate_device_polygon(polygon: DevicePolygon) -> None:
    n_line_segments, points_per_line_segment, coords_per_point = polygon.shape
    assert points_per_line_segment == 2
    assert coords_per_point == 2
    assert polygon.dtype == np.int32
    x_values = polygon[:, :, 0]
    y_values = polygon[:, :, 1]
    assert np.all(x_values >= 0)
    assert np.all(y_values >= 0)


@numba.njit(fastmath=True)  # type: ignore
def validate_device_buffer(buffer: DeviceBuffer) -> None:
    n_rows, n_cols = buffer.shape
    assert n_rows >= 1
    assert n_cols >= 1
    assert buffer.dtype == cc.ColorId


@numba.njit(fastmath=True)  # type: ignore
def validate_device_polygon_and_buffer(
    polygon: DevicePolygon,
    buffer: DeviceBuffer,
) -> None:
    validate_device_polygon(polygon)
    validate_device_buffer(buffer)

    x_values = polygon[:, :, 0]
    y_values = polygon[:, :, 1]

    device_rows, device_columns = buffer.shape
    assert np.all(x_values < device_columns)
    assert np.all(y_values < device_rows)


@numba.njit(fastmath=True)  # type: ignore
def draw_line(
    x0: int,
    y0: int,
    x1: int,
    y1: int,
    color_id: cc.ColorId,
    buffer: DeviceBuffer,
) -> None:
    # based on:
    # http://www.roguebasin.com/index.php/Bresenham%27s_Line_Algorithm#Python

    num_rows, num_columns = buffer.shape
    assert 0 <= x0 <= num_columns
    assert 0 <= x1 <= num_columns
    assert 0 <= y0 <= num_rows
    assert 0 <= y1 <= num_rows

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
            buffer[x, y] = color_id
        else:
            buffer[y, x] = color_id

        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx


@numba.njit(fastmath=True)  # type: ignore
def normalized_object2d_to_device_polygon(
    obj: cu_mk2.NormalizedObject2D,
    num_rows: int,
    num_columns: int,
) -> DevicePolygon:
    cu_mk2.validate_normalized_object2d(obj)

    assert num_rows >= 1
    assert num_columns >= 1

    n_line_segments = obj.shape[0]
    result = np.empty(shape=(n_line_segments, 2, 2), dtype=np.int32)
    result[:, :, 0] = obj[:, :, 0] * num_columns
    result[:, :, 1] = obj[:, :, 1] * num_rows
    return result


@numba.njit(fastmath=True)  # type: ignore
def draw_object2d(
    poly: cu_mk2.NormalizedObject2D,
    port: DeviceBuffer,
    color_id: cc.ColorId,
) -> None:
    # TODO: add some validation

    num_rows, num_columns = port.shape
    device_coords = normalized_object2d_to_device_polygon(
        poly,
        num_rows=num_rows,
        num_columns=num_columns,
    )

    n_segments = device_coords.shape[0]

    for line_segment in range(n_segments):
        start = device_coords[line_segment, 0, :]
        end = device_coords[line_segment, 1, :]
        draw_line(
            x0=start[0],
            y0=start[1],
            x1=end[0],
            y1=end[1],
            color_id=color_id,
            buffer=port,
        )

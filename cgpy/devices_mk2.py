import numba
import numpy as np
import numpy.typing as npt

import cgpy.colors as cc

Polygon = npt.NDArray[np.float32]
NormalizedPolygon = npt.NDArray[np.float32]
DevicePolygon = npt.NDArray[np.int32]
DeviceBuffer = npt.NDArray[cc.ColorId]


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
def normalized_points_to_device_points(
    poly: NormalizedPolygon,
    num_rows: int,
    num_columns: int,
) -> npt.NDArray[np.int32]:
    assert num_rows >= 1
    assert num_columns >= 1

    n_points, n_dimensions = poly.shape

    # ensure working in 2d + homogeneous coord
    assert n_dimensions == 3

    # ensure no homoegenous coord is valid
    assert np.all(poly[:, 2] != 0)

    # remove homogenous coord
    poly_x = poly[:, 0] / poly[:, 2]
    poly_y = poly[:, 1] / poly[:, 2]

    result = np.empty_like(poly, dtype=np.int32)
    result[:, 0] = poly_x * num_columns
    result[:, 1] = poly_y * num_rows
    return result


@numba.njit(fastmath=True)  # type: ignore
def draw_polygon(
    poly: NormalizedPolygon,
    port: DeviceBuffer,
    color_id: cc.ColorId,
) -> None:
    n_points, n_dimensions = poly.shape
    assert n_points >= 2  # working with at least a line segment
    assert n_dimensions == 3  # working in 2d + homogeneous

    num_rows, num_columns = port.shape
    device_coords = normalized_points_to_device_points(
        poly,
        num_rows=num_rows,
        num_columns=num_columns,
    )

    for i in numba.prange(n_points - 1):
        draw_line(
            x0=device_coords[i][0],
            y0=device_coords[i][1],
            x1=device_coords[i + 1][0],
            y1=device_coords[i + 1, 1],
            color_id=color_id,
            buffer=port,
        )

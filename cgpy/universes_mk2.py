import numba
import numpy as np
import numpy.typing as npt

Polygon = npt.NDArray[np.float32]
NormalizedPolygon = npt.NDArray[np.float32]


@numba.njit(fastmath=True)  # type: ignore
def check_if_2d_with_homogeneous_coordinates(polygon: Polygon) -> None:
    _, num_dimensions = polygon.shape

    # 2d + homogeneous
    assert num_dimensions == 3

    # valid homogenous values
    assert np.all(polygon[:, 2] != 0)


@numba.njit(fastmath=True)  # type: ignore
def normalize_polygon(
    polygon: Polygon,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
) -> NormalizedPolygon:
    check_if_2d_with_homogeneous_coordinates(polygon)

    assert x_min < x_max
    assert y_min < y_max

    x_values = polygon[:, 0]
    assert np.all(x_min <= x_values)
    assert np.all(x_max >= x_values)

    y_values = polygon[:, 1]
    assert np.all(y_min <= y_values)
    assert np.all(y_max >= y_values)

    delta_x = x_max - x_min
    delta_y = y_max - y_min

    result = np.empty_like(polygon)
    result[:, 0] = (polygon[:, 0] - x_min) / delta_x
    result[:, 1] = (polygon[:, 1] - y_min) / delta_y
    result[:, 2] = polygon[:, 2]

    return result

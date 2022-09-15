import numba
import numpy as np
import numpy.typing as npt
from numba.typed import List as NumbaList

import cgpy.universes as cu

# Shape = (a, b, c), dtype = np.float
# a = number of line of  segments
# b = 2 = number of points in line segment = `start` and `end`
# c = 3 = number of coordinates in point = `x`, `y`, and `w`
Object2D = npt.NDArray[np.float32]

# Shape = (a, b, c), dtype = np.float
# a = number of line of  segments
# b = 2 = number of points in line segment = `start` and `end`
# c = 2 = number of coordinates in point = `x` and `y`
NormalizedObject2D = npt.NDArray[np.float32]

# Shape = (a, b, c), dtype = np.float
# a = number of line of  segments
# b = 2 = number of points in line segment = `start` and `end`
# c = 4 = number of coordinates in point = `x`, `y`, `z` and `w`
Object3D = npt.NDArray[np.float32]


@numba.njit(fastmath=True)  # type: ignore
def validate_object2d(obj: Object2D) -> None:
    line_segments, points_per_line_segment, coords_per_point = obj.shape
    assert points_per_line_segment == 2
    assert coords_per_point == 3

    # type check does not work with njit
    # assert obj.dtype == np.dtype(np.float32)

    assert np.all(np.isfinite(obj))

    w_values = obj[:, :, 2]
    assert np.all(w_values != 0)


@numba.njit(fastmath=True)  # type: ignore
def validate_normalized_object2d(obj: NormalizedObject2D) -> None:
    line_segments, points_per_line_segment, coords_per_point = obj.shape
    assert points_per_line_segment == 2
    assert coords_per_point == 2

    # type check does not work with njit
    # assert obj.dtype == np.float32
    assert np.all(obj >= 0) and np.all(obj <= 1)


@numba.njit(fastmath=True)  # type: ignore
def normalize_object2d_naive(
    obj: Object2D,
    x_min: float,
    y_min: float,
    x_max: float,
    y_max: float,
) -> NormalizedObject2D:
    """
    Naive normalization function that only accepts points that are inside the window
    defined by `x_min`, `x_max`, `y_min`, and `y_max`.
    """
    validate_object2d(obj)

    assert x_min < x_max
    assert y_min < y_max

    delta_x = x_max - x_min
    delta_y = y_max - y_min

    # remove homo
    homo = obj[:, :, 2]
    x_no_homo = obj[:, :, 0] / homo
    y_no_homo = obj[:, :, 1] / homo

    # because we are normalizing values in naive way
    assert np.all(x_min <= x_no_homo) and np.all(x_no_homo <= x_max)
    assert np.all(y_min <= y_no_homo) and np.all(y_no_homo <= y_max)

    # normalize x and y
    num_line_segments = obj.shape[0]
    result = np.empty(shape=(num_line_segments, 2, 2), dtype=np.float32)
    result[:, :, 0] = (x_no_homo - x_min) / delta_x
    result[:, :, 1] = (y_no_homo - y_min) / delta_y

    return result


@numba.njit(fastmath=True)  # type: ignore
def old_polygon_to_line_segments(polygon: cu.Polygon) -> Object2D:
    assert len(polygon) >= 2

    num_points = len(polygon)
    num_line_segments = num_points - 1
    result = np.empty(shape=(num_line_segments, 2, 3), dtype=np.float32)

    for i in range(num_line_segments):
        result[i, 0, :] = polygon[i].flatten()
        result[i, 1, :] = polygon[i + 1].flatten()

    return result


def old_object2d_to_new_object2d(obj: cu.Object2D) -> Object2D:
    line_segments = [old_polygon_to_line_segments(NumbaList(p)) for p in obj]
    return np.concatenate(line_segments, axis=0, dtype=np.float32)

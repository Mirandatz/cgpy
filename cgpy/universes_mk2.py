import math

import numba
import numpy as np
import numpy.typing as npt
from numba.experimental import jitclass
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


Vector4 = npt.NDArray[np.float32]
Matrix3x3 = npt.NDArray[np.float32]
Matrix4x4 = npt.NDArray[np.float32]


@jitclass
class Window:
    _min_x: float
    _min_y: float
    _max_x: float
    _max_y: float

    def __init__(
        self,
        lower_left: tuple[float, float],
        upper_right: tuple[float, float],
    ) -> None:
        min_x, min_y = lower_left
        max_x, max_y = upper_right
        assert math.isfinite(min_x)
        assert math.isfinite(min_y)
        assert math.isfinite(max_x)
        assert math.isfinite(max_y)

        assert min_x < max_x
        assert min_y < max_y

        self._min_x = min_x
        self._min_y = min_y
        self._max_x = max_x
        self._max_y = max_y

    @property
    def min_x(self) -> float:
        return self._min_x

    @property
    def min_y(self) -> float:
        return self._min_y

    @property
    def max_x(self) -> float:
        return self._max_x

    @property
    def max_y(self) -> float:
        return self._max_y


@numba.njit(fastmath=True, cache=True)  # type: ignore
def validate_object2d(obj: Object2D) -> None:
    line_segments, points_per_line_segment, coords_per_point = obj.shape
    assert points_per_line_segment == 2
    assert coords_per_point == 3

    # type check does not work with njit
    # assert obj.dtype == np.dtype(np.float32)

    assert np.all(np.isfinite(obj))

    w_values = obj[:, :, 2]
    assert np.all(w_values != 0)


@numba.njit(fastmath=True, cache=True)  # type: ignore
def validate_normalized_object2d(obj: NormalizedObject2D) -> None:
    line_segments, points_per_line_segment, coords_per_point = obj.shape
    assert points_per_line_segment == 2
    assert coords_per_point == 2

    # type check does not work with njit
    # assert obj.dtype == np.float32
    assert np.all(obj >= 0) and np.all(obj <= 1)


@numba.njit(fastmath=True, cache=True)  # type: ignore
def validate_object3d(obj: Object3D) -> None:
    line_segments, points_per_line_segment, coords_per_point = obj.shape
    assert points_per_line_segment == 2
    assert coords_per_point == 4

    # type check does not work with njit
    # assert obj.dtype == np.dtype(np.float32)

    assert np.all(np.isfinite(obj))

    w_values = obj[:, :, 3]
    assert np.all(w_values != 0)


@numba.njit(fastmath=True, cache=True)  # type: ignore
def validate_vector4(vec: Matrix3x3) -> None:
    assert vec.shape == (4,)
    assert np.all(np.isfinite(vec))


@numba.njit(fastmath=True, cache=True)  # type: ignore
def validate_matrix3x3(mat: Matrix3x3) -> None:
    assert mat.shape == (3, 3)
    assert np.all(np.isfinite(mat))


@numba.njit(fastmath=True, cache=True)  # type: ignore
def make_vector4(x: float, y: float, z: float) -> Vector4:
    vec = np.empty(shape=(4,), dtype=np.float32)
    vec[0] = x
    vec[1] = y
    vec[2] = z
    vec[3] = 1
    return vec


@numba.njit(fastmath=True, cache=True)  # type: ignore
def validate_matrix4x4(mat: Matrix3x3) -> None:
    assert mat.shape == (4, 4)
    assert np.all(np.isfinite(mat))


@numba.njit(parallel=True, fastmath=True, cache=True)  # type: ignore
def transform_object2d(obj: Object2D, trans: Matrix3x3) -> Object2D:
    validate_object2d(obj)
    validate_matrix3x3(trans)

    num_line_segments = obj.shape[0]

    result = np.empty_like(obj)

    for i in numba.prange(num_line_segments):  # type: ignore
        result[i, 0] = trans @ obj[i, 0]
        result[i, 1] = trans @ obj[i, 1]

    return result


@numba.njit(parallel=True, fastmath=True, cache=True)  # type: ignore
def transform_object3d(obj: Object3D, trans: Matrix4x4) -> Object2D:
    validate_object3d(obj)
    validate_matrix4x4(trans)

    num_line_segments = obj.shape[0]

    result = np.empty_like(obj)

    for i in numba.prange(num_line_segments):  # type: ignore
        result[i, 0] = trans @ obj[i, 0]
        result[i, 1] = trans @ obj[i, 1]

    return result


@numba.njit(fastmath=True, cache=True)  # type: ignore
def perspective_project_point(
    point: npt.NDArray[np.float32],
    zpp: float,
    zcp: float,
) -> npt.NDArray[np.float32]:
    projected = np.empty(shape=(3,), dtype=np.float32)
    projected[0] = point[0] * (zpp - zcp) / (point[2] - zcp)
    projected[1] = point[1] * (zpp - zcp) / (point[2] - zcp)
    projected[2] = 1

    return projected


@numba.njit(parallel=True, fastmath=True, cache=True)  # type: ignore
def perspective_project(obj: Object3D, zpp: float, zcp: float) -> Object2D:
    validate_object3d(obj)

    n_line_segments = obj.shape[0]
    projected = np.empty(shape=(n_line_segments, 2, 3), dtype=np.float32)

    n_faces = obj.shape[0]
    for i in numba.prange(n_faces):  # type: ignore
        projected[i, 0, :] = perspective_project_point(obj[i, 0], zpp, zcp)
        projected[i, 1, :] = perspective_project_point(obj[i, 1], zpp, zcp)

    return projected


@numba.njit(fastmath=True, cache=True)  # type: ignore
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


@numba.njit(fastmath=True, cache=True)  # type: ignore
def old_polygon_to_line_segments(polygon: cu.Polygon) -> Object2D:
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


@numba.njit(fastmath=True, cache=True)  # type: ignore
def old_face_to_line_segments(face: cu.Face) -> Object3D:
    num_points = len(face)
    num_line_segments = num_points - 1

    result = np.empty(shape=(num_line_segments, 2, 4), dtype=np.float32)

    for i in range(num_line_segments):
        result[i, 0, :] = face[i].flatten()
        result[i, 1, :] = face[i + 1].flatten()

    return result


def old_object3d_to_new_object3d(obj: cu.Object3D) -> Object3D:
    line_segments = [old_face_to_line_segments(NumbaList(f)) for f in obj]
    return np.concatenate(line_segments, axis=0, dtype=np.float32)


@numba.njit(fastmath=True, cache=True)  # type: ignore
def make_x_rotation_3d(degrees: float) -> Matrix4x4:
    radians = degrees * np.pi / 180
    matrix: Matrix4x4 = np.eye(4, 4, dtype=np.float32)

    matrix[1, 1] = np.cos(radians)
    matrix[1, 2] = -np.sin(radians)
    matrix[2, 1] = np.sin(radians)
    matrix[2, 2] = np.cos(radians)

    return matrix


@numba.njit(fastmath=True, cache=True)  # type: ignore
def make_versor(vec: Vector4) -> Vector4:
    """
    Retorna um vetor com mesma direção que `vec`,
    mas módulo=1 e coordenada homogenea=1.
    """

    direction = vec[:3]  # x, y, z
    norm = np.linalg.norm(direction)

    versor = np.empty(shape=(4,), dtype=np.float32)
    versor[:3] = direction / norm
    versor[3] = 1

    return versor


@numba.njit(fastmath=True, cache=True)  # type: ignore
def create_observer_transformation_matrix(
    normal: Vector4,
    up: Vector4,
    offset: Vector4,
) -> Matrix4x4:
    """
    Computa a matriz de mudança de base (4x4) para um observador
    descrito por `normal`, `up`, e `offset`.
    """
    validate_vector4(normal)
    validate_vector4(up)
    validate_vector4(offset)

    w = make_versor(normal)

    u = make_versor(
        np.cross(
            up[:3].flatten(),
            w[:3].flatten(),
        )
    )

    v = np.cross(
        w[:3].flatten(),
        u[:3].flatten(),
    )

    matrix: Matrix4x4 = np.empty(shape=(4, 4), dtype=np.float32)

    matrix[0, :3] = u[:3].flatten()
    matrix[0, 3] = offset[0]

    matrix[1, :3] = v[:3].flatten()
    matrix[1, 3] = offset[1]

    matrix[2, :3] = w[:3].flatten()
    matrix[2, 3] = offset[2]

    matrix[3, :3] = 0
    matrix[3, 3] = 1

    return matrix

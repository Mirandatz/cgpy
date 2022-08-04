import numpy as np
import numpy.typing as npt

import cgpy.universes as cu


def point2d_to_vector(pt: cu.Point2D) -> npt.NDArray[np.float32]:
    vector: npt.NDArray[np.float32] = np.ones(shape=(3, 1), dtype=np.float32)
    vector[0] = pt.x
    vector[1] = pt.y
    return vector


def vector3_to_point2d(vec: npt.NDArray[np.float32]) -> cu.Point2D:
    assert vec.shape == (3, 1)

    homogeneous = vec[2]
    assert homogeneous != 0

    rescaled = vec / homogeneous
    return cu.Point2D(x=rescaled[0, 0], y=rescaled[1, 0])


def make_translation(delta_x: float, delta_y: float) -> npt.NDArray[np.float32]:
    matrix: npt.NDArray[np.float32] = np.eye(3, 3, dtype=np.float32)
    matrix[0, 2] = delta_x
    matrix[1, 2] = delta_y
    return matrix


def make_counterclockwise_rotation(degrees: float) -> npt.NDArray[np.float32]:
    radians = degrees * np.pi / 180
    matrix: npt.NDArray[np.float32] = np.eye(3, 3, dtype=np.float32)
    matrix[0, 0] = np.cos(radians)
    matrix[0, 1] = -1 * np.sin(radians)
    matrix[1, 0] = np.sin(radians)
    matrix[1, 1] = np.cos(radians)
    return matrix


def make_scale(x_factor: float, y_factor: float) -> npt.NDArray[np.float32]:
    matrix: npt.NDArray[np.float32] = np.eye(3, 3, dtype=np.float32)
    matrix[0, 0] = x_factor
    matrix[1, 1] = y_factor
    return matrix


def transform_polygon2d(
    polygon: list[cu.Point2D],
    transformation: npt.NDArray[np.float32],
) -> list[cu.Point2D]:
    assert transformation.shape == (3, 3)

    vecs = (point2d_to_vector(pt) for pt in polygon)
    transformed_vecs = [transformation @ v for v in vecs]
    return [vector3_to_point2d(v) for v in transformed_vecs]

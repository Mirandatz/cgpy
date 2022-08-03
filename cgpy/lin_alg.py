import numpy as np
import numpy.typing as npt

import cgpy.universes as uni


def point2d_to_vector(pt: uni.Point2D) -> npt.NDArray[np.float32]:
    vector: npt.NDArray[np.float32] = np.ones(shape=(3, 1), dtype=np.float32)
    vector[0] = pt.x
    vector[1] = pt.y
    return vector


def vector3_to_point2d(vec: npt.NDArray[np.float32]) -> uni.Point2D:
    assert vec.shape == (3, 1)

    homogeneous = vec[2]
    assert homogeneous != 0

    rescaled = vec / homogeneous
    return uni.Point2D(x=rescaled[0, 0], y=rescaled[1, 0])


def make_translation(delta_x: float, delta_y: float) -> npt.NDArray[np.float32]:
    matrix: npt.NDArray[np.float32] = np.zeros(shape=(3, 3), dtype=np.float32)

    matrix[0, 0] = 1
    matrix[1, 1] = 1
    matrix[2, 2] = 1

    matrix[0, 2] = delta_x
    matrix[1, 2] = delta_y

    return matrix


def make_counterclockwise_rotation(degrees: float) -> npt.NDArray[np.float32]:
    matrix = np.zeros(shape=(3, 3), dtype=np.float32)

    raise NotImplementedError()

    """
    SUBSTITUA O  `raise NotImplementedError()` PELA IMPLEMENTAÇÃO
    """

    return matrix


def make_scale(x_factor: float, y_factor: float) -> npt.NDArray[np.float32]:
    matrix = np.zeros(shape=(3, 3), dtype=np.float32)

    raise NotImplementedError()

    """
    SUBSTITUA O  `raise NotImplementedError()` PELA IMPLEMENTAÇÃO
    """

    return matrix

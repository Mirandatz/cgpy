import dataclasses
import typing

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]
Vector4 = FloatArray
Matrix4x4 = FloatArray

Face = list[Vector4]
Object3D = list[Face]


@dataclasses.dataclass(frozen=True, slots=True)
class Point2D:
    x: float
    y: float


@dataclasses.dataclass(frozen=True, slots=True)
class Window:
    lower_left: Point2D
    upper_right: Point2D

    def __post_init__(self) -> None:
        assert self.lower_left.x < self.upper_right.x
        assert self.lower_left.y < self.upper_right.y

    def __contains__(self, pt: Point2D) -> bool:
        return (
            self.lower_left.x <= pt.x <= self.upper_right.x
            and self.lower_left.y <= pt.y <= self.upper_right.y
        )

    @property
    def width(self) -> float:
        return self.upper_right.x - self.lower_left.x

    @property
    def height(self) -> float:
        return self.upper_right.y - self.lower_left.y


@dataclasses.dataclass(frozen=True, slots=True)
class NormalizedPoint2D:
    x: float
    y: float

    def __post_init__(self) -> None:
        assert 0 <= self.x <= 1
        assert 0 <= self.y <= 1


def _normalize_point_naive(pt: Point2D, win: Window) -> NormalizedPoint2D:
    assert pt in win

    return NormalizedPoint2D(
        x=(pt.x - win.lower_left.x) / win.width,
        y=(pt.y - win.lower_left.y) / win.height,
    )


def normalize_polygon(poly: list[Point2D], win: Window) -> list[NormalizedPoint2D]:
    return [_normalize_point_naive(p, win) for p in poly]


def make_vector4(x: float, y: float, z: float) -> Vector4:
    return np.asfarray((x, y, z, 1)).reshape(4, 1)


def validate_vector4(vec: typing.Any) -> None:
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (4, 1)
    assert vec.dtype == np.float64


def validate_matrix4(matrix: typing.Any) -> None:
    assert isinstance(matrix, np.ndarray)
    assert matrix.shape == (4, 4)
    assert matrix.dtype == np.float64


def make_versor(vec: npt.ArrayLike) -> Vector4:
    """
    Retorna um vetor com mesma direção que `vec`,
    mas módulo=1 e coordenada homogenea=1.
    """

    direction = np.asfarray(vec)[:3]  # x, y, z
    norm = np.linalg.norm(direction)

    versor = np.empty(shape=(4, 1))
    versor[:3] = (direction / norm).reshape((3, 1))
    versor[3] = 1

    return versor


def create_observer_transformation_matrix(
    normal: Vector4,
    up: Vector4,
    offset: Vector4,
) -> Matrix4x4:
    """
    Compute a matriz de mudança de base (4x4) para um observador
    com descrito por `normal`, `up`, e `offset`.
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

    matrix = np.empty(shape=(4, 4))

    matrix[0, :3] = u[:3].flatten()
    matrix[0, 3] = offset[0]

    matrix[1, :3] = v[:3].flatten()
    matrix[1, 3] = offset[1]

    matrix[2, :3] = w[:3].flatten()
    matrix[2, 3] = offset[2]

    matrix[3, :3] = 0
    matrix[3, 3] = 1

    return matrix


def transform_point3d(pt: Vector4, trans: Matrix4x4) -> Vector4:
    return trans @ pt


def transform_face(face: Face, trans: Matrix4x4) -> Face:
    return [transform_point3d(pt, trans) for pt in face]


def transform_object3d(
    obj: Object3D,
    trans: Matrix4x4,
) -> Object3D:
    return [transform_face(pt, trans) for pt in obj]


def main() -> None:
    matrix = create_observer_transformation_matrix(
        normal=make_vector4(0, 0, 1),
        up=make_vector4(0, 1, 0),
        offset=make_vector4(0, 0, 0),
    )
    print(matrix)


if __name__ == "__main__":
    main()

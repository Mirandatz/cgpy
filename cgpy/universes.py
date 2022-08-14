import dataclasses
import typing

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]

# 2d
Vector3 = typing.NewType("Vector3", FloatArray)
Matrix3x3 = typing.NewType("Matrix3x3", FloatArray)
Polygon = list[Vector3]
Object2D = list[Polygon]

NormalizedPoint = typing.NewType("NormalizedPoint", Vector3)

# 3d
Vector4 = typing.NewType("Vector4", FloatArray)
Matrix4x4 = typing.NewType("Matrix4x4", FloatArray)
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


def make_vector4(x: float, y: float, z: float) -> Vector4:
    vec = np.asfarray((x, y, z, 1)).reshape(4, 1)
    return Vector4(vec)


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

    return Vector4(versor)


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

    return Matrix4x4(matrix)


def transform_point3d(pt: Vector4, trans: Matrix4x4) -> Vector4:
    return Vector4(trans @ pt)


def transform_face(face: Face, trans: Matrix4x4) -> Face:
    return [transform_point3d(pt, trans) for pt in face]


def transform_object3d(
    obj: Object3D,
    trans: Matrix4x4,
) -> Object3D:
    return [transform_face(pt, trans) for pt in obj]


def perspective_project_point(
    pt: Vector4,
    zpp: float,
    zcp: float,
) -> Vector4:
    validate_vector4(pt)
    projected: Vector4 = pt * (zpp - zcp) / (pt[2, 0] - zcp)
    projected[2] = zpp
    projected[3] = 1

    return projected


def perspective_project_face(
    face: Face,
    zpp: float,
    zcp: float,
) -> Face:
    return [perspective_project_point(pt, zpp=zpp, zcp=zcp) for pt in face]


def perspective_project_object(obj: Object3D, zpp: float, zcp: float) -> Object3D:
    return [perspective_project_face(f, zpp=zpp, zcp=zcp) for f in obj]


def face_to_polygon(face: Face) -> Polygon:
    poly = []

    for vec4 in face:
        validate_vector4(vec4)
        poly.append(
            make_vector3(
                x=vec4[0],
                y=vec4[1],
            )
        )

    return poly


def object3d_to_object2d(obj: Object3D) -> Object2D:
    return [face_to_polygon(f) for f in obj]


def make_vector3(x: float, y: float) -> Vector3:
    vec = np.asfarray((x, y, 1)).reshape(3, 1)
    return Vector3(vec)


def validate_vector3(vec: Vector3) -> None:
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (3, 1)
    assert vec.dtype == np.float64


def normalize_vector3_naive(pt: Vector3, win: Window) -> Vector3:
    validate_vector3(pt)

    x = pt[0]
    y = pt[1]

    return make_vector3(
        x=(x - win.lower_left.x) / win.width,
        y=(y - win.lower_left.y) / win.height,
    )


def validate_normalized_point(pt: Vector3) -> None:
    validate_vector3(pt)

    assert ((0 <= pt) & (pt <= 1)).all()


def normalize_polygon2(poly: Polygon, win: Window) -> Polygon:
    return [normalize_vector3_naive(pt, win) for pt in poly]

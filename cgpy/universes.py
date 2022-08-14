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
NormalizedPolygon = list[NormalizedPoint]

# 3d
Vector4 = typing.NewType("Vector4", FloatArray)
Matrix4x4 = typing.NewType("Matrix4x4", FloatArray)
Face = list[Vector4]
Object3D = list[Face]


@dataclasses.dataclass(frozen=True, slots=True)
class Window:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    def __post_init__(self) -> None:
        assert self.min_x < self.max_x
        assert self.min_y < self.max_y

    def __contains__(self, pt: Vector3) -> bool:
        validate_vector3(pt)

        x: float = pt[0, 0]
        y: float = pt[1, 0]

        return (self.min_x <= x <= self.max_x) and (self.min_y <= y <= self.max_y)

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y


def make_vector4(x: float, y: float, z: float) -> Vector4:
    vec = np.asfarray((x, y, z, 1)).reshape(4, 1)
    return Vector4(vec)


def validate_vector4(vec: typing.Any) -> None:
    assert isinstance(vec, np.ndarray)
    assert vec.shape == (4, 1)
    assert vec.dtype == np.float64


def validate_matrix4x4(matrix: typing.Any) -> None:
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


def transform_point_3d(pt: Vector4, trans: Matrix4x4) -> Vector4:
    return Vector4(trans @ pt)


def transform_face(face: Face, trans: Matrix4x4) -> Face:
    return [transform_point_3d(pt, trans) for pt in face]


def transform_object(
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


def normalize_vector3_naive(pt: Vector3, win: Window) -> NormalizedPoint:
    validate_vector3(pt)

    x = pt[0]
    y = pt[1]

    normalized = make_vector3(
        x=(x - win.min_x) / win.width,
        y=(y - win.min_y) / win.height,
    )

    return NormalizedPoint(normalized)


def validate_normalized_point(pt: Vector3) -> None:
    validate_vector3(pt)

    assert ((0 <= pt) & (pt <= 1)).all()


def normalize_polygon(poly: Polygon, win: Window) -> NormalizedPolygon:
    return [normalize_vector3_naive(pt, win) for pt in poly]


def make_translation_2d(delta_x: float, delta_y: float) -> Matrix3x3:
    matrix = np.eye(3, 3)
    matrix[0, 2] = delta_x
    matrix[1, 2] = delta_y
    return Matrix3x3(matrix)


def make_counterclockwise_rotation_2d(degrees: float) -> Matrix3x3:
    radians = degrees * np.pi / 180
    matrix = np.eye(3, 3)
    matrix[0, 0] = np.cos(radians)
    matrix[0, 1] = -1 * np.sin(radians)
    matrix[1, 0] = np.sin(radians)
    matrix[1, 1] = np.cos(radians)

    return Matrix3x3(matrix)


def make_scale_2d(x_factor: float, y_factor: float) -> Matrix3x3:
    matrix = np.eye(3, 3)
    matrix[0, 0] = x_factor
    matrix[1, 1] = y_factor

    return Matrix3x3(matrix)


def validate_matrix3x3(matrix: typing.Any) -> None:
    assert isinstance(matrix, np.ndarray)
    assert matrix.shape == (3, 3)
    assert matrix.dtype == np.float64


def transform_polygon(
    polygon: Polygon,
    trans: Matrix3x3,
) -> Polygon:
    validate_matrix3x3(trans)

    trans_poly = []
    for vec in polygon:
        validate_vector3(vec)
        trans_vec = Vector3(trans @ vec)
        trans_poly.append(trans_vec)

    return Polygon(trans_poly)

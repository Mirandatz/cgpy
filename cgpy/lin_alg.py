import dataclasses

from cgpy.universes import Point2D


@dataclasses.dataclass(frozen=True, slots=True)
class Vector3:
    v0: float
    v1: float
    v2: float


@dataclasses.dataclass(frozen=True, slots=True)
class Matrix3x3:
    m00: float
    m01: float
    m02: float
    m10: float
    m11: float
    m12: float
    m20: float
    m21: float
    m22: float

    def multiply_vector(self, vec: Vector3) -> Vector3:
        raise NotImplementedError()

    def multiply_matrix(self, other: "Matrix3x3") -> "Matrix3x3":
        raise NotImplementedError()


def point2d_to_vector3(pt: Point2D) -> Vector3:
    raise NotImplementedError()


def vector3_to_point2d(vec: Vector3) -> Point2D:
    raise NotImplementedError()


def make_translation(x_offset: float, y_offset: float) -> Matrix3x3:
    raise NotImplementedError()


def make_counterclockwise_rotation(degrees: float) -> Matrix3x3:
    raise NotImplementedError()


def make_scale(x_factor: float, y_factor: float) -> Matrix3x3:
    raise NotImplementedError()

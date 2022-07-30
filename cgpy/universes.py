import dataclasses


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
            pt.x > self.lower_left.x
            and pt.x < self.upper_right.x
            and pt.y > self.lower_left.y
            and pt.y < self.upper_right.y
        )


@dataclasses.dataclass(frozen=True, slots=True)
class NormalizedPoint2D:
    x: float
    y: float

    def __post_init__(self) -> None:
        assert 0 <= self.x <= 1
        assert 0 <= self.y <= 1


def normalize_point2d(pt: Point2D, win: Window) -> NormalizedPoint2D:
    raise NotImplementedError()

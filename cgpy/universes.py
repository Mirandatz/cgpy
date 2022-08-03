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
            self.lower_left.x <= pt.x <= self.upper_right.x
            and self.lower_left.y <= pt.y <= self.upper_right.y
        )

    @property
    def width(self) -> float:
        return self.upper_right.x - self.lower_left.x

    @property
    def height(self) -> float:
        return self.upper_right.y - -self.lower_left.y


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

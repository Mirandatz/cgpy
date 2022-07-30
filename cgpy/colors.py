import dataclasses
import typing

MIN_COLOR_INTENSITY = 0.0
MAX_COLOR_INTENSITY = 1.0
MAX_CHANNEL_VALUE = 255

ColorId = typing.NewType('ColorId', int)


@dataclasses.dataclass(frozen=True, slots=True)
class Color:
    red: float
    green: float
    blue: float

    def __post_init__(self) -> None:
        assert MIN_COLOR_INTENSITY <= self.red <= MAX_COLOR_INTENSITY
        assert MIN_COLOR_INTENSITY <= self.green <= MAX_COLOR_INTENSITY
        assert MIN_COLOR_INTENSITY <= self.blue <= MAX_COLOR_INTENSITY

    def as_rgb_ints(self) -> tuple[int, int, int]:
        r = int(self.red * MAX_CHANNEL_VALUE)
        g = int(self.green * MAX_CHANNEL_VALUE)
        b = int(self.blue * MAX_CHANNEL_VALUE)
        return r, g, b

import dataclasses

MIN_COLOR_INTENSITY = 0.0
MAX_COLOR_INTENSITY = 1.0
MAX_CHANNEL_VALUE = 255


@dataclasses.dataclass(frozen=True, slots=True)
class Color:
    red: float
    green: float
    blue: float

    def __post_init__(self) -> None:
        assert MIN_COLOR_INTENSITY <= self.red <= MAX_COLOR_INTENSITY
        assert MIN_COLOR_INTENSITY <= self.green <= MAX_COLOR_INTENSITY
        assert MIN_COLOR_INTENSITY <= self.blue <= MAX_COLOR_INTENSITY

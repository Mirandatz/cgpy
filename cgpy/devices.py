import dataclasses

import cgpy.colors as colors


@dataclasses.dataclass
class DevicePoint:
    x: int
    y: int

    def __post_init__(self) -> None:
        assert self.x > 0
        assert self.y > 0


class Device:
    def __init__(
        self,
        height: int,
        width: int,
        name: str = "dizpositivo",
    ) -> None:
        assert height > 0
        assert width > 0

        self._name = name
        self._height = height
        self._width = width
        self._buffer = [0 for _ in range(width * height)]

    @property
    def name(self) -> str:
        return self._name

    @property
    def height(self) -> int:
        return self._height

    @property
    def width(self) -> int:
        return self._width

    def set(self, x: int, y: int, color_id: int) -> None:
        assert 0 <= x < self.width
        assert 0 <= y < self.height

        self._buffer[y * self.width + x] = color_id

    def get(self, x: int, y: int) -> int:
        assert 0 <= x < self.width
        assert 0 <= y < self.height

        return self._buffer[y * self.width + x]


@dataclasses.dataclass(frozen=True, slots=True)
class Viewport:
    lower_left: DevicePoint
    upper_right: DevicePoint

    def __post_init__(self) -> None:
        assert self.lower_left.x < self.upper_right.x
        assert self.lower_left.y < self.upper_right.y


def show_device(
    device: Device,
    palette: list[colors.Color],
    close_after_milliseconds: int = 5000,
) -> None:
    assert close_after_milliseconds > 0

    import cv2
    import numpy as np

    img = np.zeros(shape=(device.height, device.width, 3), dtype="float64")
    for y in range(device.height):
        for x in range(device.width):
            color_index = device.get(x, y)

            assert color_index > 0

            color = palette[color_index]
            img[y, x, 0] = color.blue
            img[y, x, 1] = color.green
            img[y, x, 2] = color.red

    cv2.imshow(device.name, img)
    cv2.waitKey(close_after_milliseconds)
    cv2.destroyAllWindows()

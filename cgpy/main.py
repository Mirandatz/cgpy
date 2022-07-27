import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
class Color:
    red: float
    green: float
    blue: float

    def __post_init__(self) -> None:
        assert 0 <= self.red <= 1
        assert 0 <= self.green <= 1
        assert 0 <= self.blue <= 1


class Device:
    def __init__(self, height: int, width: int, name: str = "dizpositivo") -> None:
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


def show_device(
    device: Device,
    palette: list[Color],
    close_after_milliseconds: int = 5000,
) -> None:
    assert close_after_milliseconds > 0

    import cv2
    import numpy as np

    img = np.zeros(shape=(device.height, device.width, 3), dtype="float64")
    for y in range(device.height):
        for x in range(device.width):
            color_index = device.get(x, y)
            color = palette[color_index]
            img[y, x, 0] = color.blue
            img[y, x, 1] = color.green
            img[y, x, 2] = color.red

    cv2.imshow(device.name, img)
    cv2.waitKey(close_after_milliseconds)
    cv2.destroyAllWindows()


def main() -> None:
    dev = Device(height=480, width=720)
    for y in range(dev.height):
        for x in range(dev.width):
            dev.set(x, y, 1)

    palette = [Color(0, 0, 0), Color(1, 0, 0)]
    show_device(dev, palette)


if __name__ == "__main__":
    main()

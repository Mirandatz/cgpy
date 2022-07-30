from cgpy.colors import Color, ColorId
from cgpy.devices import Device, create_device_with_max_size, show_device


def main() -> None:
    dev = Device(height=720, width=480)
    dev = create_device_with_max_size()
    for y in range(dev.height):
        for x in range(dev.width):
            dev.set(x, y, ColorId(1))

    palette = [
        Color(red=0, green=0, blue=0),
        Color(red=1, green=0, blue=0),
        Color(red=0, green=0, blue=1),
    ]

    show_device(dev, palette, close_after_seconds=5)


if __name__ == "__main__":
    main()

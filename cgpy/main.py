import cgpy.colors as colors
import cgpy.devices as devices


def main() -> None:
    dev = devices.create_device_with_max_size()
    for y in range(dev.height):
        for x in range(dev.width):
            dev.set(x, y, 1)

    palette = [
        colors.Color(red=0, green=0, blue=0),
        colors.Color(red=1, green=0, blue=0),
        colors.Color(red=0, green=0, blue=1),
    ]

    devices.show_device(dev, palette, close_after_seconds=5)


if __name__ == "__main__":
    main()

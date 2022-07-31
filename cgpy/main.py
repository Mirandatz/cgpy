import cgpy.colors as colors
import cgpy.devices as devices
import cgpy.lin_alg as la
import cgpy.universes as uni


def main() -> None:
    dev = devices.Device(
        num_rows=1000,
        num_columns=100,
    )
    for y in range(dev.num_rows):
        for x in range(dev.num_columns):
            dev.set(x, y, colors.ColorId(2))

    palette = [
        colors.Color(red=1, green=0, blue=0),
        colors.Color(red=0, green=1, blue=0),
        colors.Color(red=0, green=0, blue=1),
    ]

    devices.show_device(dev, palette, close_after_milliseconds=500)
    palette[2] = colors.Color(red=1, green=0, blue=0)
    devices.show_device(dev, palette, close_after_milliseconds=500)
    palette[2] = colors.Color(red=0, green=1, blue=0)
    devices.show_device(dev, palette, close_after_milliseconds=500)


if __name__ == "__main__":
    main()

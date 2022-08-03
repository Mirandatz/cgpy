import numpy as np

import cgpy.colors as colors
import cgpy.devices as cd
import cgpy.lin_alg as la
import cgpy.universes as uni


def main() -> None:
    dev = cd.Device(
        num_rows=1000,
        num_columns=100,
    )
    for y in range(dev.num_rows):
        for x in range(dev.num_columns):
            dev.set(x, y, colors.ColorId(y))

    palette = [
        colors.Color(
            color_id / dev.num_rows, color_id / dev.num_rows, color_id / dev.num_rows
        )
        for color_id in np.sort(np.unique(dev.raw_buffer))
    ]

    cd.show_device(dev, palette, close_after_milliseconds=5000)


if __name__ == "__main__":
    main()

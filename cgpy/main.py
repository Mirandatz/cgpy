import numpy as np

import cgpy.colors as cc
import cgpy.devices as cd
import cgpy.lin_alg as la
import cgpy.universes as uni


def main() -> None:
    dev = cd.Device(
        num_rows=500,
        num_columns=500,
    )

    port = cd.Viewport(
        lower_left=cd.DevicePoint(0, 0),
        num_rows=dev.num_rows,
        num_columns=dev.num_columns,
        device=dev,
    )

    center = cd.DevicePoint(x=dev.num_columns // 2, y=dev.num_rows // 2)

    for x in range(dev.num_columns):
        if x % 2 == 0:
            cd.draw_line_bresenham(
                pt0=center,
                pt1=cd.DevicePoint(x, 0),
                color_id=cc.ColorId(1),
                port=port,
            )
            cd.draw_line_bresenham(
                pt0=center,
                pt1=cd.DevicePoint(x, dev.num_rows - 1),
                color_id=cc.ColorId(1),
                port=port,
            )

    palette = [cc.Color(0, 0, 0), cc.Color(1, 1, 1)]
    cd.show_device(dev, palette, close_after_milliseconds=50000)


if __name__ == "__main__":
    main()

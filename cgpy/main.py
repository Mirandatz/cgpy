import cgpy.colors as cc
import cgpy.devices as cd
import cgpy.universes as cu


def exemplo1() -> None:
    poly1 = [
        cu.Point2D(-9, -8),
        cu.Point2D(-7, -3),
        cu.Point2D(-4, -4),
        cu.Point2D(-3, -6),
        cu.Point2D(-6, -9),
    ]

    poly2 = [
        cu.Point2D(-6, -2),
        cu.Point2D(-1, -2),
        cu.Point2D(-1, -6),
        cu.Point2D(-6, -6),
    ]

    win = cu.Window(
        lower_left=cu.Point2D(-10, -10),
        upper_right=cu.Point2D(0, 0),
    )

    npoly1 = cu.normalize_polygon(poly1, win)
    npoly2 = cu.normalize_polygon(poly2, win)

    dev = cd.Device(num_columns=640, num_rows=480)

    port = cd.Viewport(
        lower_left=cd.DevicePoint(0, 0),
        num_rows=dev.num_rows,
        num_columns=dev.num_columns,
        device=dev,
    )

    cd.draw_polygon(npoly1, port, cc.ColorId(1))
    cd.draw_polygon(npoly2, port, cc.ColorId(3))

    palette = [
        cc.Color(0, 0, 0),
        cc.Color(1, 0, 0),
        cc.Color(0, 1, 0),
        cc.Color(0, 0, 1),
        cc.Color(1, 1, 1),
    ]
    cd.show_device(dev, palette, close_after_milliseconds=2000)


def exemplo2() -> None:
    poly1 = [
        cu.Point2D(-9, -8),
        cu.Point2D(-7, -3),
        cu.Point2D(-4, -4),
        cu.Point2D(-3, -6),
        cu.Point2D(-6, -9),
    ]

    poly2 = [
        cu.Point2D(-6, -2),
        cu.Point2D(-1, -2),
        cu.Point2D(-1, -6),
        cu.Point2D(-6, -6),
    ]

    win = cu.Window(
        lower_left=cu.Point2D(-10, -10),
        upper_right=cu.Point2D(0, 0),
    )

    npoly1 = cu.normalize_polygon(poly1, win)
    npoly2 = cu.normalize_polygon(poly2, win)

    dev = cd.Device(num_columns=640, num_rows=480)

    port1 = cd.make_viewport_from_corners(
        cd.DevicePoint(30, 60),
        cd.DevicePoint(347, 220),
        dev,
    )
    port2 = cd.make_viewport_from_corners(
        cd.DevicePoint(370, 270),
        cd.DevicePoint(503, 407),
        device=dev,
    )

    cd.draw_polygon(npoly1, port1, cc.ColorId(1))
    cd.draw_polygon(npoly2, port2, cc.ColorId(3))

    palette = [
        cc.Color(0, 0, 0),
        cc.Color(1, 0, 0),
        cc.Color(0, 1, 0),
        cc.Color(0, 0, 1),
        cc.Color(1, 1, 1),
    ]
    cd.show_device(dev, palette, close_after_milliseconds=2000)


def main() -> None:
    exemplo1()
    exemplo2()


if __name__ == "__main__":
    main()

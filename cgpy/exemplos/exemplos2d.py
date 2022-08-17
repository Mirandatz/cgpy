import cgpy.colors as cc
import cgpy.devices as cd
import cgpy.universes as cu


def exemplo1() -> None:
    poly1 = [
        cu.make_vector3(-9, -8),
        cu.make_vector3(-7, -3),
        cu.make_vector3(-4, -4),
        cu.make_vector3(-3, -6),
        cu.make_vector3(-6, -9),
    ]

    poly2 = [
        cu.make_vector3(-6, -2),
        cu.make_vector3(-1, -2),
        cu.make_vector3(-1, -6),
        cu.make_vector3(-6, -6),
    ]

    win = cu.Window(
        min_x=-10,
        min_y=-10,
        max_x=0,
        max_y=0,
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
        cu.make_vector3(-9, -8),
        cu.make_vector3(-7, -3),
        cu.make_vector3(-4, -4),
        cu.make_vector3(-3, -6),
        cu.make_vector3(-6, -9),
    ]

    poly2 = [
        cu.make_vector3(-6, -2),
        cu.make_vector3(-1, -2),
        cu.make_vector3(-1, -6),
        cu.make_vector3(-6, -6),
    ]

    win = cu.Window(
        min_x=-10,
        min_y=-10,
        max_x=0,
        max_y=0,
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


def exemplo3() -> None:
    dev = cd.Device(num_columns=800, num_rows=600)
    palette = [
        cc.Color(0, 0, 0),
        cc.Color(1, 0, 0),
        cc.Color(0, 1, 0),
        cc.Color(0, 0, 1),
        cc.Color(0.4, 0.3, 1),
        cc.Color(0.8, 0.8, 0.8),
        cc.Color(1, 1, 1),
    ]

    poly1 = [
        cu.make_vector3(-9, -8),
        cu.make_vector3(-7, -3),
        cu.make_vector3(-4, -4),
        cu.make_vector3(-3, -6),
        cu.make_vector3(-6, -9),
    ]

    poly2 = [
        cu.make_vector3(-6, -2),
        cu.make_vector3(-1, -2),
        cu.make_vector3(-1, -6),
        cu.make_vector3(-6, -6),
    ]

    win = cu.Window(
        min_x=-10,
        min_y=-10,
        max_x=10,
        max_y=10,
    )

    port = cd.Viewport(
        lower_left=cd.DevicePoint(0, 0),
        num_columns=800,
        num_rows=600,
        device=dev,
    )

    npoly1 = cu.normalize_polygon(poly1, win)
    cd.draw_polygon(npoly1, port, cc.ColorId(1))

    npoly2 = cu.normalize_polygon(poly2, win)
    cd.draw_polygon(npoly2, port, cc.ColorId(3))

    translate = cu.make_translation_2d(10, 10)
    poly3 = cu.transform_polygon(poly1, translate)
    npoly3 = cu.normalize_polygon(poly3, win)
    cd.draw_polygon(npoly3, port, cc.ColorId(2))

    rotate = cu.make_counterclockwise_rotation_2d(45)
    poly4 = cu.transform_polygon(poly2, rotate)
    npoly4 = cu.normalize_polygon(poly4, win)
    cd.draw_polygon(npoly4, port, cc.ColorId(4))

    cd.draw_viewport(port, cc.ColorId(len(palette) - 1))
    cd.show_device(dev, palette, close_after_milliseconds=2000)


def exemplo_floodfill() -> None:
    num_columns = 1000
    num_rows = 200
    dev = cd.Device(num_columns=num_columns, num_rows=num_rows)
    port = cd.Viewport(
        lower_left=cd.DevicePoint(1, 1),
        num_columns=num_columns - 1,
        num_rows=num_rows - 1,
        device=dev,
    )

    palette = [
        cc.Color(0, 0, 0),
        cc.Color(1, 0, 0),
        cc.Color(0, 1, 0),
        cc.Color(0, 0, 1),
        cc.Color(0.4, 0.3, 1),
        cc.Color(0.8, 0.8, 0.8),
        cc.Color(1, 1, 1),
    ]

    cd._flood_fill(cd.DevicePoint(5, 5), cc.ColorId(3), cc.ColorId(3), port.buffer_view)

    cd.show_device(dev, palette, close_after_milliseconds=2000)


def main() -> None:
    exemplo1()
    exemplo2()
    exemplo3()


if __name__ == "__main__":
    main()

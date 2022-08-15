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
    cd.show_device(dev, palette)


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

    cd.show_device(dev, palette, 2000)


def exemplo_3d() -> None:
    window = cu.Window(
        min_x=-30,
        min_y=-30,
        max_x=30,
        max_y=30,
    )

    device = cd.Device(num_columns=800, num_rows=600)

    palette = [
        cc.Color(0, 0, 0),
        cc.Color(1, 0, 0),
        cc.Color(0, 1, 0),
        cc.Color(0, 0, 1),
        cc.Color(0.4, 0.3, 1),
        cc.Color(0.8, 0.8, 0.8),
        cc.Color(1, 1, 1),
    ]

    face0 = [
        cu.make_vector4(10.0, 10.0, 0.0),
        cu.make_vector4(10.0, 0.0, 15.0),
        cu.make_vector4(10.0, -10.0, 0.0),
    ]

    face1 = [
        cu.make_vector4(-10.0, 10.0, 0.0),
        cu.make_vector4(-10.0, 0.0, 15.0),
        cu.make_vector4(-10.0, -10.0, 0.0),
    ]

    face2 = [
        cu.make_vector4(10.0, 10.0, 0.0),
        cu.make_vector4(10.0, 0.0, 15.0),
        cu.make_vector4(-10.0, 0.0, 15.0),
        cu.make_vector4(-10.0, 10.0, 0.0),
    ]

    face3 = [
        cu.make_vector4(10.0, 0.0, 15.0),
        cu.make_vector4(10.0, -10.0, 0.0),
        cu.make_vector4(-10.0, -10.0, 0.0),
        cu.make_vector4(-10.0, 0.0, 15.0),
    ]

    face4 = [
        cu.make_vector4(10.0, 10.0, 0.0),
        cu.make_vector4(10.0, -10.0, 0.0),
        cu.make_vector4(-10.0, -10.0, 0.0),
        cu.make_vector4(-10.0, 10.0, 0.0),
    ]

    objected_3d = [face0, face1, face2, face3, face4]
    zpp = 40
    zcp = -45

    # port 0
    observer_0 = cu.create_observer_transformation_matrix(
        cu.make_vector4(0, 0, 1),
        cu.make_vector4(1, 0, 0),
        cu.make_vector4(0, 0, 0),
    )
    obj_for_observer_0 = cu.transform_object(objected_3d, observer_0)

    projected_0 = cu.perspective_project_object(obj_for_observer_0, zpp=zpp, zcp=zcp)
    object_2d_0 = cu.object3d_to_object2d(projected_0)

    port0 = cd.Viewport(
        lower_left=cd.DevicePoint(0, 0),
        num_columns=device.num_columns // 2,
        num_rows=device.num_rows // 2,
        device=device,
    )

    for poly in object_2d_0:
        npoly = cu.normalize_polygon(poly, window)
        cd.draw_polygon(npoly, port0, cc.ColorId(1))

    # port 1
    observer_1 = cu.create_observer_transformation_matrix(
        cu.make_vector4(0, 0, 1),
        cu.make_vector4(0, 1, 0),
        cu.make_vector4(0, 0, 0),
    )
    obj_for_observer_1 = cu.transform_object(objected_3d, observer_1)

    projected_1 = cu.perspective_project_object(obj_for_observer_1, zpp=zpp, zcp=zcp)
    object_2d_1 = cu.object3d_to_object2d(projected_1)

    port1 = cd.Viewport(
        lower_left=cd.DevicePoint(400 - 1, 0),
        num_columns=device.num_columns // 2,
        num_rows=device.num_rows // 2,
        device=device,
    )

    for poly in object_2d_1:
        npoly = cu.normalize_polygon(poly, window)
        cd.draw_polygon(npoly, port1, cc.ColorId(1))

    # port 3
    observer_3 = cu.create_observer_transformation_matrix(
        cu.make_vector4(1, 1, 1),
        cu.make_vector4(1, -1, -1),
        cu.make_vector4(0, 0, 0),
    )
    obj_for_observer_3 = cu.transform_object(objected_3d, observer_3)

    projected_3 = cu.perspective_project_object(obj_for_observer_3, zpp=zpp, zcp=zcp)
    object_2d_3 = cu.object3d_to_object2d(projected_3)

    port3 = cd.Viewport(
        lower_left=cd.DevicePoint(400 - 1, 300 - 1),
        num_columns=device.num_columns // 2,
        num_rows=device.num_rows // 2,
        device=device,
    )

    for poly in object_2d_3:
        npoly = cu.normalize_polygon(poly, window)
        cd.draw_polygon(npoly, port3, cc.ColorId(1))

    cd.show_device(device, palette, close_after_milliseconds=2000)


def main() -> None:
    # exemplo1()
    # exemplo2()
    # exemplo3()
    # exemplo_floodfill()
    exemplo_3d()


if __name__ == "__main__":
    main()

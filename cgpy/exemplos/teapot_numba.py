import pathlib
import time

import numpy as np
import pandas as pd

import cgpy.colors as cc
import cgpy.devices as cd
import cgpy.devices_mk2 as cd_mk2
import cgpy.universes as cu
import cgpy.universes_mk2 as cu_mk2

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
NUMBER_OF_DEVICES = 600


def load_teapot() -> cu.Object3D:
    vertices_df = pd.read_csv(DATA_DIR / "teapot_vertices.csv", index_col=0)
    vertices = [cu.make_vector4(*r) for r in vertices_df.to_numpy()]

    faces_df = pd.read_csv(
        DATA_DIR / "teapot_faces.csv",
        index_col=0,
    )

    teapot = [
        cu.Face([vertices[i], vertices[j], vertices[k]])
        for i, j, k in faces_df.to_numpy()
    ]

    return teapot


def generate_device(teapot: cu_mk2.Object3D, degrees: float) -> cd.Device:
    rotation_matrix = cu_mk2.make_x_rotation_3d(degrees)
    observer = cu.create_observer_transformation_matrix(
        normal=cu.make_vector4(0, 0, 1),
        up=cu.make_vector4(0, 1, 0),
        offset=cu.make_vector4(0, 0, 0),
    )

    trans = (observer @ rotation_matrix).astype(np.float32)
    rotated_teapot = cu_mk2.transform_object3d(teapot, trans)

    zpp = 40
    zcp = -45

    bruh_obj2d = cu_mk2.perspective_project(rotated_teapot, zpp, zcp)
    device = cd.Device(num_columns=800, num_rows=600)

    port = cd.Viewport(
        lower_left=cd.DevicePoint(0, 0),
        num_columns=device.num_columns,
        num_rows=device.num_rows,
        device=device,
    )

    window = cu.Window(-10, -10, 10, 10)

    n_bruh_obj2d = cu_mk2.normalize_object2d_naive(
        bruh_obj2d,
        x_min=window.min_x,
        y_min=window.min_y,
        x_max=window.max_x,
        y_max=window.max_y,
    )
    cd_mk2.draw_object2d(
        poly=n_bruh_obj2d,
        port=port.buffer_view,
        color_id=cc.ColorId(1),
    )

    print(".", end="")

    return device


def animate_teapot(number_of_devices: int = NUMBER_OF_DEVICES) -> None:
    start = time.time()

    teapot = load_teapot()
    new_teapot = cu_mk2.old_object3d_to_new_object3d(teapot)

    devices = []
    for timestep in range(number_of_devices):
        devices.append(generate_device(new_teapot, timestep))

    palette = cc.Palette([cc.Color(0, 0, 0), cc.Color(1, 0, 0)])

    end = time.time()
    print(f"time: {end - start}")

    assert devices is not None
    assert palette is not None

    cd.animate_devices(
        devices,
        [palette],
        fps=60,
    )


def main() -> None:
    animate_teapot()


if __name__ == "__main__":
    main()

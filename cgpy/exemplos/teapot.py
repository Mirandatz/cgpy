import itertools
import multiprocessing as mp
import pathlib
import pickle

import pandas as pd

import cgpy.colors as cc
import cgpy.devices as cd
import cgpy.universes as cu

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"
DEVICE_COUNT = 360


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


def generate_device(teapot: cu.Object3D, degrees: float) -> cd.Device:
    rotation_matrix = cu.make_y_rotation_3d(degrees)
    rotated_teapot = cu.transform_object(teapot, rotation_matrix)

    observer = cu.create_observer_transformation_matrix(
        normal=cu.make_vector4(0, 0, 1),
        up=cu.make_vector4(0, 1, 0),
        offset=cu.make_vector4(0, 0, 0),
    )

    obj_for_observer_1 = cu.transform_object(rotated_teapot, observer)
    zpp = 40
    zcp = -45

    projected_teapot = cu.perspective_project_object(
        obj_for_observer_1, zpp=zpp, zcp=zcp
    )
    teapot_2d = cu.object3d_to_object2d(projected_teapot)

    device = cd.Device(num_columns=800, num_rows=600)

    port = cd.Viewport(
        lower_left=cd.DevicePoint(0, 0),
        num_columns=device.num_columns,
        num_rows=device.num_rows,
        device=device,
    )

    window = cu.Window(-10, -10, 10, 10)

    for poly in teapot_2d:
        npoly = cu.normalize_polygon(poly, window)
        cd.draw_polygon(npoly, port, cc.ColorId(1))

    print(".", end="")

    return device


def load_or_generate_devices() -> list[cd.Device]:
    cache = pathlib.Path("/dev/shm/cgpy/teapots.pickle")

    try:
        devices: list[cd.Device] = pickle.loads(cache.read_bytes())
        assert isinstance(devices, list)
        assert all(isinstance(d, cd.Device) for d in devices)

    except Exception:
        teapot = load_teapot()

        with mp.Pool() as pool:
            teapots = itertools.repeat(teapot)
            timesteps = range(DEVICE_COUNT)
            args = zip(teapots, timesteps)
            devices = pool.starmap(generate_device, args)

            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_bytes(pickle.dumps(devices, pickle.HIGHEST_PROTOCOL))

    return devices


def animate_teapot() -> None:
    devices = load_or_generate_devices()
    palette = cc.Palette([cc.Color(0, 0, 0), cc.Color(1, 0, 0)])
    cd.animate_devices(
        devices,
        [palette],
        fps=60,
    )


if __name__ == "__main__":
    animate_teapot()

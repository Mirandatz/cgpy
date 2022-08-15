import itertools
import multiprocessing as mp
import pathlib

import pandas as pd
import pygame

import cgpy.colors as cc
import cgpy.devices as cd
import cgpy.universes as cu

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


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


def get_device(teapot: cu.Object3D, timestep: int) -> cd.Device:
    print(f"start processing {timestep=}")

    rotation_matrix = cu.make_y_rotation_3d(timestep * 5)
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

    print(f"finished processing {timestep=}")

    return device


def draw_teapot() -> None:
    teapot = load_teapot()

    palette = [
        cc.Color(0, 0, 0),
        cc.Color(1, 0, 0),
        cc.Color(0, 1, 0),
        cc.Color(0, 0, 1),
        cc.Color(0.4, 0.3, 1),
        cc.Color(0.8, 0.8, 0.8),
        cc.Color(1, 1, 1),
    ]

    with mp.Pool() as pool:
        teapots = itertools.repeat(teapot)
        timesteps = range(100)
        args = zip(teapots, timesteps)
        devices = pool.starmap(get_device, args)

    surface_arrays = [cd._device_to_surface_array(dev, palette) for dev in devices]

    screen = pygame.display.set_mode((800, 600), pygame.NOFRAME)
    clock = pygame.time.Clock()

    frames = itertools.chain(surface_arrays, reversed(surface_arrays))
    for sa in itertools.cycle(frames):
        surface = pygame.surfarray.make_surface(sa)
        screen.blit(surface, (0, 0))
        pygame.display.update()

        clock.tick(60)


if __name__ == "__main__":
    draw_teapot()

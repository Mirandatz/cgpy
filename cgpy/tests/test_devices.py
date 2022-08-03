import hypothesis.strategies as hs
from hypothesis import given

import cgpy.devices as cd


@hs.composite
def devices(draw: hs.DrawFn) -> cd.Device:
    return cd.Device(
        num_rows=draw(hs.integers(min_value=1, max_value=9)),
        num_columns=draw(hs.integers(min_value=1, max_value=9)),
    )


@hs.composite
def viewports(draw: hs.DrawFn) -> cd.Viewport:
    dev = draw(devices())

    num_columns = draw(hs.integers(min_value=1, max_value=dev.num_columns))
    num_rows = draw(hs.integers(min_value=1, max_value=dev.num_rows))

    max_x = abs(num_columns - dev.num_columns)
    max_y = abs(num_rows - dev.num_rows)

    lower_left = cd.DevicePoint(
        x=draw(hs.integers(0, max_x)),
        y=draw(hs.integers(0, max_y)),
    )

    return cd.Viewport(
        lower_left=lower_left,
        num_rows=num_rows,
        num_columns=num_columns,
        device=dev,
    )


@hs.composite
def devicepoints(draw: hs.DrawFn) -> cd.DevicePoint:
    return cd.DevicePoint(
        draw(hs.integers(min_value=0)),
        draw(hs.integers(min_value=0)),
    )


@given(dev=devices(), pt=devicepoints())
def test_device_contains(dev: cd.Device, pt: cd.DevicePoint) -> None:
    expected = pt.x < dev.num_columns and pt.y < dev.num_rows
    assert expected == (pt in dev)


@given(port=viewports(), pt=devicepoints())
def test_viewport_contains(port: cd.Viewport, pt: cd.DevicePoint) -> None:
    expected = (
        port.inclusive_left <= pt.x < port.exclusive_right
        and port.inclusive_bottom <= pt.y < port.exclusive_top
    )
    assert expected == (pt in port)

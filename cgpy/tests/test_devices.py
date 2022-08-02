import hypothesis.strategies as hs
from hypothesis import given

import cgpy.devices as devices


@given(
    num_columns=hs.integers(
        min_value=1, max_value=9
    ),  # max_value = 9 to limit allocated buffer size
    num_rows=hs.integers(
        min_value=1, max_value=9
    ),  # max_value = 9 to limit allocated buffer size
    x=hs.integers(min_value=0, max_value=99),
    y=hs.integers(min_value=0, max_value=99),
)
def test_device_contains(
    num_columns: int,
    num_rows: int,
    x: int,
    y: int,
) -> None:
    dev = devices.Device(num_columns=num_columns, num_rows=num_rows)
    pt = devices.DevicePoint(x=x, y=y)
    expected = pt.x < dev.num_columns and pt.y < dev.num_rows
    assert expected == (pt in dev)

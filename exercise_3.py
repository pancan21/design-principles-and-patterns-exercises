# TODO: The function `get_bounding_box` is generic in that it allows to compute
#       the bounding box for any point cloud represented in the form of an iterable
#       over points of a specific interface (defined in `PointInterface`). But, we want
#       to use points of type `MyPoint` which does not fulfill that interface.
#       In order to still be able to use `get_bounding_box`, we have to write an adapter
#       that wraps an instance of `MyPoint` and exposes the required interface.
from sys import float_info
from typing import Protocol, Iterable, Tuple
from dataclasses import dataclass


@dataclass
class BoundingBox:
    min: Tuple[float, float]
    max: Tuple[float, float]

    def __repr__(self) -> str:
        return f"BBox: {self._as_string(self.min)} - {self._as_string(self.max)}"

    def _as_string(self, point: Tuple[float, float]) -> str:
        return f"({point[0]}, {point[1]})"


# `Point` interface expected by `get_bounding_box`
class PointInterface(Protocol):
    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

def get_bounding_box(point_cloud: Iterable[PointInterface]) -> BoundingBox:
    xmin = ymin = float_info.max
    xmax = ymax = -xmin
    for p in point_cloud:
        xmin = min(xmin, p.x)
        ymin = min(ymin, p.y)

        xmax = max(xmax, p.x)
        ymax = max(ymax, p.y)
    return BoundingBox(min=(xmin, ymin), max=(xmax, ymax))


@dataclass
class Point:
    x: float
    y: float


class MyPoint:
    def __init__(self, coords: Tuple[float, float]) -> None:
        self._coords = coords

    def __getitem__(self, i: int) -> float:
        """Return the coordinate for the given index"""
        return self._coords[i]


# TODO: Implement this adapter
# class MyPointAdapter:
#     pass

if __name__ == "__main__":
    point_cloud = [
        Point(0.1, 0.1),
        Point(0.9, 0.9),
        Point(0.1, 2.0)
    ]
    bbox = get_bounding_box(point_cloud)
    print("Bounding box with default point implementation: ", bbox)

    # TODO: make it possible to use `get_bounding_box` also with a list of
    #       instances of `MyPoint` by implementing the adapter
    my_points_impl_2 = [MyPoint((p.x, p.y)) for p in point_cloud]
    bbox = get_bounding_box([MyPointAdapter(p) for p in my_points_impl_2])
    print("Bounding box with MyPoint: ", bbox)

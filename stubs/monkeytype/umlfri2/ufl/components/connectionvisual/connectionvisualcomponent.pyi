from typing import List
from umlfri2.types.geometry.point import Point
from umlfri2.ufl.components.connectionvisual.connectionvisualcontainer import ConnectionVisualContainerObject
from umlfri2.ufl.context.context import Context


class ConnectionVisualComponent:
    def create_connection_object(
        self,
        context: Context
    ) -> ConnectionVisualContainerObject: ...


class ConnectionVisualObject:
    def _compute_position(
        self,
        points: List[Point],
        position: float
    ) -> PointPosition: ...

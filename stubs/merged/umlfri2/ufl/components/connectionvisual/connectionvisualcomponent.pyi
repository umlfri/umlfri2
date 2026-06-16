from ..base.component import Component as Component
from _typeshed import Incomplete
from typing import NamedTuple
from typing import List
from umlfri2.types.geometry.point import Point
from umlfri2.ufl.components.connectionvisual.connectionvisualcontainer import ConnectionVisualContainerObject
from umlfri2.ufl.context.context import Context

class PointPosition(NamedTuple):
    id: Incomplete
    t: Incomplete
    position: Incomplete
    orientation: Incomplete

class ConnectionVisualObject:
    def assign_points(self, points) -> None: ...
    def draw(self, canvas) -> None: ...

class ConnectionVisualComponent(Component):
    def create_connection_object(
        self,
        context: Context
    ) -> ConnectionVisualContainerObject: ...

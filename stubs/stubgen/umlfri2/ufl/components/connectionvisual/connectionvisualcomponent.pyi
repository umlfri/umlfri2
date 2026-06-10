from ..base.component import Component as Component
from _typeshed import Incomplete
from typing import NamedTuple

class PointPosition(NamedTuple):
    id: Incomplete
    t: Incomplete
    position: Incomplete
    orientation: Incomplete

class ConnectionVisualObject:
    def assign_points(self, points) -> None: ...
    def draw(self, canvas) -> None: ...

class ConnectionVisualComponent(Component):
    def create_connection_object(self, context): ...

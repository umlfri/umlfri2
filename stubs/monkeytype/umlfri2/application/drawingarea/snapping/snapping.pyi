from typing import (
    Any,
    Iterator,
)
from umlfri2.application.application import Application
from umlfri2.application.drawingarea.snapping.initialized import InitializedSnapping
from umlfri2.model.connection.connectionvisual import ConnectionVisual


class Snapping:
    def __init__(
        self,
        application: Application,
        elements: Iterator[Any],
        connections: Iterator[Any],
        selected_elements: Iterator[Any]
    ) -> None: ...
    def build(self) -> InitializedSnapping: ...
    def ignore_point(
        self,
        connection: ConnectionVisual,
        index: int
    ) -> Snapping: ...
    def ignore_selection(self) -> Snapping: ...

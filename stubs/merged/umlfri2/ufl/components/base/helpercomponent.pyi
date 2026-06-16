from .component import Component as Component
from typing import (
    Any,
    Iterator,
)
from umlfri2.ufl.context.context import Context

class HelperComponent(Component):
    IS_HELPER: bool
    def get_children(self, context: Context) -> Iterator[Any]: ...

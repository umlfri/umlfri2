from typing import (
    Any,
    Iterator,
)
from umlfri2.ufl.context.context import Context


class HelperComponent:
    def get_children(self, context: Context) -> Iterator[Any]: ...

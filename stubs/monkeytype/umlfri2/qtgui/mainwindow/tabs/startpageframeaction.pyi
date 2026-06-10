from functools import partial
from typing import (
    Callable,
    Union,
)


class StartPageFrameAction:
    def __init__(self) -> None: ...
    def set_action_callback(self, callback: Union[Callable, partial]) -> None: ...
    def set_context_menu_builder(self, menu_builder: partial) -> None: ...

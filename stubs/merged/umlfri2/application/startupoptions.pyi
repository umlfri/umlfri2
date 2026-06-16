from typing import (
    Any,
    List,
)
from umlfri2.application.application import Application

class StartupOptions:
    def __init__(self, application: Application, args: List[Any]) -> None: ...
    def apply_at_start(self) -> None: ...
    def apply_after_main_window(self) -> None: ...

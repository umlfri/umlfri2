from __future__ import annotations

from typing import Any

from ..base import Event


class ActionTriggeredEvent(Event):
    def __init__(self, action: Any) -> None:
        self.__action = action
    
    @property
    def action(self) -> Any:
        return self.__action

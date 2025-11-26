from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.addon.local.gui import AddOnAction


class ActionTriggeredEvent(Event):
    def __init__(self, action: AddOnAction) -> None:
        self.__action = action
    
    @property
    def action(self) -> AddOnAction:
        return self.__action

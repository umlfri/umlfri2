from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.addon.local import AddOn, AddOnState


class AddOnStateChangedEvent(Event):
    def __init__(self, addon: AddOn, state: AddOnState) -> None:
        self.__addon = addon
        self.__state = state
    
    @property
    def addon(self) -> AddOn:
        return self.__addon
    
    @property
    def addon_state(self) -> AddOnState:
        return self.__state

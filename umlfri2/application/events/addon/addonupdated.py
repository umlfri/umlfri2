from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.addon.local import AddOn


class AddOnUpdatedEvent(Event):
    def __init__(self, addon: AddOn) -> None:
        self.__addon = addon
    
    @property
    def addon(self) -> AddOn:
        return self.__addon

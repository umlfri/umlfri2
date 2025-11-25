from __future__ import annotations

from typing import TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.updates import UmlFriUpdates


class UpdateCheckFinishedEvent(Event):
    def __init__(self, updates: UmlFriUpdates) -> None:
        self.__updates = updates
    
    @property
    def updates(self) -> UmlFriUpdates:
        return self.__updates

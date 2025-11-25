from __future__ import annotations

from typing import Union, TYPE_CHECKING

from ..base import Event

if TYPE_CHECKING:
    from umlfri2.application.recentfile import RecentFile


class RecentFilesChangedEvent(Event):
    def __init__(self, new_file: Union[str, RecentFile]) -> None:
        self.__new_file = new_file
    
    @property
    def new_file(self) -> Union[str, RecentFile]:
        return self.__new_file

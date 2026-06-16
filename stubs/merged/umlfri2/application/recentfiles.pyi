from .events.application import RecentFilesChangedEvent as RecentFilesChangedEvent
from .recentfile import RecentFile as RecentFile
from _typeshed import Incomplete
from umlfri2.constants.paths import CONFIG as CONFIG
from typing import Iterator
from umlfri2.application.application import Application
from umlfri2.application.recentfile import RecentFile


class RecentFiles:
    CONFIG_FILE: Incomplete
    def __init__(self, application: Application) -> None: ...
    def __iter__(self) -> Iterator[RecentFile]: ...
    def add_file(self, file_path: str) -> None: ...

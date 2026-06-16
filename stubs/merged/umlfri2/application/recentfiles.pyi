from .events.application import RecentFilesChangedEvent as RecentFilesChangedEvent
from .recentfile import RecentFile as RecentFile
from _typeshed import Incomplete
from umlfri2.constants.paths import CONFIG as CONFIG

class RecentFiles:
    CONFIG_FILE: Incomplete
    def __init__(self, application) -> None: ...
    def __iter__(self): ...
    def add_file(self, file_path) -> None: ...

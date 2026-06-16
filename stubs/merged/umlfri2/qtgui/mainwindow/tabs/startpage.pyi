from ...base.resources import ICONS as ICONS
from .startpageframe import StartPageFrame as StartPageFrame
from PyQt5.QtWidgets import QWidget
from umlfri2.application import Application as Application
from umlfri2.application.events.application import LanguageChangedEvent as LanguageChangedEvent, RecentFilesChangedEvent as RecentFilesChangedEvent
from umlfri2.constants.paths import GRAPHICS as GRAPHICS

class StartPage(QWidget):
    def __init__(self, main_window) -> None: ...
    def paintEvent(self, event) -> None: ...

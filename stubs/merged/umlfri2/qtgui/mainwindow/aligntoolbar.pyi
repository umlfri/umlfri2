from PyQt5.QtWidgets import QToolBar
from umlfri2.application import Application as Application
from umlfri2.application.commands.diagram import AlignSelectionCommand as AlignSelectionCommand, AlignType as AlignType
from umlfri2.application.events.application import LanguageChangedEvent as LanguageChangedEvent
from umlfri2.application.events.diagram import SelectionChangedEvent as SelectionChangedEvent
from umlfri2.application.events.tabs import ChangedCurrentTabEvent as ChangedCurrentTabEvent
from umlfri2.constants.paths import GRAPHICS as GRAPHICS

class AlignToolBar(QToolBar):
    def __init__(self) -> None: ...

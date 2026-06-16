from PyQt5.QtWidgets import QToolBar
from umlfri2.application import Application as Application
from umlfri2.application.commands.diagram import HideElementsCommand as HideElementsCommand, PasteSnippetCommand as PasteSnippetCommand
from umlfri2.application.events.application import LanguageChangedEvent as LanguageChangedEvent

UNDO_REDO_COUNT: int

class MainToolBar(QToolBar):
    def __init__(self, main_window) -> None: ...

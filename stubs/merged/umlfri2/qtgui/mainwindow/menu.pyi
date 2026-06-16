from PyQt5.QtWidgets import QMenuBar
from umlfri2.application import Application as Application
from umlfri2.application.commands.diagram import DuplicateSnippetCommand as DuplicateSnippetCommand, HideElementsCommand as HideElementsCommand, PasteSnippetCommand as PasteSnippetCommand
from umlfri2.application.events.application.languagechanged import LanguageChangedEvent as LanguageChangedEvent
from umlfri2.constants.keys import COPY_IMAGE as COPY_IMAGE, FULL_SCREEN as FULL_SCREEN, PASTE_DUPLICATE as PASTE_DUPLICATE, ZOOM_ORIGINAL as ZOOM_ORIGINAL
from umlfri2.qtgui.appdialogs.about import AboutDialog as AboutDialog
from umlfri2.qtgui.appdialogs.addons import AddOnsDialog as AddOnsDialog
from umlfri2.qtgui.appdialogs.settings import SettingsDialog as SettingsDialog
from umlfri2.qtgui.fullscreen import FullScreenDiagram as FullScreenDiagram
from umlfri2.qtgui.printing import Printing as Printing
from umlfri2.qtgui.rendering import ExportDialog as ExportDialog, ImageExport as ImageExport

class MainWindowMenu(QMenuBar):
    def __init__(self, main_window) -> None: ...

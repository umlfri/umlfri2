from ..base.contextmenu import ContextMenu as ContextMenu
from ..properties import PropertiesDialog as PropertiesDialog
from umlfri2.application import Application as Application
from umlfri2.application.commands.diagram import DuplicateSnippetCommand as DuplicateSnippetCommand, PasteSnippetCommand as PasteSnippetCommand
from umlfri2.constants.keys import PASTE_DUPLICATE as PASTE_DUPLICATE

class CanvasDiagramMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, diagram) -> None: ...

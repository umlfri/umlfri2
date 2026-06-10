from ..base.contextmenu import ContextMenu as ContextMenu
from ..properties import PropertiesDialog as PropertiesDialog
from umlfri2.application import Application as Application
from umlfri2.application.commands.diagram import DuplicateSnippetCommand as DuplicateSnippetCommand, HideConnectionCommand as HideConnectionCommand, PasteSnippetCommand as PasteSnippetCommand
from umlfri2.application.commands.model import DeleteConnectionCommand as DeleteConnectionCommand, ReverseConnectionCommand as ReverseConnectionCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT as DELETE_FROM_PROJECT, PASTE_DUPLICATE as PASTE_DUPLICATE

class CanvasConnectionMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, connection) -> None: ...

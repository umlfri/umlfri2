from ..base.contextmenu import ContextMenu as ContextMenu
from ..properties import PropertiesDialog as PropertiesDialog
from umlfri2.application import Application as Application
from umlfri2.application.commands.diagram import ChangeZOrderCommand as ChangeZOrderCommand, DuplicateSnippetCommand as DuplicateSnippetCommand, HideElementsCommand as HideElementsCommand, PasteSnippetCommand as PasteSnippetCommand, ShowConnectionCommand as ShowConnectionCommand, ZOrderDirection as ZOrderDirection
from umlfri2.application.commands.model import DeleteElementsCommand as DeleteElementsCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT as DELETE_FROM_PROJECT, PASTE_DUPLICATE as PASTE_DUPLICATE, Z_ORDER_LOWER as Z_ORDER_LOWER, Z_ORDER_RAISE as Z_ORDER_RAISE, Z_ORDER_TO_BOTTOM as Z_ORDER_TO_BOTTOM, Z_ORDER_TO_TOP as Z_ORDER_TO_TOP
from umlfri2.metamodel import DefaultElementAction as DefaultElementAction
from umlfri2.qtgui.base import image_loader as image_loader

class CanvasElementMenu(ContextMenu):
    def __init__(self, main_window, drawing_area, elements) -> None: ...

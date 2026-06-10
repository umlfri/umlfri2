from ..base.contextmenu import ContextMenu as ContextMenu
from ..properties import PropertiesDialog as PropertiesDialog
from umlfri2.application import Application as Application
from umlfri2.application.commands.model import CreateDiagramCommand as CreateDiagramCommand, CreateElementCommand as CreateElementCommand, DeleteElementsCommand as DeleteElementsCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT as DELETE_FROM_PROJECT
from umlfri2.qtgui.base.image_loader import load_icon as load_icon

class ProjectTreeElementMenu(ContextMenu):
    def __init__(self, main_window, element) -> None: ...

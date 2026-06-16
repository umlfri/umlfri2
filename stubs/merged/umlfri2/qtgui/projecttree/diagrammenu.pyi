from ..base.contextmenu import ContextMenu as ContextMenu
from ..properties import PropertiesDialog as PropertiesDialog
from umlfri2.application import Application as Application
from umlfri2.application.commands.model import DeleteDiagramCommand as DeleteDiagramCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT as DELETE_FROM_PROJECT

class ProjectTreeDiagramMenu(ContextMenu):
    def __init__(self, main_window, diagram) -> None: ...

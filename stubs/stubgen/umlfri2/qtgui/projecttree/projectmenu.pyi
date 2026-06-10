from ..base.contextmenu import ContextMenu as ContextMenu
from ..properties import ProjectPropertiesDialog as ProjectPropertiesDialog
from umlfri2.application import Application as Application
from umlfri2.application.commands.model import CreateElementCommand as CreateElementCommand
from umlfri2.qtgui.properties import PropertiesDialog as PropertiesDialog

class ProjectTreeProjectMenu(ContextMenu):
    def __init__(self, main_window, project) -> None: ...

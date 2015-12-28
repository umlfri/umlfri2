from functools import partial

from PySide.QtGui import QMenu

from umlfri2.application import Application
from umlfri2.application.commands.model import CreateElementCommand
from umlfri2.qtgui.base import image_loader
from umlfri2.qtgui.properties import ProjectPropertiesDialog


class ProjectTreeProjectMenu(QMenu):
    def __init__(self, main_window, project): 
        super().__init__()
        
        self.__main_window = main_window
        self.__project = project
        
        metamodel = project.metamodel
        translation = metamodel.addon.get_translation(Application().language)
        
        sub_menu = self.addMenu(_("Add element"))
        for element_type in metamodel.element_types:
            action = sub_menu.addAction(translation.translate(element_type))
            action.setIcon(image_loader.load_icon(element_type.icon))
            action.triggered.connect(partial(self.__create_element_action, element_type))
        
        self.addSeparator()
        
        self.addAction(_("Properties...")).triggered.connect(self.__open_project_properties_action)
    
    def __create_element_action(self, element_type, checked=False):
        command = CreateElementCommand(self.__project, element_type)
        Application().commands.execute(command)
    
    def __open_project_properties_action(self, checked=False):
        ProjectPropertiesDialog.open_for(self.__main_window, self.__project)

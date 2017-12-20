from umlfri2.application import Application
from umlfri2.application.commands.model import CreateElementCommand
from umlfri2.qtgui.properties import PropertiesDialog
from ..base.contextmenu import ContextMenu
from ..properties import ProjectPropertiesDialog


class ProjectTreeProjectMenu(ContextMenu):
    def __init__(self, main_window, project): 
        super().__init__()
        
        self.__main_window = main_window
        self.__project = project
        
        metamodel = project.metamodel

        direct_element_types = [element_type for element_type in metamodel.element_types if element_type.allow_direct_add]
        if any(direct_element_types):
            for element_type in direct_element_types:
                self._add_type_menu_item(element_type, self.__create_element_action, format=_("Add '{0}'"))
        else:
            sub_menu = self._add_sub_menu_item(_("Add Element"))
            for element_type in metamodel.element_types:
                self._add_type_menu_item(element_type, self.__create_element_action, sub_menu)
        
        self.addSeparator()
        
        self._add_menu_item(None, _("Metamodel config..."), None, self.__open_metamodel_config_action)
        
        self.addSeparator()
        
        self._add_menu_item(None, _("Properties..."), None, self.__open_project_properties_action)
    
    def __create_element_action(self, element_type, checked=False):
        command = CreateElementCommand(self.__project, element_type)
        Application().commands.execute(command)
    
    def __open_project_properties_action(self, checked=False):
        ProjectPropertiesDialog.open_for(self.__main_window, self.__project)
    
    def __open_metamodel_config_action(self, checked=False):
        PropertiesDialog.open_config(self.__main_window, self.__project.metamodel)

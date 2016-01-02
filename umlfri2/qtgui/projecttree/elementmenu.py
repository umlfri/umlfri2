from functools import partial

from umlfri2.application import Application
from umlfri2.application.commands.model import CreateElementCommand, CreateDiagramCommand, DeleteElementsCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT
from ..base.contextmenu import ContextMenu
from ..properties import PropertiesDialog


class ProjectTreeElementMenu(ContextMenu):
    def __init__(self, main_window, element): 
        super().__init__()
        
        self.__main_window = main_window
        self.__element = element
        
        metamodel = element.project.metamodel
        
        sub_menu = self._add_sub_menu_item(_("Add diagram"))
        for diagram_type in metamodel.diagram_types:
            self._add_type_menu_item(diagram_type, self.__create_diagram_action, sub_menu)
        
        sub_menu = self._add_sub_menu_item(_("Add element"))
        for element_type in metamodel.element_types:
            self._add_type_menu_item(element_type, self.__create_element_action, sub_menu)
        
        self.addSeparator()
        
        diagrams = [visual.diagram for visual in element.visuals]
        sub_menu = self._add_sub_menu_item(_("Show in diagram"), len(diagrams) > 0)
        for diagram in diagrams:
            self._add_menu_item(None, diagram.get_display_name(), None,
                                partial(self.__show_in_diagram, diagram), sub_menu)
        
        self._add_menu_item("edit-delete", _("Delete"), DELETE_FROM_PROJECT, self.__delete_element_action)
        
        self.addSeparator()
        
        if self.__element.has_ufl_dialog:
            self._add_menu_item(None, _("Properties..."), None, self.__open_properties_action)
        else:
            self._add_menu_item(None, _("Properties..."), None)
    
    def __create_element_action(self, element_type, checked=False):
        command = CreateElementCommand(self.__element, element_type)
        Application().commands.execute(command)
    
    def __create_diagram_action(self, element_type, checked=False):
        command = CreateDiagramCommand(self.__element, element_type)
        Application().commands.execute(command)
        Application().tabs.select_tab(command.diagram)
    
    def __show_in_diagram(self, diagram, checked=False):
        tab = Application().tabs.select_tab(diagram)
        tab.drawing_area.selection.select(diagram.get_visual_for(self.__element))
    
    def __delete_element_action(self, checked=False):
        command = DeleteElementsCommand([self.__element])
        Application().commands.execute(command)
    
    def __open_properties_action(self, checked=False):
        PropertiesDialog.open_for(self.__main_window, self.__element)

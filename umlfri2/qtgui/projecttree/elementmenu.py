from functools import partial

from PySide.QtGui import QMenu, QIcon, QKeySequence

from umlfri2.application import Application
from umlfri2.application.commands.model import CreateElementCommand, CreateDiagramCommand, DeleteElementsCommand
from umlfri2.constants.keys import DELETE_FROM_PROJECT
from umlfri2.qtgui.base import image_loader
from umlfri2.qtgui.properties import PropertiesDialog


class ProjectTreeElementMenu(QMenu):
    def __init__(self, main_window, element): 
        super().__init__()
        
        self.__main_window = main_window
        self.__element = element
        
        metamodel = element.project.metamodel
        translation = metamodel.addon.get_translation(Application().language)
        
        sub_menu = self.addMenu(_("Add diagram"))
        for diagram_type in metamodel.diagram_types:
            action = sub_menu.addAction(translation.translate(diagram_type))
            action.setIcon(image_loader.load_icon(diagram_type.icon))
            action.triggered.connect(partial(self.__create_diagram_action, diagram_type))
        
        sub_menu = self.addMenu(_("Add element"))
        for element_type in metamodel.element_types:
            action = sub_menu.addAction(translation.translate(element_type))
            action.setIcon(image_loader.load_icon(element_type.icon))
            action.triggered.connect(partial(self.__create_element_action, element_type))
        
        self.addSeparator()
        
        diagrams = [visual.diagram for visual in element.visuals]
        action = self.addAction(_("Show in diagram"))
        if len(diagrams) == 0:
            action.setEnabled(False)
        sub_menu = QMenu()
        action.setMenu(sub_menu)
        for diagram in diagrams:
            action = sub_menu.addAction(diagram.get_display_name())
            action.setIcon(image_loader.load_icon(diagram.type.icon))
            action.triggered.connect(partial(self.__show_in_diagram, diagram))
        
        action = self.addAction(_("Delete"))
        action.setIcon(QIcon.fromTheme("edit-delete"))
        action.setShortcut(QKeySequence(DELETE_FROM_PROJECT))
        action.triggered.connect(self.__delete_element_action)
        
        self.addSeparator()
        
        action = self.addAction(_("Properties..."))
        if self.__element.has_ufl_dialog:
            action.triggered.connect(self.__open_properties_action)
        else:
            action.setEnabled(False)
    
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

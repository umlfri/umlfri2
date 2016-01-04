from PySide.QtGui import QTableWidget, QTabWidget

from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent, ItemSelectedEvent
from umlfri2.application.events.diagram import SelectionChangedEvent
from umlfri2.application.events.model import ObjectDataChangedEvent, ProjectChangedEvent
from umlfri2.application.events.tabs import ChangedCurrentTabEvent
from umlfri2.model import Project
from umlfri2.ufl.dialog import UflDialogOptions, UflDialogObjectTab, UflDialogValueTab
from .emptytab import EmptyTab
from .objecttab import ObjectTab
from .projecttab import ProjectTab
from .texttab import TextTab


class PropertiesWidget(QTabWidget):
    def __init__(self, main_window):
        super().__init__()
        
        self.__main_window = main_window
        
        self.setTabPosition(QTabWidget.South)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        Application().event_dispatcher.subscribe(ItemSelectedEvent, lambda event: self.__select_item(event.item))
        Application().event_dispatcher.subscribe(ObjectDataChangedEvent,
                                                 lambda event: self.__item_changed(event.object))
        Application().event_dispatcher.subscribe(ProjectChangedEvent,
                                                 lambda event: self.__item_changed(event.project))
        Application().event_dispatcher.subscribe(SelectionChangedEvent, self.__selection_changed)
        Application().event_dispatcher.subscribe(ChangedCurrentTabEvent, self.__tab_changed)
        
        self.__item = None
        self.__dialog = None
        self.__select_item(None)
    
    def __item_changed(self, item):
        if item is self.__item:
            self.__select_item(item)
    
    def __selection_changed(self, event):
        if event.diagram is Application().tabs.current_tab.drawing_area.diagram:
            self.__select_selection(event.selection)
    
    def __tab_changed(self, event):
        if event.tab is not None:
            self.__select_selection(event.tab.drawing_area.selection)
    
    def __select_selection(self, selection):
        if selection.is_diagram_selected:
            self.__select_item(selection.selected_diagram)
        elif selection.is_connection_selected:
            self.__select_item(selection.selected_connection.object)
        else:
            elements = list(selection.selected_elements)
            if len(elements) == 1:
                self.__select_item(elements[0].object)
            else:
                self.__select_item(None)
    
    def __select_item(self, item):
        self.__item = item
        
        for no in range(self.count()):
            self.removeTab(0)
        
        if isinstance(item, Project):
            self.addTab(ProjectTab(item), None)
            self.__dialog = None
        elif item is not None and item.has_ufl_dialog:
            self.__dialog = item.create_ufl_dialog(UflDialogOptions.list)
            for tab in self.__dialog.tabs:
                if isinstance(tab, UflDialogObjectTab):
                    self.addTab(ObjectTab(self.__main_window, tab, self.__dialog), None)
                elif isinstance(tab, UflDialogValueTab):
                    self.addTab(TextTab(tab, self.__dialog), None)
        else:
            self.addTab(EmptyTab(), None)
            self.__dialog = None
        
        self.__reload_texts()
    
    def __reload_texts(self):
        if self.__dialog is not None:
            self.__dialog.translate(self.__item.type.metamodel.addon.get_translation(Application().language))
        for no in range(self.count()):
            self.setTabText(no, self.widget(no).label)
            self.widget(no).reload_texts()

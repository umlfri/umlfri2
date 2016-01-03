from PySide.QtGui import QTableWidget, QTabWidget

from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent, ItemSelectedEvent
from umlfri2.application.events.model import ObjectDataChangedEvent, ProjectChangedEvent
from umlfri2.model import Project
from .emptytab import EmptyTab
from .projecttab import ProjectTab


class PropertiesWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.setTabPosition(QTabWidget.South)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        Application().event_dispatcher.subscribe(ItemSelectedEvent, lambda event: self.select_item(event.item))
        Application().event_dispatcher.subscribe(ObjectDataChangedEvent,
                                                 lambda event: self.__item_changed(event.object))
        Application().event_dispatcher.subscribe(ProjectChangedEvent,
                                                 lambda event: self.__item_changed(event.project))
        
        self.__item = None
        self.select_item(None)
    
    def __item_changed(self, item):
        if item is self.__item:
            self.select_item(item)
    
    def select_item(self, item):
        self.__item = item
        
        for no in range(self.count()):
            self.removeTab(0)
        
        if item is None:
            self.addTab(EmptyTab(), None)
        elif isinstance(item, Project):
            self.addTab(ProjectTab(item), None)
        else:
            self.addTab(EmptyTab(), None)
        
        self.__reload_texts()
    
    def __reload_texts(self):
        for no in range(self.count()):
            self.setTabText(no, self.widget(no).label)
            self.widget(no).reload_texts()

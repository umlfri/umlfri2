import sip

from PyQt5.QtWidgets import QWidget, QVBoxLayout

from umlfri2.application import Application
from umlfri2.application.events.tabs import ChangedCurrentTabEvent
from .toolbox import ToolBox


class MainToolBox(QWidget):
    def __init__(self):
        super().__init__()
        
        self.__layout = QVBoxLayout()
        self.__layout.setContentsMargins(0, 0, 0, 0)

        self.__toolbox = ToolBox(None, True)
        self.__layout.addWidget(self.__toolbox)
        
        self.setLayout(self.__layout)
        
        Application().event_dispatcher.subscribe(ChangedCurrentTabEvent, self.__current_tab_changed)
    
    def __current_tab_changed(self, event):
        self.__layout.removeWidget(self.__toolbox)
        sip.delete(self.__toolbox)
        
        if event.tab is None:
            self.__toolbox = ToolBox(None, True)
        else:
            self.__toolbox = ToolBox(event.tab.drawing_area, True)

        self.__layout.addWidget(self.__toolbox)

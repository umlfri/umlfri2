from PySide.QtGui import QTableWidget, QTabWidget

from umlfri2.application import Application
from umlfri2.application.events.application import LanguageChangedEvent


class PropertiesWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.__table = QTableWidget()
        self.__table.setColumnCount(2)
        self.__table.horizontalHeader().setStretchLastSection(True)
        self.setTabPosition(QTabWidget.South)
        self.addTab(self.__table, None)
        
        Application().event_dispatcher.subscribe(LanguageChangedEvent, lambda event: self.__reload_texts())
        
        self.__reload_texts()
    
    def __reload_texts(self):
        self.__table.setHorizontalHeaderLabels([_("Name"), _("Value")])
        self.setTabText(0, _("Properties"))

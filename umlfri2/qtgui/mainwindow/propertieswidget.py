from PySide.QtGui import QTableWidget, QTabWidget


class PropertiesWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.__table = QTableWidget()
        self.__table.setColumnCount(2)
        self.__table.horizontalHeader().setStretchLastSection(True)
        self.setTabPosition(QTabWidget.South)
        self.addTab(self.__table, None)
        self.reload_texts()
    
    def reload_texts(self):
        self.__table.setHorizontalHeaderLabels([_("Name"), _("Value")])
        self.setTabText(0, _("Properties"))

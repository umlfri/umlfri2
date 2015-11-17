from PySide.QtGui import QTableWidget, QTabWidget


class PropertiesWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        
        self.__table = QTableWidget()
        self.__table.setColumnCount(2)
        self.__table.setHorizontalHeaderLabels(["Name", "Value"])
        self.__table.horizontalHeader().setStretchLastSection(True)
        self.setTabPosition(QTabWidget.South)
        self.addTab(self.__table, "Properties")

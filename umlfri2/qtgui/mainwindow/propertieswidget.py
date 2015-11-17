from PySide.QtGui import QTableWidget


class PropertiesWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["Name", "Value"])
        self.horizontalHeader().setStretchLastSection(True)
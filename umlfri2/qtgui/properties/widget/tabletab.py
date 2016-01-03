from PySide.QtGui import QTableWidget, QTableWidgetItem


class TableTab(QTableWidget):
    def __init__(self):
        super().__init__()
        
        self.setColumnCount(2)
        self.verticalHeader().hide()
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setHighlightSections(False)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
    
    def reload_texts(self):
        self.setHorizontalHeaderLabels([_("Name"), _("Value")])
    
    @property
    def label(self):
        raise Exception

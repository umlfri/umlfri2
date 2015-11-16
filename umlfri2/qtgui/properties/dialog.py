from PySide.QtCore import QSize, Qt
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QTabWidget
from .listtab import ListPropertyTab
from .objecttab import ObjectPropertyTab
from umlfri2.ufl.dialog import UflDialogListTab, UflDialogObjectTab


class PropertiesDialog(QDialog):
    def __init__(self, main_window, dialog): 
        super().__init__(main_window)
        self.__main_window = main_window
        self.setWindowTitle("Properties")
        self.__dialog = dialog
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        tab = dialog.get_lonely_tab()
        if isinstance(tab, UflDialogListTab):
            layout.addWidget(ListPropertyTab(self, tab))
        elif isinstance(tab, UflDialogObjectTab):
            layout.addWidget(ObjectPropertyTab(self, tab))
        else:
            tabs = QTabWidget()
            tabs.setFocusPolicy(Qt.NoFocus)
            
            for tab in dialog.tabs:
                if isinstance(tab, UflDialogListTab):
                    tabs.addTab(ListPropertyTab(self, tab), tab.name)
                elif isinstance(tab, UflDialogObjectTab):
                    tabs.addTab(ObjectPropertyTab(self, tab), tab.name)
            layout.addWidget(tabs)
        
        layout.addWidget(buttonBox)
        self.setLayout(layout)
    
    def sizeHint(self):
        orig = super().sizeHint()
        return QSize(500, orig.height())

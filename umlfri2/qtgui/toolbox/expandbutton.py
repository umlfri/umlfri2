from PyQt5.QtCore import QEvent, Qt, pyqtSignal
from PyQt5.QtWidgets import QPushButton


class ExpandButton(QPushButton):
    expanded_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.setFocusPolicy(Qt.NoFocus)
        
        self.clicked.connect(self.__click)
        
        self.expanded = True
        
        self.setFlat(True)
    
    @property
    def expanded(self):
        return self.__expanded
    
    @expanded.setter
    def expanded(self, value):
        self.__expanded = value
        
        if self.__expanded:
            self.setText("«")
        else:
            self.setText("»")
        
        self.expanded_changed.emit()

    def event(self, e):
        if e.type() == QEvent.HoverEnter:
            self.setFlat(False)
        elif e.type() == QEvent.HoverLeave:
            self.setFlat(True)
        return super().event(e)
    
    def __click(self, checked=False):
        self.expanded = not self.expanded

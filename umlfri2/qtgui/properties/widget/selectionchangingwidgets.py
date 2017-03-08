from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QPushButton, QComboBox, QSpinBox, QLineEdit


class QSelectionChangingCheckBox(QCheckBox):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)


class QSelectionChangingPushButton(QPushButton):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)


class QSelectionChangingComboBox(QComboBox):
    lostFocus = pyqtSignal(str)
    
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)
    
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        
        self.lostFocus.emit(self.currentText())


class QSelectionChangingSpinBox(QSpinBox):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)


class QSelectionChangingLineEdit(QLineEdit):
    lostFocus = pyqtSignal(str)
    
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)
    
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        
        self.lostFocus.emit(self.text())

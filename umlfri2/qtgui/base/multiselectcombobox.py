from PySide.QtCore import Qt, Signal
from PySide.QtGui import QComboBox, QStandardItemModel, QStyledItemDelegate, QStyle, QStandardItem, QStylePainter, \
    QPalette, QStyleOptionComboBox


class MultiSelectComboBox(QComboBox):
    check_changed = Signal(int, bool)
    
    class __CheckingStyledItemDelegate(QStyledItemDelegate):
        def paint(self, painter, option, index):
            option.showDecorationSelected = False
            option.state &= ~QStyle.State_HasFocus & ~QStyle.State_MouseOver
    
            super().paint(painter, option, index)
    
    def __init__(self):
        super().__init__()
        
        self.__model = QStandardItemModel()
        self.__model.dataChanged.connect(self.__data_changed)
        self.setModel(self.__model)
        self.setItemDelegate(self.__CheckingStyledItemDelegate())
        self.__checked = []
    
    def paintEvent(self, event):
        painter = QStylePainter(self)
        
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        
        selected = []
        
        for index in range(self.__model.rowCount()):
            item = self.__model.item(index)
            if item.checkState() == Qt.Checked:
                selected.append(item.text())
        
        opt.currentText = " | ".join(selected)
        
        painter.drawComplexControl(QStyle.CC_ComboBox, opt)
        painter.drawControl(QStyle.CE_ComboBoxLabel, opt)
    
    def add_check_item(self, checked, text):
        item = QStandardItem(text)
        item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        if checked:
            item.setData(Qt.Checked, Qt.CheckStateRole)
        else:
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.__model.appendRow(item)
        self.__checked.append(checked)
    
    def set_item_text(self, index, text):
        item = self.__model.item(index)
        item.setText(text)
    
    def set_item_checked(self, index, checked):
        item = self.__model.item(index)
        if checked:
            item.setData(Qt.Checked, Qt.CheckStateRole)
        else:
            item.setData(Qt.Unchecked, Qt.CheckStateRole)
        
        self.__checked[index] = checked
    
    def __data_changed(self, top_left, bottom_right):
        index = top_left.row()
        item = self.__model.item(index)
        
        checked = item.checkState() == Qt.Checked
        
        if checked != self.__checked[index]:
            self.__checked[index] = checked
            self.check_changed.emit(index, checked)
            
            self.update()

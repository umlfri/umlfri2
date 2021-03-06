from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

from umlfri2.qtgui.base.colorwidget import ColorSelectionWidget
from umlfri2.qtgui.base.fontwidget import FontSelectionWidget
from umlfri2.qtgui.base.multiselectcombobox import MultiSelectComboBox
from ..dialog import PropertiesDialog
from .selectionchangingwidgets import QSelectionChangingCheckBox, QSelectionChangingPushButton, \
    QSelectionChangingComboBox, QSelectionChangingSpinBox, QSelectionChangingLineEdit, QSelectionChangingDoubleSpinBox
from umlfri2.ufl.dialog import *
from .tabletab import TableTab


class ObjectTab(TableTab):
    __tab = None
    
    def __init__(self, main_window, widget, tab):
        super().__init__()
        
        self.__main_window = main_window
        self.__widget = widget
        
        self.setRowCount(tab.widget_count)
        self.currentCellChanged.connect(self.__cell_changed)
        
        for no, widget in enumerate(tab.widgets):
            if isinstance(widget, UflDialogNullableWidget):
                qt_nullable_checkbox = QSelectionChangingCheckBox(self, no)
                qt_nullable_checkbox.stateChanged.connect(partial(self.__nullable_state_changed, widget, no))
                self.setCellWidget(no, 0, qt_nullable_checkbox)
                self.setCellWidget(no, 1, self.__build_qt_widget(no, widget.inner_widget))
            else:
                self.setCellWidget(no, 1, self.__build_qt_widget(no, widget))
        
        self.content_updated()
        
        self.__tab = tab
    
    def __build_qt_widget(self, no, widget):
        if isinstance(widget, UflDialogCheckWidget):
            qt_widget = QSelectionChangingCheckBox(self, no)
            qt_widget.stateChanged.connect(partial(self.__state_changed, widget))
        elif isinstance(widget, UflDialogChildWidget):
            qt_widget = QSelectionChangingPushButton(self, no)
            qt_widget.clicked.connect(partial(self.__show_dialog, widget))
        elif isinstance(widget, UflDialogColorWidget):
            qt_widget = ColorSelectionWidget(btn_class=partial(QSelectionChangingPushButton, self, no))
            qt_widget.color_changed.connect(partial(self.__value_changed, widget))
        elif isinstance(widget, UflDialogComboWidget):
            qt_widget = QSelectionChangingComboBox(self, no)
            qt_widget.setEditable(True)
            for item in widget.possibilities:
                qt_widget.addItem(item)
            qt_widget.editTextChanged.connect(partial(self.__value_changed, widget))
            qt_widget.lostFocus.connect(partial(self.__value_changed, widget))
        elif isinstance(widget, UflDialogFontWidget):
            qt_widget = FontSelectionWidget(btn_class=partial(QSelectionChangingPushButton, self, no))
            qt_widget.font_changed.connect(partial(self.__value_changed, widget))
        elif isinstance(widget, UflDialogIntegerWidget):
            qt_widget = QSelectionChangingSpinBox(self, no)
            qt_widget.valueChanged[int].connect(partial(self.__value_changed, widget))
        elif isinstance(widget, UflDialogDecimalWidget):
            qt_widget = QSelectionChangingDoubleSpinBox(self, no)
            qt_widget.valueChanged[float].connect(partial(self.__value_changed, widget))
        elif isinstance(widget, UflDialogMultiSelectWidget):
            qt_widget = MultiSelectComboBox()
            for checked, item in widget.possibilities:
                qt_widget.add_check_item(checked, item)
            qt_widget.check_changed.connect(partial(self.__multi_changed, widget))
        elif isinstance(widget, UflDialogSelectWidget):
            qt_widget = QSelectionChangingComboBox(self, no)
            for item in widget.possibilities:
                qt_widget.addItem(item)
            qt_widget.currentIndexChanged[int].connect(partial(self.__index_changed, widget))
        elif isinstance(widget, UflDialogTextWidget):
            qt_widget = QSelectionChangingLineEdit(self, no)
            qt_widget.lostFocus.connect(partial(self.__value_changed, widget))
            qt_widget.returnPressed.connect(partial(self.__value_accepted, widget, qt_widget))
        else:
            raise Exception()
        
        return qt_widget
    
    def __cell_changed(self, row, column, prev_row, prev_column):
        widget = self.cellWidget(row, 1)
        if widget is not None:
            widget.setFocus()
    
    def __show_dialog(self, widget, checked=False):
        PropertiesDialog(self.__main_window, widget.dialog, None).exec_()
        self.__widget.apply()
    
    def __nullable_state_changed(self, widget, no, state):
        widget.is_null = state == Qt.Unchecked
        qt_widget = self.cellWidget(no, 1)
        qt_widget.setEnabled(not widget.is_null)
        
        self.__widget.apply()
    
    def __state_changed(self, widget, state):
        widget.value = state == Qt.Checked
        self.__widget.apply()
    
    def __value_changed(self, widget, value):
        widget.value = value
        self.__widget.apply()
    
    def __multi_changed(self, widget, index, checked):
        if checked:
            widget.check(index)
        else:
            widget.uncheck(index)
        self.__widget.apply()
    
    def __index_changed(self, widget, index):
        widget.current_index = index
        self.__widget.apply()
    
    def __value_accepted(self, widget, qt_widget):
        widget.value = qt_widget.text()
        self.__widget.apply()
    
    def reload_data(self):
        for no, widget in enumerate(self.__tab.widgets):
            qt_widget = self.cellWidget(no, 1)
            if isinstance(widget, UflDialogNullableWidget):
                qt_nullable_checkbox = self.cellWidget(no, 0)
                qt_nullable_checkbox.setChecked(not widget.is_null)
                qt_widget.setEnabled(not widget.is_null)
                self.__reload_widget_data(qt_widget, widget.inner_widget)
            else:
                self.__reload_widget_data(qt_widget, widget)
        
        self.content_updated()
    
    def __reload_widget_data(self, qt_widget, widget):
        if isinstance(widget, UflDialogCheckWidget):
            qt_widget.setChecked(widget.value)
        elif isinstance(widget, UflDialogChildWidget):
            pass
        elif isinstance(widget, UflDialogColorWidget):
            qt_widget.selected_color = widget.value
        elif isinstance(widget, UflDialogComboWidget):
            qt_widget.setEditText(widget.value)
        elif isinstance(widget, UflDialogFontWidget):
            qt_widget.selected_font = widget.value
        elif isinstance(widget, UflDialogIntegerWidget):
            qt_widget.setValue(widget.value)
        elif isinstance(widget, UflDialogDecimalWidget):
            qt_widget.setValue(widget.value)
        elif isinstance(widget, UflDialogMultiSelectWidget):
            for no, (checked, possibility) in enumerate(widget.possibilities):
                qt_widget.set_item_checked(no, checked)
        elif isinstance(widget, UflDialogSelectWidget):
            qt_widget.setCurrentIndex(widget.current_index)
        elif isinstance(widget, UflDialogTextWidget):
            qt_widget.setText(widget.value)
        else:
            raise Exception()
    
    def reload_texts(self):
        super().reload_texts()
        
        for no, widget in enumerate(self.__tab.widgets):
            qt_widget = self.cellWidget(no, 1)
            
            if isinstance(widget, UflDialogNullableWidget):
                qt_nullable_checkbox = self.cellWidget(no, 0)
                qt_nullable_checkbox.setText(widget.label)
                
                self.__reload_widget_text(widget.inner_widget, qt_widget)
            else:
                label = QTableWidgetItem(widget.label)
                label.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.setItem(no, 0, label)
                
                self.__reload_widget_text(widget, qt_widget)
        
        self.content_updated()
    
    def __reload_widget_text(self, widget, qt_widget):
        if isinstance(widget, UflDialogChildWidget):
            qt_widget.setText(_("Edit..."))
        elif isinstance(widget, UflDialogSelectWidget):
            for no, possibility in enumerate(widget.possibilities):
                qt_widget.setItemText(no, possibility)
        elif isinstance(widget, UflDialogMultiSelectWidget):
            for no, (checked, possibility) in enumerate(widget.possibilities):
                qt_widget.set_item_text(no, possibility)
    
    @property
    def label(self):
        if self.__tab.name is None:
            return _("General")
        else:
            return self.__tab.name

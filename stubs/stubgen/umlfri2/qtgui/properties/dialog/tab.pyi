from umlfri2.ufl.dialog import *
from .smalltextedit import SmallTextEdit as SmallTextEdit
from PyQt5.QtWidgets import QWidget
from umlfri2.qtgui.base.colorwidget import ColorSelectionWidget as ColorSelectionWidget
from umlfri2.qtgui.base.fontwidget import FontSelectionWidget as FontSelectionWidget
from umlfri2.qtgui.base.multiselectcombobox import MultiSelectComboBox as MultiSelectComboBox
from umlfri2.qtgui.base.selectalldoublespinbox import SelectAllDoubleSpinBox as SelectAllDoubleSpinBox
from umlfri2.qtgui.base.selectalllineedit import SelectAllLineEdit as SelectAllLineEdit
from umlfri2.qtgui.base.selectallspinbox import SelectAllSpinBox as SelectAllSpinBox

class PropertyTab(QWidget):
    def __init__(self, window, tab) -> None: ...
    def refresh(self) -> None: ...

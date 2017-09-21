from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QComboBox, QFormLayout, QRadioButton

from umlfri2.application import Application
from umlfri2.constants.languages import AVAILABLE_LANGUAGES


class SettingsDialogGeneral(QWidget):
    def __init__(self, dialog):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        
        self.__language_gb = QGroupBox()
        layout.addWidget(self.__language_gb)

        self.__language_selector = QComboBox()

        current_language_id = Application().config.language
        
        for no, (lang_id, label) in enumerate(AVAILABLE_LANGUAGES):
            self.__language_selector.addItem(label)
            if lang_id == current_language_id:
                self.__language_selector.setCurrentIndex(no)

        self.__use_system = QRadioButton()
        self.__use_custom = QRadioButton()
        self.__use_custom.toggled.connect(self.__use_custom_changed)
        
        if current_language_id is None:
            self.__use_system.setChecked(True)
            self.__language_selector.setEnabled(False)
        else:
            self.__use_custom.setChecked(True)
        
        language_layout = QFormLayout()
        language_layout.addRow(self.__use_system)
        language_layout.addRow(self.__use_custom, self.__language_selector)

        self.__language_gb.setLayout(language_layout)
        
        self.setLayout(layout)
        
        self.reload_texts()
    
    def __use_custom_changed(self, checked):
        self.__language_selector.setEnabled(checked)
    
    @staticmethod
    def get_name():
        return _("General")
    
    def apply_settings(self):
        if self.__use_system.isChecked():
            Application().language.change_language(None)
        else:
            selected_no = self.__language_selector.currentIndex()
            
            Application().language.change_language(AVAILABLE_LANGUAGES[selected_no][0])
    
    def reload_texts(self):
        self.__use_system.setText(_("Use system language"))
        self.__use_custom.setText(_("Custom language"))
        self.__language_gb.setTitle(_("Application language"))

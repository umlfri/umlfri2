from PyQt5.QtWidgets import QDialog, QFormLayout, QSpinBox, QCheckBox, QDialogButtonBox, QVBoxLayout

from umlfri2.application import Application


class ExportDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        
        self.setWindowTitle(_("Export Options"))
        
        dialog_layout = QVBoxLayout()
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout = QFormLayout()
        
        self.__zoom = QSpinBox()
        self.__zoom.setValue(Application().config.export_zoom)
        
        self.__padding = QSpinBox()
        self.__padding.setValue(Application().config.export_padding)
        
        self.__transparent = QCheckBox(_("Copy without background (transparent)"))
        self.__transparent.setChecked(True)
        
        layout.addRow(_("Zoom") + ":", self.__zoom)
        layout.addRow(_("Padding") + ":", self.__padding)
        layout.addRow(self.__transparent)
        
        dialog_layout.addLayout(layout)
        dialog_layout.addWidget(button_box)
        
        self.setLayout(dialog_layout)
    
    def done(self, dialog_code):
        if dialog_code == ExportDialog.Accepted:
            Application().config.set_export_options(self.__zoom.value(), self.__padding.value())
        super().done(dialog_code)
    
    @property
    def zoom(self):
        return self.__zoom.value()
    
    @property
    def padding(self):
        return self.__padding.value()
    
    @property
    def transparent(self):
        return self.__transparent.isChecked()

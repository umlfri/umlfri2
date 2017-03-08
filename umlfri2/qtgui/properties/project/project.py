from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QFormLayout, QLineEdit

from umlfri2.application import Application
from umlfri2.application.commands.model import ChangeProjectNameCommand


class ProjectPropertiesDialog(QDialog):
    def __init__(self, main_window, project): 
        super().__init__(main_window)
        self.__project = project
        self.__main_window = main_window
        self.setWindowTitle(_("Properties"))
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
        button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
        apply_button = button_box.button(QDialogButtonBox.Apply)
        apply_button.setText(_("Apply"))
        apply_button.clicked.connect(self.__apply_clicked)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.__name_text = QLineEdit()
        self.__name_text.setText(project.name)
        form_layout.addRow(_("Name"), self.__name_text)
        
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def sizeHint(self):
        orig = super().sizeHint()
        return QSize(500, orig.height())
    
    @property
    def project_name(self):
        return self.__name_text.text()
    
    def __apply_clicked(self, checked=False):
        command = ChangeProjectNameCommand(self.__project, self.project_name)
        Application().commands.execute(command)
    
    @staticmethod
    def open_for(main_window, project):
        qt_dialog = ProjectPropertiesDialog(main_window, project)
        qt_dialog.setModal(True)
        if qt_dialog.exec_() == ProjectPropertiesDialog.Accepted:
            command = ChangeProjectNameCommand(project, qt_dialog.project_name)
            Application().commands.execute(command)

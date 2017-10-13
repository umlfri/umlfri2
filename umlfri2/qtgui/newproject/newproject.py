import html

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QListWidget, QLabel, QSizePolicy, \
    QListWidgetItem, QCheckBox, QLineEdit, QFormLayout, QFrame
from umlfri2.application import Application
from umlfri2.qtgui.base import image_loader


class TemplateItem(QListWidgetItem):
    def __init__(self, template):
        translation = template.metamodel.get_translation(Application().language.current_language)
        super().__init__(translation.translate(template))
        self.setIcon(image_loader.load_icon(template.icon))
        self.__template = template
    
    @property
    def template(self):
        return self.__template


class NewProjectDialog(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle(_("New Project"))
        self.__main_window = main_window
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        self.__ok_button = button_box.button(QDialogButtonBox.Ok)
        
        layout = QVBoxLayout()
        
        self.__templates = QListWidget()
        self.__templates.setViewMode(QListWidget.IconMode)
        self.__templates.setMovement(QListWidget.Static)
        self.__templates.currentItemChanged.connect(self.__selection_changed)
        self.__templates.itemDoubleClicked.connect(self.__selection_double_clicked)
        
        self.__description = QLabel()
        self.__description.setBackgroundRole(QPalette.Base)
        self.__description.setAutoFillBackground(True)
        self.__description.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.__description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__description.setAlignment(Qt.AlignTop)
        self.__description.setWordWrap(True)
        
        self.__project_name = QLineEdit()
        self.__project_name.setText(_("Project"))
        self.__project_name.textChanged.connect(self.__name_changed)
        project_name_layout = QFormLayout()
        project_name_layout.addRow(_("Project &name:"), self.__project_name)
        
        self.__new_solution = QCheckBox(_("Create a new &solution"))
        self.__new_solution.setChecked(True)
        
        if Application().solution is None:
            self.__new_solution.setEnabled(False)
        
        layout.addWidget(self.__templates)
        layout.addWidget(self.__description)
        layout.addLayout(project_name_layout)
        layout.addWidget(self.__new_solution)
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        for template in Application().templates:
            self.__templates.addItem(TemplateItem(template))
        
        self.__templates.setCurrentRow(0)
    
    def sizeHint(self):
        return QSize(600, 400)
    
    def __selection_changed(self, current, previous):
        text = "<font size=+2><b>{0}</b></font><br>".format(current.template.addon.name)
        text += "<i>{0}: {1}</i><br>".format(_("Metamodel version"), current.template.addon.version)
        text += "<p>" + html.escape(current.template.addon.description).replace('\n', '</p><p>') + "</p>"
        self.__description.setText(text)
    
    def __name_changed(self, text):
        self.__ok_button.setEnabled(text != "")
    
    def __selection_double_clicked(self, item):
        self.accept()
    
    @property
    def selected_template(self):
        return self.__templates.selectedItems()[0].template
    
    @property
    def new_solution(self):
        return self.__new_solution.isChecked()
    
    @property
    def project_name(self):
        return self.__project_name.text()
    
    @staticmethod
    def open_dialog(main_window):
        qt_dialog = NewProjectDialog(main_window)
        qt_dialog.setModal(True)
        if qt_dialog.exec_() == NewProjectDialog.Accepted:
            return qt_dialog
        return None

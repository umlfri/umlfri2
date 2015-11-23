import html

from PySide.QtCore import Qt, QSize
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QListWidget, QLabel, QFont, QPalette, QSizePolicy, \
    QListWidgetItem, QScrollArea

from umlfri2.application import Application
from ..base import image_loader


class TemplateItem(QListWidgetItem):
    def __init__(self, template):
        super().__init__(template.name)
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
        
        layout = QVBoxLayout()
        
        self.__templates = QListWidget()
        self.__templates.setViewMode(QListWidget.IconMode)
        self.__templates.setMovement(QListWidget.Static)
        self.__templates.currentItemChanged.connect(self.__selection_changed)
        
        self.__description = QLabel()
        self.__description.setStyleSheet("background-color: white")
        self.__description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__description.setAlignment(Qt.AlignTop)
        self.__description.setWordWrap(True)
        
        layout.addWidget(self.__templates)
        layout.addWidget(self.__description)
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        for template in Application().templates:
            self.__templates.addItem(TemplateItem(template))
        
        self.__templates.setCurrentRow(0)
    
    def sizeHint(self):
        return QSize(600, 400)
    
    def __selection_changed(self, current, previous):
        text = "<font size=+2><b>{0}</b></font><br>".format(current.template.addon.name)
        text += "<i>Metamodel version: {0}</i><br>".format(current.template.addon.version)
        text += "<p>" + html.escape(current.template.addon.description).replace('\n', '</p><p>') + "</p>"
        self.__description.setText(text)
    
    @staticmethod
    def open_dialog(main_window):
        qt_dialog = NewProjectDialog(main_window)
        qt_dialog.setModal(True)
        if qt_dialog.exec_() == NewProjectDialog.Accepted:
            pass

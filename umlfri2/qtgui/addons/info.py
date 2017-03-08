from html import escape

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QLabel, QFormLayout

from umlfri2.qtgui.base import image_loader


class AddOnInfo(QDialog):
    def __init__(self, addon_window, addon):
        super().__init__(addon_window)
        self.__addon = addon

        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.button(QDialogButtonBox.Close).setText(_("Close"))
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        
        hbox_caption = QHBoxLayout()
        
        if addon.icon:
            icon = QLabel()
            icon.setPixmap(image_loader.load(addon.icon))
            hbox_caption.addWidget(icon, 0)
        
        nameWidget = QLabel('<font size="+2"><b>{0}</b></font>&nbsp;&nbsp;&nbsp;&nbsp;{1}'.format(escape(addon.name), addon.version))
        hbox_caption.addWidget(nameWidget, 1)
        
        layout.addLayout(hbox_caption, 0)
        
        info = QFormLayout()
        
        info.addRow(_("Author") + ":", QLabel(addon.author))
        homepageWidget = QLabel('<a href="{0}">{0}</a>'.format(escape(addon.homepage)))
        homepageWidget.setTextInteractionFlags(Qt.TextBrowserInteraction)
        homepageWidget.setOpenExternalLinks(True)
        info.addRow(_("Homepage") + ":", homepageWidget)
        
        if addon.license.title:
            license = "{0} ({1})".format(addon.license.title, addon.license.abbreviation)
        else:
            license = addon.license.abbreviation
        
        license = escape(license)
        
        if addon.license.url:
            license = '<a href="{0}">{1}</a>'.format(addon.license.url, license)
        
        licenseWidget = QLabel(license)
        licenseWidget.setTextInteractionFlags(Qt.TextBrowserInteraction)
        licenseWidget.setOpenExternalLinks(True)
        info.addRow(_("License") + ":", licenseWidget)
        
        if addon.description:
            info.addRow(QLabel(_("Description") + ":"))
            descriptionWidget = QLabel(escape(addon.description))
            descriptionWidget.setWordWrap(True)
            info.addRow(descriptionWidget)
        
        layout.addLayout(info, 1)
        
        layout.addWidget(button_box)
        
        self.setLayout(layout)
    
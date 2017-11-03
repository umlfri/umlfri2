from html import escape

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QFormLayout, QWidget

from umlfri2.application.addon.online import OnlineAddOn
from umlfri2.qtgui.base import image_loader


class AddOnInfoWidget(QWidget):
    def __init__(self, addon):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        hbox_caption = QHBoxLayout()
        
        if addon.icon:
            icon = QLabel()
            icon.setPixmap(image_loader.load(addon.icon))
            hbox_caption.addWidget(icon, 0)
        
        if isinstance(addon, OnlineAddOn):
            version = addon.latest_version.version
        else:
            version = addon.version
        
        name_widget = QLabel('<font size="+2"><b>{0}</b></font>&nbsp;&nbsp;&nbsp;&nbsp;{1}'.format(escape(addon.name), version))
        hbox_caption.addWidget(name_widget, 1)
        
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
        
        license_widget = QLabel(license)
        license_widget.setTextInteractionFlags(Qt.TextBrowserInteraction)
        license_widget.setOpenExternalLinks(True)
        info.addRow(_("License") + ":", license_widget)
        
        if addon.description:
            info.addRow(QLabel(_("Description") + ":"))
            description_widget = QLabel(escape(addon.description))
            description_widget.setWordWrap(True)
            info.addRow(description_widget)
        
        layout.addLayout(info, 1)
        
        self.setLayout(layout)

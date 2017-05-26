import os.path

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QDialogButtonBox, QTabWidget, \
    QTextEdit, QGridLayout, QFormLayout, QScrollArea, QWidget, QPushButton

from umlfri2.application import Application
from umlfri2.constants.paths import GRAPHICS, LICENSE_FILE


class About(QDialog):
    def __init__(self, main_window):
        super().__init__(main_window)
        
        self.setWindowTitle(_("About UML .FRI"))
        
        main_layout = QVBoxLayout()
        
        desc_layout = QHBoxLayout()

        logo_pixmap = QPixmap()
        logo_pixmap.load(os.path.join(GRAPHICS, "logo", "logo_full.png"))
        
        logo = QLabel()
        logo.setPixmap(logo_pixmap)
        
        desc_layout.addWidget(logo, 0, Qt.AlignTop)
        
        desc_text_layout = QVBoxLayout()
        
        desc_text_layout.addWidget(QLabel("<h1>{0}</h1>".format(Application().about.name)))
        desc_text_layout.addWidget(QLabel("{0} {1}".format(_("Version"), Application().about.version)))
        desc_text_layout.addItem(QSpacerItem(0, 20))
        desc_label = QLabel(Application().about.description)
        desc_label.setWordWrap(True)
        desc_text_layout.addWidget(desc_label)
        desc_text_layout.addStretch(1)
        for author, year in Application().about.author:
            desc_text_layout.addWidget(QLabel("<small>{0}</small>".format(self.__about_line(author, year))))
        
        desc_layout.addLayout(desc_text_layout, 1)
        
        main_layout.addLayout(desc_layout)
        
        tabs = QTabWidget()
        main_layout.addWidget(tabs, 1)
        
        versions_layout = QFormLayout()
        
        for depencency, version in Application().about.dependency_versions:
            versions_layout.addRow(_("{0} version").format(depencency), QLabel(version))
        
        versions_widget = QWidget()
        versions_widget.setLayout(versions_layout)
        tabs.addTab(versions_widget, _("Used libraries"))
        
        if os.path.exists(LICENSE_FILE):
            license_text = QTextEdit()
            with open(LICENSE_FILE, 'rt') as license_file:
                license_text.setPlainText(license_file.read())
            license_text.setReadOnly(True)
            license_text.setLineWrapMode(QTextEdit.NoWrap)
            
            tabs.addTab(license_text, _("License"))
        
        version_1_layout = QVBoxLayout()
        
        for author, year in Application().about.version_1_contributions:
            version_1_layout.addWidget(QLabel(self.__about_line(author, year)))
        
        version_1_widget = QWidget()
        version_1_widget.setLayout(version_1_layout)
        version_1_scroll = QScrollArea()
        version_1_scroll.setWidget(version_1_widget)
        tabs.addTab(version_1_scroll, _("Version 1.0 contributions"))
        
        updates_layout = QGridLayout()
        updates_widget = QWidget()
        updates_widget.setLayout(updates_layout)
        
        check_updates = QPushButton(_("Check for updates"))
        updates_layout.addWidget(check_updates, 0, 0)

        updates_layout.addWidget(QLabel(_("Latest version available:")), 1, 0)
        if Application().about.updates.latest_version is None:
            updates_layout.addWidget(QLabel("-"), 1, 1)
        else:
            updates_layout.addWidget(QLabel(str(Application().about.updates.latest_version)), 1, 1)
        
        if Application().about.updates.has_newer_version:
            updates_layout.addWidget(QLabel("<a href=\"{0}\">{1}</a>".format(
                Application().about.updates.version_update_url, _("download update")
            )), 1, 2)

        if Application().about.updates.latest_prerelease is not None:
            updates_layout.addWidget(QLabel(_("Latest unstable version available:")), 2, 0)
            updates_layout.addWidget(QLabel(str(Application().about.updates.latest_prerelease)), 2, 1)
    
            if Application().about.updates.has_newer_version:
                updates_layout.addWidget(QLabel("<a href=\"{0}\">{1}</a>".format(
                    Application().about.updates.prerelease_update_url, _("download update")
                )), 2, 2)
        
        tabs.addTab(updates_widget, _("Updates"))
        
        if Application().about.is_debug_version:
            debug_layout = QHBoxLayout()
            debug_icon = QLabel()
            debug_icon.setPixmap(QIcon.fromTheme("dialog-warning").pixmap(QSize(16, 16)))
            debug_layout.addWidget(debug_icon)
            debug_text = QLabel(_("You are running UML .FRI in the debug mode"))
            debug_layout.addWidget(debug_text, 1)
            main_layout.addLayout(debug_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        button_box.accepted.connect(self.accept)
        
        main_layout.addWidget(button_box)
        
        self.setLayout(main_layout)

    def __about_line(self, author, year):
        line = "© "
        if isinstance(year, tuple):
            line += "{0}-{1} ".format(year[0], year[1])
        else:
            line += "{0} ".format(author[1])
        line += author
        return line

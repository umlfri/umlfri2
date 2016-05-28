import os.path

from PySide.QtGui import QApplication, QIcon


def find_gtk_rc():
    for path in "~/.gtkrc-2.0", "~/.config/gtkrc-2.0", "/etc/gtk-2.0/gtkrc":
        gtkrc = os.path.expanduser(path)
        
        if os.path.exists(gtkrc):
            return gtkrc


def set_gtk_icon_theme():
    gtkrc = find_gtk_rc()
    
    if gtkrc is None:
        return
    
    with open(gtkrc, "r") as gtkrc_file:
        for line in gtkrc_file:
            line = line.strip()
            if line.startswith('#'):
                continue
            
            if '=' not in line:
                continue
            
            name, value = line.split('=', 1)
            
            name = name.strip()
            value = value.strip().strip('"')
            
            if name == "gtk-icon-theme-name":
                QIcon.setThemeName(value)
                return

    QIcon.setThemeName("gnome")


def set_gtk_icon_theme_if_needed():
    if QApplication.instance().style().objectName() == 'gtk+':
        set_gtk_icon_theme()

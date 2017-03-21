import os.path
import appdirs

APP_DIRS = appdirs.AppDirs('umlfri2')

ROOT_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))

XML_SCHEMAS = os.path.join(ROOT_DIR, 'data', 'schema')
GRAPHICS = os.path.join(ROOT_DIR, 'data', 'graphics')
ADDONS = os.path.join(ROOT_DIR, 'addons')
LOCAL_ADDONS = os.path.join(APP_DIRS.user_data_dir, 'addons')
CONFIG = APP_DIRS.user_config_dir
NT_ICON_THEME_PATH = os.path.join(ROOT_DIR, 'data', 'icons')
NT_ICON_THEME = 'oxygen'
LOCALE_DIR = os.path.join(ROOT_DIR, 'data', 'locale')
LICENSE_FILE = os.path.join(ROOT_DIR, 'LICENSE.txt')

#!/usr/bin/env python3
import re
try:
    from importlib._bootstrap_external import _code_to_bytecode
except ImportError:
    from importlib._bootstrap import _code_to_bytecode

import os
import os.path
import sys
import zipfile
import shutil
import compileall
import glob

########################################
# Config
# VERSION_TYPE = 'Debug'
VERSION_TYPE = 'Release'
########################################


def print_h1(text):
    print()
    print(text)
    print('='*len(text))


def print_h2(text):
    print()
    print(text)
    print('-'*len(text))


print_h1("Initialization")

DIR = os.path.abspath(os.path.dirname(__file__))
UML_FRI_DIR = os.path.abspath(os.path.join(DIR, '..', '..'))

OUT_DIR = os.path.join(DIR, 'out')
INSTALL_DIR = os.path.join(DIR, 'installer')

print("Detected directories:")
print("- UML .FRI directory: {}".format(UML_FRI_DIR))
print("- Output directory: {}".format(OUT_DIR))

sys.path.append(UML_FRI_DIR)
from umlfri2.application.about import AboutUmlFri


UMLFRI_VERSION = AboutUmlFri.version

print('Detected UML .FRI version: {}'.format(UMLFRI_VERSION))


class UmlFriZip:
    def __init__(self, zip_name, base_path):
        self.__base_path = base_path
        self.__zip_file = zipfile.ZipFile(os.path.join(OUT_DIR, zip_name), mode='w', compression=zipfile.ZIP_DEFLATED)

    def __enter__(self):
        self.__zip_file.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__zip_file.__exit__(exc_type, exc_val, exc_tb)

    def __add_pyc_to_zip(self, root, file_name):
        dir = os.path.relpath(os.path.dirname(root), self.__base_path).replace('\\', '/')

        file_content = open(os.path.join(root, file_name), 'rb').read()

        new_file_name = file_name.split('.', 2)[0] + '.pyc'

        if dir == '.':
            file_path = new_file_name
        else:
            file_path = '{}/{}'.format(dir, new_file_name)
        self.__zip_file.writestr(file_path, file_content)

    def add_compiled_to_zip(self, path, source):
        codeobject = compile(source, path, 'exec')

        bytecode = _code_to_bytecode(codeobject)
        self.__zip_file.writestr(path, bytecode)

    def process_python_directory(self, dir=None, ignore=lambda x, y: set()):
        if dir is None:
            walked_dir = self.__base_path
        else:
            walked_dir = os.path.join(self.__base_path, dir)

        for root, dirs, files in os.walk(walked_dir):
            if os.path.basename(root) != '__pycache__':
                continue

            for file in set(files) - ignore(root, files):
                if file.endswith('.opt-2.pyc'):
                    self.__add_pyc_to_zip(root, file)

if os.path.exists(OUT_DIR):
    print("Old output directory is being removed")
    shutil.rmtree(OUT_DIR)

print("Creating the new output directory")
os.mkdir(OUT_DIR)

print_h1("UML .FRI source processing")
print_h2("Compilation")

compileall.compile_dir(os.path.join(UML_FRI_DIR, 'umlfri2'), optimize=2)

print_h2("Paths modification")
paths_path = os.path.join(UML_FRI_DIR, 'umlfri2', 'constants', 'paths.py')
paths_file = open(paths_path, 'r').read()
paths_file = re.sub('^ROOT_DIR = .*$', 'import sys; ROOT_DIR = os.path.normpath(os.path.dirname(sys.executable))', paths_file, flags=re.MULTILINE)

print_h2("Packing")
with UmlFriZip('umlfri.zip', UML_FRI_DIR) as zip:
    zip.process_python_directory('umlfri2', ignore=shutil.ignore_patterns("paths.*"))
    zip.add_compiled_to_zip('umlfri2/constants/paths.pyc', paths_file)

print_h2("pl_runner packing")
pl_runner_path = os.path.join(UML_FRI_DIR, 'addons', 'python_starter', 'starter', 'python_runner.py')
pl_runner_file = open(pl_runner_path, 'r').read()
with UmlFriZip('pl_runner.zip', UML_FRI_DIR) as zip:
    zip.add_compiled_to_zip('python_runner.pyc', pl_runner_file)

print_h1("Python binaries processing")
print("- UML .FRI binary")
print("  - Using " + VERSION_TYPE)
shutil.copy(os.path.join(DIR, 'stub', VERSION_TYPE, 'umlfri2.exe'), os.path.join(OUT_DIR, 'umlfri2.exe'))

print("- Python dlls")
shutil.copy(os.path.join(sys.base_prefix, 'python36.dll'), os.path.join(OUT_DIR, 'python36.dll'))
shutil.copy(os.path.join(sys.base_prefix, 'python3.dll'), os.path.join(OUT_DIR, 'python3.dll'))

if VERSION_TYPE == 'Debug':
    shutil.copy(os.path.join('c:\\', 'Windows', 'SysWOW64', 'vcruntime140d.dll'), os.path.join(OUT_DIR, 'vcruntime140d.dll'))
    shutil.copy(os.path.join('c:\\', 'Windows', 'SysWOW64', 'ucrtbased.dll'), os.path.join(OUT_DIR, 'ucrtbased.dll'))
else:
    shutil.copy(os.path.join('c:\\', 'Windows', 'SysWOW64', 'vcruntime140.dll'), os.path.join(OUT_DIR, 'vcruntime140.dll'))
    shutil.copy(os.path.join('c:\\', 'Windows', 'SysWOW64', 'ucrtbase.dll'), os.path.join(OUT_DIR, 'ucrtbase.dll'))

print_h1("Python standard library")
print_h2("Copying into temp")

for dll_path in glob.glob(os.path.join('c:\\', 'Windows', 'SysWOW64', 'downlevel', 'api-ms-win-crt-*')):
    dll_name = os.path.basename(dll_path)
    shutil.copy(dll_path, os.path.join(OUT_DIR, dll_name))

for dll_path in glob.glob(os.path.join('c:\\', 'Windows', 'SysWOW64', 'downlevel', 'api-ms-win-core-*')):
    dll_name = os.path.basename(dll_path)
    shutil.copy(dll_path, os.path.join(OUT_DIR, dll_name))

shutil.copytree(os.path.join(sys.base_prefix, 'Lib'), os.path.join(OUT_DIR, 'python'), ignore=shutil.ignore_patterns("__pycache__", "site-packages", "test", "idlelib", "tkinter", "turtledemo", "turtle.py"))

print_h2("Compilation")
compileall.compile_dir(os.path.join(OUT_DIR, 'python'), optimize=2)

print_h2("Packing")
with UmlFriZip('python.zip', os.path.join(OUT_DIR, 'python')) as zip:
    zip.process_python_directory()

print_h2("Removing the temp")
shutil.rmtree(os.path.join(OUT_DIR, 'python'))

print_h2("Copying dlls")
shutil.copytree(os.path.join(sys.base_prefix, 'DLLs'), os.path.join(OUT_DIR, 'dlls'), ignore=shutil.ignore_patterns("*.ico", "*.cat", "_test*", "_tkinter.*"))

print_h1("Libraries and data")
print_h2("Copying UML .FRI data")
shutil.copytree(os.path.join(UML_FRI_DIR, 'data'), os.path.join(OUT_DIR, 'data'), ignore=shutil.ignore_patterns("128x128", "256x256", "api", "*.svg", "icon", "tool_icons"))
shutil.copy(os.path.join(UML_FRI_DIR, 'LICENSE.txt'), os.path.join(OUT_DIR, 'LICENSE.txt'))
shutil.copy(os.path.join(UML_FRI_DIR, 'CHANGELOG.md'), os.path.join(OUT_DIR, 'CHANGELOG.md'))

print_h2("Appdirs lib")
import appdirs
shutil.copy(appdirs.__file__, os.path.join(OUT_DIR, 'dlls', 'appdirs.py'))

print_h2("Pyparsing lib")
import pyparsing
shutil.copy(pyparsing.__file__, os.path.join(OUT_DIR, 'dlls', 'pyparsing.py'))

print_h2("Lxml lib")
import lxml
shutil.copytree(os.path.dirname(lxml.__file__), os.path.join(OUT_DIR, 'dlls', 'lxml'), ignore=shutil.ignore_patterns("*.h", "includes", "__pycache__"))

print_h2("PyQt+Qt libs")
import sip
shutil.copy(sip.__file__, os.path.join(OUT_DIR, 'dlls', 'sip.pyd'))

import PyQt5
shutil.copytree(os.path.dirname(PyQt5.__file__), os.path.join(OUT_DIR, 'dlls', 'PyQt5'), ignore=shutil.ignore_patterns("__pycache__", "qml", "resources", "translations", "uic",
    "Qt*Bluetooth.*", "Qt*CLucene.*", "Qt*DBus.*", "Qt*Designer.*", "Qt*Help.*", "Qt*Location.*", "Qt*Multimedia.*", "Qt*MultimediaWidgets.*", "Qt*Network.*", "Qt*Nfc.*",
    "Qt*Positioning.*", "Qt*Qml.*", "Qt*Quick.*", "Qt*QuickControls2.*", "Qt*QuickParticles.*", "Qt*QuickTemplates2.*", "Qt*QuickTest.*", "Qt*QuickWidgets.*", "Qt*Sensors.*",
    "Qt*SerialPort.*", "Qt*Sql.*", "Qt*Test.*", "Qt*WebEngine.*", "Qt*WebEngineCore.*", "Qt*WebEngineWidgets.*", "Qt*WebChannel.*", "Qt*WebSockets.*",
    "concrt140.dll", "libeay32.dll", "libEGL.dll", "libGLESv2.dll", "QtWebEngineProcess.exe", "ssleay32.dll",
    "audio", "bearer", "generic", "geoservices", "iconengines", "mediaservice", "qminimal.dll", "qoffscreen.dll", "playlistformats", "position", "sceneparsers", "sensorgestures",
    "sensors", "sqldrivers"))

print_h2("Sentry SDK with dependencies")
import sentry_sdk
import urllib3
import certifi
shutil.copytree(os.path.dirname(sentry_sdk.__file__), os.path.join(OUT_DIR, 'dlls', 'sentry_sdk'), ignore=shutil.ignore_patterns("__pycache__"))
shutil.copytree(os.path.dirname(urllib3.__file__), os.path.join(OUT_DIR, 'dlls', 'urllib3'), ignore=shutil.ignore_patterns("__pycache__"))
shutil.copytree(os.path.dirname(certifi.__file__), os.path.join(OUT_DIR, 'dlls', 'certifi'), ignore=shutil.ignore_patterns("__pycache__", "__main__.py"))

print_h2("Compiling dependencies")
compileall.compile_dir(os.path.join(OUT_DIR, 'dlls'), optimize=2)

print()
print_h1("Addons")
print_h2("Creating directory")
os.mkdir(os.path.join(OUT_DIR, 'addons'))

print_h2("Infjavauml")
shutil.copytree(os.path.join(UML_FRI_DIR, 'addons', 'infjavauml'), os.path.join(OUT_DIR, 'addons', 'infjavauml'))

print_h2("Python starter")
shutil.copytree(os.path.join(UML_FRI_DIR, 'addons', 'python_starter'), os.path.join(OUT_DIR, 'addons', 'python_starter'), ignore=shutil.ignore_patterns('__pycache__', 'python_runner.py', 'libraryTemplate'))

print_h2("Compiling addons")
compileall.compile_dir(os.path.join(OUT_DIR, 'addons'), optimize=2)

print_h1("Saving INNO SETUP config")
with open(os.path.join(INSTALL_DIR, 'config.iss'), 'w') as iss_config:
    print_h2("Version")
    print('#define MyAppVersion "{0}"'.format(UMLFRI_VERSION), file=iss_config)

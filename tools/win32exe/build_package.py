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

########################################
# Config
#version = 'Debug'
version = 'Release'
########################################

print("Initialization")
print("==============")

DIR = os.path.abspath(os.path.dirname(__file__))
UML_FRI_DIR = os.path.abspath(os.path.join(DIR, '..', '..'))

OUT_DIR = os.path.join(DIR, 'out')

print("Detected directories:")
print("- UML .FRI directory: {}".format(UML_FRI_DIR))
print("- Output directory: {}".format(OUT_DIR))

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

print()
print("UML .FRI source processing")
print("==========================")
print("Compilation")
print("-----------")
compileall.compile_dir(os.path.join(UML_FRI_DIR, 'umlfri2'), optimize=2)

print()
print("Paths modification")
print("------------------")
paths_path = os.path.join(UML_FRI_DIR, 'umlfri2', 'constants', 'paths.py')
paths_file = open(paths_path, 'r').read()
paths_file = re.sub('^ROOT_DIR = .*$', 'import sys; ROOT_DIR = os.path.normpath(os.path.dirname(sys.executable))', paths_file, flags=re.MULTILINE)

print("Packing")
print("-------")
with UmlFriZip('umlfri.zip', UML_FRI_DIR) as zip:
    zip.process_python_directory('umlfri2', ignore=shutil.ignore_patterns("paths.*"))
    zip.add_compiled_to_zip('umlfri2/constants/paths.pyc', paths_file)

print("pl_runner packing")
print("-----------------")
pl_runner_path = os.path.join(UML_FRI_DIR, 'addons', 'python_starter', 'starter', 'python_runner.py')
pl_runner_file = open(pl_runner_path, 'r').read()
with UmlFriZip('pl_runner.zip', UML_FRI_DIR) as zip:
    zip.add_compiled_to_zip('python_runner.pyc', pl_runner_file)

print("Python binaries processing")
print("==========================")
print("- UML .FRI binary")
print("  - Using " + version)
shutil.copy(os.path.join(DIR, 'stub', version, 'umlfri2.exe'), os.path.join(OUT_DIR, 'umlfri2.exe'))

print("- Python dlls")
shutil.copy(os.path.join(sys.base_prefix, 'python36.dll'), os.path.join(OUT_DIR, 'python36.dll'))
shutil.copy(os.path.join(sys.base_prefix, 'python3.dll'), os.path.join(OUT_DIR, 'python3.dll'))

if version == 'Debug':
    shutil.copy(os.path.join('c:', 'Windows', 'SysWOW64', 'vcruntime140d.dll'), os.path.join(OUT_DIR, 'vcruntime140d.dll'))
    shutil.copy(os.path.join('c:', 'Windows', 'SysWOW64', 'ucrtbased.dll'), os.path.join(OUT_DIR, 'ucrtbased.dll'))
else:
    shutil.copy(os.path.join('c:', 'Windows', 'SysWOW64', 'vcruntime140.dll'), os.path.join(OUT_DIR, 'vcruntime140.dll'))
    shutil.copy(os.path.join('c:', 'Windows', 'SysWOW64', 'ucrtbase.dll'), os.path.join(OUT_DIR, 'ucrtbase.dll'))

print("Python standard library")
print("=======================")
print("Copying into temp")
print("-----------------")
shutil.copytree(os.path.join(sys.base_prefix, 'Lib'), os.path.join(OUT_DIR, 'python'), ignore=shutil.ignore_patterns("__pycache__", "site-packages", "test", "idlelib", "tkinter", "turtledemo", "turtle.py"))

print("Compilation")
print("-----------")
compileall.compile_dir(os.path.join(OUT_DIR, 'python'), optimize=2)

print()
print("Packing")
print("-------")
with UmlFriZip('python.zip', os.path.join(OUT_DIR, 'python')) as zip:
    zip.process_python_directory()

print("Removing the temp")
print("-----------------")
shutil.rmtree(os.path.join(OUT_DIR, 'python'))

print("Copying dlls")
print("------------")
shutil.copytree(os.path.join(sys.base_prefix, 'DLLs'), os.path.join(OUT_DIR, 'dlls'), ignore=shutil.ignore_patterns("*.ico", "*.cat", "_test*", "_tkinter.*"))

print("Libraries and data")
print("==================")
print("Copying UML .FRI data")
print("---------------------")
shutil.copytree(os.path.join(UML_FRI_DIR, 'data'), os.path.join(OUT_DIR, 'data'), ignore=shutil.ignore_patterns("128x128", "256x256", "api", "*.svg", "icon", "tool_icons"))
shutil.copy(os.path.join(UML_FRI_DIR, 'LICENSE.txt'), os.path.join(OUT_DIR, 'LICENSE.txt'))

print("Appdirs lib")
print("-----------")
import appdirs
shutil.copy(appdirs.__file__, os.path.join(OUT_DIR, 'dlls', 'appdirs.py'))

print("Pyparsing lib")
print("-------------")
import pyparsing
shutil.copy(pyparsing.__file__, os.path.join(OUT_DIR, 'dlls', 'pyparsing.py'))

print("Lxml lib")
print("--------")
import lxml
shutil.copytree(os.path.dirname(lxml.__file__), os.path.join(OUT_DIR, 'dlls', 'lxml'), ignore=shutil.ignore_patterns("*.h", "includes", "__pycache__"))

print("PyQt+Qt libs")
print("------------")
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

print("Compiling dependencies")
print("----------------------")
compileall.compile_dir(os.path.join(OUT_DIR, 'dlls'), optimize=2)

print()
print("Addons")
print("======")
print("Creating directory")
print("------------------")
os.mkdir(os.path.join(OUT_DIR, 'addons'))

print("Infjavauml")
print("----------")
shutil.copytree(os.path.join(UML_FRI_DIR, 'addons', 'infjavauml'), os.path.join(OUT_DIR, 'addons', 'infjavauml'))

print("Python starter")
print("----------")
shutil.copytree(os.path.join(UML_FRI_DIR, 'addons', 'python_starter'), os.path.join(OUT_DIR, 'addons', 'python_starter'), ignore=shutil.ignore_patterns('__pycache__', 'python_runner.py', 'libraryTemplate'))

print("Compiling addons")
print("----------------")
compileall.compile_dir(os.path.join(OUT_DIR, 'addons'), optimize=2)

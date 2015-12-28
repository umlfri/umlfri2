#!/usr/bin/python3

import os
import os.path
import re
import tarfile
import urllib.request
import zipfile
from io import BytesIO

import shutil

TOOLS_PATH = os.path.dirname(__file__)


class TarReader:
    def __init__(self, tar):
        self.__tar = tarfile.open(fileobj=tar, mode='r:*')

    def get_names(self):
        for file in self.__tar.getmembers():
            if file.isfile():
                yield file.name

    def read(self, file):
        return self.__tar.extractfile(file).read()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__tar.__exit__(exc_type, exc_val, exc_tb)


class ZipReader:
    def __init__(self, zip):
        self.__zip = zipfile.ZipFile(zip)

    def get_names(self):
        for name in self.__zip.namelist():
            if not name.endswith('/'):
                yield name

    def read(self, file):
        return self.__zip.read(file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__zip.__exit__(exc_type, exc_val, exc_tb)


def extract_theme(theme_dir, url, reader, remove_dirs):
    re_underscored = re.compile(b'^_', re.MULTILINE)

    tar = urllib.request.urlopen(url)

    out = os.path.join(TOOLS_PATH, "..", "..", "data", "icons", theme_dir)
    if os.path.isdir(out):
        shutil.rmtree(out)

    tar = BytesIO(tar.read())
    with reader(tar) as tar:
        for file in tar.get_names():
            if file.endswith('.png'):
                dirname = os.path.join(out, *os.path.dirname(file).split('/')[remove_dirs:]) # remove n first directories
                basename = os.path.basename(file)
                try:
                    os.makedirs(dirname)
                except os.error:
                    pass
                content = tar.read(file)
                with open(os.path.join(dirname, basename), 'wb') as icon:
                    icon.write(content)
            elif file.endswith('/index.theme.in') or file.endswith('/index.theme'):
                content = tar.read(file)
                content = re_underscored.sub(b'', content)
                with open(os.path.join(out, 'index.theme'), 'wb') as index:
                    index.write(content)


def extract_tango_theme():
    re_actual_file = re.compile(b'<a href="(tango-icon-theme-[0-9]+[0-9\.]+[0-9]+.tar.gz)">')

    releases = urllib.request.urlopen("http://tango.freedesktop.org/releases/").read()
    last_release = re_actual_file.findall(releases)[-1].decode('ascii')

    extract_theme("tango", "http://tango.freedesktop.org/releases/{0}".format(last_release), TarReader, 1)


def extract_oxygen_theme():
    extract_theme("oxygen", "https://github.com/pasnox/oxygen-icons-png/archive/master.zip", ZipReader, 2)


extract_oxygen_theme()
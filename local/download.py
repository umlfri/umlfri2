import os
import os.path
import re
import shlex
import tarfile
import urllib.request
from io import BytesIO

import shutil

LOCAL_PATH = os.path.dirname(__file__)


def extract_theme():
    out = os.path.join(LOCAL_PATH, "tango")

    if os.path.isdir(out):
        shutil.rmtree(out)

    re_actual_file = re.compile(b'<a href="(tango-icon-theme-[0-9]+[0-9\.]+[0-9]+.tar.gz)">')
    re_underscored = re.compile(b'^_', re.MULTILINE)

    releases = urllib.request.urlopen("http://tango.freedesktop.org/releases/").read()
    last_release = re_actual_file.findall(releases)[-1].decode('ascii')
    tar = urllib.request.urlopen("http://tango.freedesktop.org/releases/{0}".format(last_release))
    tar = BytesIO(tar.read())
    with tarfile.open(fileobj=tar, mode='r:*') as tar:
        for file in tar.getmembers():
            if file.name.endswith('.png') and file.isfile():
                dirname = os.path.join(out, *os.path.dirname(file.name).split('/')[1:]) # remove first directory
                basename = os.path.basename(file.name)
                try:
                    os.makedirs(dirname)
                except os.error:
                    pass
                content = tar.extractfile(file).read()
                with open(os.path.join(dirname, basename), 'wb') as icon:
                    icon.write(content)
            elif file.name.endswith('/index.theme.in'):
                content = tar.extractfile(file).read()
                content = re_underscored.sub(b'', content)
                with open(os.path.join(out, 'index.theme'), 'wb') as index:
                    index.write(content)


extract_theme()

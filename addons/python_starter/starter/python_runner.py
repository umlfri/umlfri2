#!/usr/bin/python
import sys

import os

pin = int(os.environ['UMLFRI_PIN'])
pout = int(os.environ['UMLFRI_POUT'])

if os.name == 'nt':
    import msvcrt
    pin = msvcrt.open_osfhandle(pin, os.O_RDONLY)
    pout = msvcrt.open_osfhandle(pout, os.O_APPEND)

sys.path.insert(0, os.environ['UMLFRI_PATH'])
sys.path.append(os.environ['UMLFRI_LIB'])

from org.umlfri.api.implementation import Server, FileChannel, MIMChannel, StartupMessage
from org.umlfri.api.base import Application

fin = os.fdopen(pin, 'r')
fout = os.fdopen(pout, 'w')

channel = FileChannel(fin, fout)

if 'UMLFRI_PLUGIN_DEBUG' in os.environ:
    channel = MIMChannel(channel)

server = Server(channel)

import plugin

adapter=Application(server, 'app')
plugin.plugin_main(adapter)

server.start()

try:
    server.main_loop()
except KeyboardInterrupt:
    pass

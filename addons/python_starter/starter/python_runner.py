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

from org.umlfri.api.implementation import Server, FileChannel, MIMChannel
from org.umlfri.api.base import Application

fin = os.fdopen(pin, 'rb')
fout = os.fdopen(pout, 'wb')

channel = FileChannel(fin, fout)

if 'UMLFRI_PLUGIN_DEBUG' in os.environ:
    channel = MIMChannel(channel)

server = Server(channel)

import plugin

if hasattr(plugin, 'get_main_loop'):
    main_loop = plugin.get_main_loop()
else:
    main_loop = None


def main(args):
    server.start(main_loop)

    adapter=Application(server, 'app')
    plugin.plugin_main(adapter)

    try:
        server.main_loop()
    except KeyboardInterrupt:
        pass

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

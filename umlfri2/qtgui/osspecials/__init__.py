import os


if os.name == 'nt':
    from .win32 import apply as apply_os_specials
else:
    def apply_os_specials():
        pass

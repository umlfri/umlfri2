import platform


platform_name = platform.system()

if platform_name == 'Windows':
    from .win32 import Win32Specials
    SPECIALS = Win32Specials()
elif platform_name == 'Darwin':
    from .macosx import MacOsXSpecials
    SPECIALS = MacOsXSpecials()
else:
    from .base import OSSpecials
    SPECIALS = OSSpecials()

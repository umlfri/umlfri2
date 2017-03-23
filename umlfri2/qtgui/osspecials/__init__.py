import platform


platform_name = platform.system()

if platform_name == 'Windows':
    from .win32 import apply as apply_os_specials
elif platform_name == 'Darwin':
    from .macosx import apply as apply_os_specials
else:
    def apply_os_specials():
        pass

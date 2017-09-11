import ctypes
import gettext
import locale
import os

from .events.application import LanguageChangedEvent

from umlfri2.constants.paths import LOCALE_DIR


class LanguageManager:
    def __init__(self, application):
        self.__application = application
        self.__default_language = self.__find_out_system_language().split('.', 1)[0]
        self.change_language(application.config.language)

    def __find_out_system_language(self):
        for e in 'LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG':
            if e in os.environ:
                return os.environ[e]

        if os.name == 'nt':
            try:
                langid = ctypes.windll.kernel32.GetUserDefaultUILanguage()
                return locale.windows_locale[langid]
            except:
                pass

        try:
            lang, enc = locale.getlocale()
        except:
            lang = None

        if lang is not None:
            return lang

        try:
            lang, enc = locale.getdefaultlocale()
        except:
            lang = None

        if lang is not None:
            return lang

        return 'POSIX'

    def change_language(self, language):
        self.__application.config.language = language
        
        # install new language handler from gettext
        gettext.translation('umlfri2', localedir=LOCALE_DIR, languages=[self.current_language], fallback=True).install()
        self.__application.event_dispatcher.dispatch(LanguageChangedEvent(language))

    @property
    def current_language(self):
        if self.__application.config.language is None:
            return self.__default_language
        return self.__application.config.language

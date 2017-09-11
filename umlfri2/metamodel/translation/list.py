from .translation import POSIX_TRANSLATION


class TranslationList:
    def __init__(self, translations):
        self.__translations = {i.language: i for i in translations}

    def get_translation(self, language):
        ret = self.__translations.get(language, None)
        if ret is not None:
            return ret

        if '_' in language:
            language, variation = language.split('_', 2)

            ret = self.__translations.get(language, None)
            if ret is not None:
                return ret

        ret = self.__translations.get('en', None)
        if ret is not None:
            return ret

        return POSIX_TRANSLATION

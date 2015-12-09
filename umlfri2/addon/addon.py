from .translation import POSIX_TRANSLATION


class AddOn:
    def __init__(self, identifier, name, version, author, homepage, license, icon, description, config, translations, metamodel):
        self.__identifier = identifier
        self.__name = name
        self.__version = version
        self.__author = author
        self.__homepage = homepage
        self.__license = license
        self.__icon = icon
        self.__description = description
        self.__config_structure = config
        self.__config_structure.set_parent(None)
        self.__config = config.build_default(None)
        self.__translations = translations
        self.__metamodel = metamodel
        self.__metamodel._set_addon(self)
    
    @property
    def identifier(self):
        return self.__identifier
    
    @property
    def name(self):
        return self.__name
    
    @property
    def version(self):
        return self.__version
    
    @property
    def author(self):
        return self.__author
    
    @property
    def homepage(self):
        return self.__homepage
    
    @property
    def license(self):
        return self.__license
    
    @property
    def icon(self):
        return self.__icon
    
    @property
    def description(self):
        return self.__description
    
    @property
    def config_structure(self):
        return self.__config_structure
    
    @property
    def config(self):
        return self.__config
    
    @property
    def metamodel(self):
        return self.__metamodel
    
    def get_translation(self, language):
        ret = self.__get_translation(language)
        if ret is not None:
            return ret

        if '_' in language:
            language, variation = language.split('_', 2)

            ret = self.__get_translation(language)
            if ret is not None:
                return ret

        return POSIX_TRANSLATION

    def __get_translation(self, language):
        for translation in self.__translations:
            if translation.language == language:
                return translation

        return None

    def compile(self):
        self.__metamodel.compile()

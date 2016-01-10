from umlfri2.ufl.types import UflObjectType
from .translation import POSIX_TRANSLATION


class AddOn:
    def __init__(self, identifier, name, version, author, homepage, license, icon, description, dependencies, config,
                 translations, metamodel, toolbars, patch_plugin, plugin):
        self.__identifier = identifier
        self.__name = name
        self.__version = version
        self.__author = author
        self.__homepage = homepage
        self.__license = license
        self.__icon = icon
        self.__description = description
        self.__dependencies = tuple(dependencies)
        if config is None:
            self.__config_structure = UflObjectType({})
        else:
            self.__config_structure = config
        self.__config_structure.set_parent(None)
        self.__config = self.__config_structure.build_default(None)
        self.__translations = translations
        self.__metamodel = metamodel
        if self.__metamodel is not None:
            self.__metamodel._set_addon(self)
        self.__started = False
        self.__toolbars = tuple(toolbars)
        self.__patch_plugin = patch_plugin
        if self.__patch_plugin is not None:
            self.__patch_plugin._set_addon(self)
        self.__plugin = plugin
        if self.__plugin is not None:
            self.__plugin._set_addon(self)
    
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
    def dependencies(self):
        yield from self.__dependencies
    
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
        
        ret = self.__get_translation('en')
        if ret is not None:
            return ret
        
        return POSIX_TRANSLATION

    def __get_translation(self, language):
        for translation in self.__translations:
            if translation.language == language:
                return translation

        return None

    def compile(self):
        if self.__metamodel is not None:
            self.__metamodel.compile()
    
    @property
    def is_started(self):
        return self.__started
    
    @property
    def toolbars(self):
        yield from self.__toolbars
    
    def start(self):
        if self.__started:
            raise Exception
        self.__started = True
        if self.__patch_plugin is not None:
            self.__patch_plugin.start()
        if self.__plugin is not None:
            self.__plugin.start()
    
    def stop(self):
        if not self.__started:
            raise Exception
        self.__started = False
        if self.__patch_plugin is not None:
            self.__patch_plugin.stop()
        if self.__plugin is not None:
            self.__plugin.stop()

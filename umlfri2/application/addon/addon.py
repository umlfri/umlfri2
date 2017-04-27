from .starter import AddOnStarter
from .state import AddOnState
from .stopper import AddOnStopper
from umlfri2.application.events.addon import AddonStateChangedEvent
from umlfri2.ufl.types import UflObjectType
from .translation import POSIX_TRANSLATION


class AddOn:
    def __init__(self, application, identifier, name, version, author, homepage, license, icon, description,
                 requirements, provisions, config, translations, metamodel, gui_injection, patch_plugin, plugin,
                 system_addon):
        self.__application = application
        self.__identifier = identifier
        self.__name = name
        self.__version = version
        self.__author = author
        self.__homepage = homepage
        self.__license = license
        self.__icon = icon
        self.__description = description
        self.__requirements = tuple(requirements)
        self.__provisions = tuple(provisions)
        if config is None:
            self.__config_structure = UflObjectType({})
            self.__has_config = False
        else:
            self.__config_structure = config
            self.__has_config = True
        self.__config_structure.set_parent(None)
        self.__config = self.__config_structure.build_default(None)
        self.__translations = translations
        self.__metamodel = metamodel
        if self.__metamodel is not None:
            self.__metamodel._set_addon(self)
        self.__gui_injection = gui_injection
        self.__gui_injection._set_addon(self)
        self.__patch_plugin = patch_plugin
        if self.__patch_plugin is not None:
            self.__patch_plugin._set_addon(self)
        self.__plugin = plugin
        if self.__plugin is not None:
            self.__plugin._set_addon(self)
        if self.__patch_plugin is None and self.__plugin is None:
            self.__state = AddOnState.none
        else:
            self.__state = AddOnState.stopped
        
        self.__system_addon = system_addon
    
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
    def requirements(self):
        yield from self.__requirements
    
    @property
    def provisions(self):
        yield from self.__provisions
    
    @property
    def config_structure(self):
        return self.__config_structure
    
    @property
    def config(self):
        return self.__config
    
    @property
    def has_config(self):
        return self.__has_config
    
    @property
    def metamodel(self):
        return self.__metamodel
    
    @property
    def is_system_addon(self):
        return self.__system_addon
    
    @property
    def application(self):
        return self.__application
    
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
    def state(self):
        return self.__state
    
    @property
    def gui_injection(self):
        return self.__gui_injection
    
    def start(self):
        return AddOnStarter(self.__application.addons, self)

    def stop(self):
        return AddOnStopper(self.__application.addons, self)
    
    def _start(self):
        if self.__state == AddOnState.none:
            return
        if self.__state not in (AddOnState.stopped, AddOnState.error):
            raise Exception
        if self.__patch_plugin is not None:
            self.__patch_plugin.start()
        if self.__plugin is not None:
            self.__state = AddOnState.starting
            self.__application.event_dispatcher.dispatch(AddonStateChangedEvent(self, self.__state))
            self.__plugin.start()
        else:
            self.__state = AddOnState.started
            self.__application.event_dispatcher.dispatch(AddonStateChangedEvent(self, self.__state))
    
    def _plugin_started(self):
        self.__gui_injection.reset();
        self.__state = AddOnState.started
        self.__application.event_dispatcher.dispatch(AddonStateChangedEvent(self, self.__state))
    
    def _stop(self):
        if self.__state == AddOnState.none:
            return
        if self.__state != AddOnState.started:
            raise Exception
        if self.__patch_plugin is not None:
            self.__patch_plugin.stop()
        if self.__plugin is not None:
            self.__state = AddOnState.stopping
            self.__application.event_dispatcher.dispatch(AddonStateChangedEvent(self, self.__state))
            self.__plugin.stop()
        else:
            self.__state = AddOnState.stopped
            self.__application.event_dispatcher.dispatch(AddonStateChangedEvent(self, self.__state))
    
    def _plugin_stopped(self):
        if self.__patch_plugin is not None and self.__patch_plugin.running:
            self.__patch_plugin.stop()
        if self.__plugin is not None and self.__plugin.running:
            self.__plugin.stop()
        if self.__state == AddOnState.starting:
            self.__state = AddOnState.error
        else:
            self.__state = AddOnState.stopped
        self.__application.event_dispatcher.dispatch(AddonStateChangedEvent(self, self.__state))

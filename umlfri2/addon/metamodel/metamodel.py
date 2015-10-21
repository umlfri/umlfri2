class Metamodel:
    def __init__(self, config):
        self.__config_structure = config
        self.__config = config.build_default()
    
    @property
    def config(self):
        return self.__config
    
    @property
    def config_structure(self):
        return self.__config_structure

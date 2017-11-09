class OnlineAddOn:
    def __init__(self, application, identifier, versions):
        self.__application = application
        self.__identifier = identifier
        self.__versions = tuple(sorted(versions, key=lambda ver: ver.version, reverse=True))
        
        for version in self.__versions:
            version._set_addon(self)
    
    @property
    def identifier(self):
        return self.__identifier
    
    @property
    def name(self):
        return self.__versions[0].name
    
    @property
    def author(self):
        return self.__versions[0].author
    
    @property
    def homepage(self):
        return self.__versions[0].homepage
    
    @property
    def license(self):
        return self.__versions[0].license
    
    @property
    def icon(self):
        return self.__versions[0].icon
    
    @property
    def description(self):
        return self.__versions[0].description
    
    @property
    def requirements(self):
        yield from self.__versions[0].requirements
    
    @property
    def provisions(self):
        yield from self.__versions[0].provisions
    
    @property
    def versions(self):
        yield from self.__versions
    
    @property
    def latest_version(self):
        return self.__versions[0]
    
    @property
    def local_addon(self):
        return self.__application.addons.local.get_addon(self.__identifier)

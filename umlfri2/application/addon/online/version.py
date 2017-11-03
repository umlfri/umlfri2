class OnlineAddOnVersion:
    def __init__(self, name, version, author, homepage, license, icon, description,
                 requirements, provisions, changelog, locations):
        self.__name = name
        self.__version = version
        self.__author = author
        self.__homepage = homepage
        self.__license = license
        self.__icon = icon
        self.__description = description
        self.__requirements = tuple(requirements)
        self.__provisions = tuple(provisions)
        self.__changelog = changelog
        self.__locations = tuple(locations)
    
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
    def changelog(self):
        return self.__changelog
    
    @property
    def valid_location(self):
        for location in self.__locations:
            if location.is_valid:
                return location

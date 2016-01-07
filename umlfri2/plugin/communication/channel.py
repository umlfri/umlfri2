class Channel:
    def write(self, data):
        raise NotImplementedError
    
    def read(self):
        raise NotImplementedError
    
    @property
    def closed(self):
        raise NotImplementedError

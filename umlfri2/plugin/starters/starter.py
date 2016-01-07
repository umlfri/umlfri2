class AddonStarter:
    def start(self):
        # should return communication channel
        raise NotImplementedError
    
    def terminate(self):
        raise NotImplementedError
    
    def kill(self):
        raise NotImplementedError
    
    @property
    def is_alive(self):
        raise NotImplementedError

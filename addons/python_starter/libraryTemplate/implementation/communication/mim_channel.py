class MIMChannel:
    def __init__(self, channel):
        self.__channel = channel
    
    def write(self, data):
        print('S:', data)
        self.__channel.write(data)
    
    def read(self):
        ret = self.__channel.read()
        print('R:', ret)
        return ret
    
    def close(self):
        self.__channel.close()

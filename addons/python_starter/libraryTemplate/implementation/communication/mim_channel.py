from sys import stdout


class MIMChannel:
    def __init__(self, channel):
        self.__channel = channel
    
    def write(self, data):
        print('S:', data, file=stdout)
        stdout.flush()
        self.__channel.write(data)
    
    def read(self):
        ret = self.__channel.read()
        print('R:', ret, file=stdout)
        stdout.flush()
        return ret
    
    def close(self):
        self.__channel.close()
    
    @property
    def closed(self):
        return self.__channel.closed

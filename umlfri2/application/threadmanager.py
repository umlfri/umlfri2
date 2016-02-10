class ThreadManager:
    def start_thread(self, function):
        """
        Do not forget to keep returned reference. 
        """
        raise NotImplementedError
    
    def execute_in_main_thread(self, function):
        raise NotImplementedError


from .launcher import Launcher
from .util.daemon import Daemon

class Config:
    
    active_user_list = None
    
    def __init__(self):
        self.active_user_list = ['root', 'john-charles']

class RecronDaemon(Daemon):
    
    def __init__(self):
        Daemon.__init__(self, "/var/run/recron.pid")
        self.config = Config()
    
    def run(self):
        
        self.launcher = Launcher(self.config)
        self.launcher.start()
        
    def quit(self):
        self.launcher.stop()
    
    
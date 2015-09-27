__all__ = ['CONFIG']

import os
import pwd
import getpass
import configparser

class Config:
    
    LOG_DIR = "/var/log/recron"
    EVENTS_LOG = "events.log"
    CRONTAB = "crontab"
    CRONTAB_INI = "crontab.ini"
    
        
    def __init__(self):
        
        self.username = getpass.getuser()
        self.userinfo = pwd.getpwnam(self.username)
        self.user_dir = os.path.join(self.userinfo.pw_dir, ".recron")
        self.user_file = os.path.join(self.user_dir, "config.ini")
        self.user_crontab = os.path.join(self.user_dir, self.CRONTAB)
        self.files = ("/etc/recron/config.ini", self.user_file)
        
        self.parser = configparser.ConfigParser()
        self.parser.read(self.files)
        
        if not self.parser.has_section('user'):
            self.parser['user'] = {}
    
    def get_editor(self):
        return self.parser['user']['editor']
    
    def set_editor(self, editor):
        self.parser['user']['editor'] = editor
        
    def save(self):
        
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir, 0o700)
        
        with open(self.user_file, "w") as config_output:
            self.parser.write(config_output)
        

CONFIG = Config()
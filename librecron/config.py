__all__ = ['CONFIG']

import os
import configparser

class Config:
        
    def __init__(self):
        
        self.user_dir = os.path.expanduser("~/.recron")
        self.user_file = os.path.join(self.user_dir, "config.ini")
        self.user_crontab = os.path.join(self.user_dir, "crontab")
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
            os.makedirs(self.user_dir, 0x0700)
        
        with open(self.user_file, "w") as config_output:
            self.parser.write(config_output)
        

CONFIG = Config()
import configparser
import os
from pkgutil import read_code

class ConfigReader():    

    _instance = None  # Class-level variable to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, value=None):
        """Ensure initialization runs only once"""
        if not hasattr(self, 'initialized'):
            settings = self.read_config()
            self.modelused = settings['model_used']
            self.gtest_model = settings['gtest_model']
            self.vc_installdir = settings['vc_installdir']
            self.win10dev_installdir = settings['win10dev_installdir']
            self.initialized = True


    def get_model_used(self):
        return self.modelused

    def get_gtest_model(self):
        return self.gtest_model

    def get_vc_installdir(self):
        return self.vc_installdir

    def get_win10dev_installdir(self):
        return self.win10dev_installdir

    def read_config(self, file_path='CppMicroAgent.cfg'):
        config = configparser.ConfigParser()
        config.read(file_path)
    
        if 'OLLAMA_SETTINGS' not in config:
            raise ValueError("Missing [OLLAMA_SETTINGS] section in the config file")
    
        settings = {
            'model_used': config['OLLAMA_SETTINGS'].get('model_used', ''),
            'gtest_model': config['OLLAMA_SETTINGS'].get('gtest_model', ''),
            'vc_installdir': config['OLLAMA_SETTINGS'].get('vc_installdir', ''),
            'win10dev_installdir': config['OLLAMA_SETTINGS'].get('win10dev_installdir', '')
        }
    
        return settings




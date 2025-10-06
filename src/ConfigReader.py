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
            self.codegen_model = settings['codegen_model']
            self.gtest_model = settings['gtest_model']
            self.vc_installdir = settings['vc_installdir']
            self.win10dev_installdir = settings['win10dev_installdir']
            self.win10dev_libdir = settings['win10dev_libdir']
            self.opencpp_dir = settings['opencpp_dir']
            # Linux-specific settings
            self.gcc_compiler = settings.get('gcc_compiler', '/usr/bin/g++')
            self.gcov_tool = settings.get('gcov_tool', '/usr/bin/gcov')
            self.lcov_tool = settings.get('lcov_tool', '/usr/bin/lcov')
            # Project settings
            self.default_project_path = settings.get('default_project_path', 'TestProjects/SampleApplication/SampleApp')
            # Output settings
            self.clean_output_before_run = settings.get('clean_output_before_run', 'true').lower() == 'true'
            self.output_directory = settings.get('output_directory', 'output')
            self.coverage_target = float(settings.get('coverage_target', '80.0'))
            self.max_iterations = int(settings.get('max_iterations', '3'))
            self.initialized = True

    def getOpenCppDir(self):
        return self.opencpp_dir

    def get_model_used(self):
        return self.modelused

    def get_codegen_model(self):
        return self.codegen_model

    def get_gtest_model(self):
        return self.gtest_model

    def get_vc_installdir(self):
        return self.vc_installdir

    def get_win10dev_installdir(self):
        return self.win10dev_installdir

    def get_win10dev_libdir(self):
        return self.win10dev_libdir

    def get_gcc_compiler(self):
        return self.gcc_compiler

    def get_gcov_tool(self):
        return self.gcov_tool

    def get_lcov_tool(self):
        return self.lcov_tool

    def get_default_project_path(self):
        return self.default_project_path

    def get_clean_output_before_run(self):
        return self.clean_output_before_run

    def get_output_directory(self):
        return self.output_directory

    def get_coverage_target(self):
        return self.coverage_target

    def get_max_iterations(self):
        return self.max_iterations

    def read_config(self, file_path='CppMicroAgent.cfg'):
        config = configparser.ConfigParser()
        config.read(file_path)
    
        if 'OLLAMA_SETTINGS' not in config:
            raise ValueError("Missing [OLLAMA_SETTINGS] section in the config file")
    
        settings = {
            'model_used': config['OLLAMA_SETTINGS'].get('model_used', ''),
            'codegen_model': config['OLLAMA_SETTINGS'].get('codegen_model', ''),
            'gtest_model': config['OLLAMA_SETTINGS'].get('gtest_model', ''),
            'vc_installdir': config['OLLAMA_SETTINGS'].get('vc_installdir', ''),
            'win10dev_installdir': config['OLLAMA_SETTINGS'].get('win10dev_installdir', ''),
            'win10dev_libdir': config['OLLAMA_SETTINGS'].get('win10dev_libdir', ''),
            'opencpp_dir': config['OLLAMA_SETTINGS'].get('opencpp_dir', ''),
            'gcc_compiler': config['OLLAMA_SETTINGS'].get('gcc_compiler', '/usr/bin/g++'),
            'gcov_tool': config['OLLAMA_SETTINGS'].get('gcov_tool', '/usr/bin/gcov'),
            'lcov_tool': config['OLLAMA_SETTINGS'].get('lcov_tool', '/usr/bin/lcov')
        }
        
        # Add project settings if section exists
        if 'PROJECT_SETTINGS' in config:
            settings.update({
                'default_project_path': config['PROJECT_SETTINGS'].get('default_project_path', 'TestProjects/SampleApplication/SampleApp')
            })
        else:
            settings['default_project_path'] = 'TestProjects/SampleApplication/SampleApp'
        
        # Add output settings if section exists
        if 'OUTPUT_SETTINGS' in config:
            settings.update({
                'clean_output_before_run': config['OUTPUT_SETTINGS'].get('clean_output_before_run', 'true'),
                'output_directory': config['OUTPUT_SETTINGS'].get('output_directory', 'output'),
                'coverage_target': config['OUTPUT_SETTINGS'].get('coverage_target', '80.0'),
                'max_iterations': config['OUTPUT_SETTINGS'].get('max_iterations', '3')
            })
        else:
            settings.update({
                'clean_output_before_run': 'true',
                'output_directory': 'output',
                'coverage_target': '80.0',
                'max_iterations': '3'
            })
    
        return settings




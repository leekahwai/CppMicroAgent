#!/usr/bin/env python3
"""
Configuration reader utility for CppMicroAgent
Reads settings from CppMicroAgent.cfg
"""

import configparser
from pathlib import Path

def get_config_path():
    """Get the path to the configuration file"""
    # Assume config is in the root directory
    root_dir = Path(__file__).parent.parent
    return root_dir / "CppMicroAgent.cfg"

def read_config():
    """Read the configuration file and return a config object"""
    config_path = get_config_path()
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    return config

def get_project_path():
    """Get the project path from configuration"""
    config = read_config()
    
    if 'PROJECT_SETTINGS' not in config:
        raise ValueError("PROJECT_SETTINGS section not found in configuration")
    
    project_settings = config['PROJECT_SETTINGS']
    
    if 'project_path' not in project_settings:
        raise ValueError("project_path not found in PROJECT_SETTINGS")
    
    project_path = project_settings['project_path'].strip()
    
    # Convert to absolute path
    root_dir = Path(__file__).parent.parent
    absolute_path = root_dir / project_path
    
    return absolute_path

def get_ollama_model():
    """Get the Ollama model from configuration"""
    config = read_config()
    
    if 'OLLAMA_SETTINGS' in config:
        return config['OLLAMA_SETTINGS'].get('model_used', 'qwen2.5:0.5b')
    
    return 'qwen2.5:0.5b'

if __name__ == "__main__":
    # Test the configuration reader
    print(f"Configuration file: {get_config_path()}")
    print(f"Project path: {get_project_path()}")
    print(f"Ollama model: {get_ollama_model()}")

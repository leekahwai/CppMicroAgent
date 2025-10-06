"""
Query Class - Data Container for Project Information
==================================================

Simple data container class that holds project path and related information
for the C++ Micro Agent coverage improvement system.
"""

import os

class Query:
    """
    Data container class for project information and configuration.
    Used throughout the state machine system to pass project context.
    """
    
    def __init__(self, input_data):
        """
        Initialize Query with project path or data.
        
        Args:
            input_data (str): Project path or input data
        """
        self.input_data = input_data
        self.project_path = input_data if isinstance(input_data, str) else str(input_data)
        
    def get_input_data(self):
        """
        Get the input data/project path.
        
        Returns:
            str: The project path or input data
        """
        return self.input_data
    
    def get_project_path(self):
        """
        Get the project path.
        
        Returns:
            str: The project path
        """
        return self.project_path
    
    def set_input_data(self, data):
        """
        Set the input data/project path.
        
        Args:
            data (str): New project path or input data
        """
        self.input_data = data
        self.project_path = data if isinstance(data, str) else str(data)
    
    def exists(self):
        """
        Check if the project path exists.
        
        Returns:
            bool: True if path exists, False otherwise
        """
        return os.path.exists(self.project_path)
    
    def is_directory(self):
        """
        Check if the project path is a directory.
        
        Returns:
            bool: True if path is a directory, False otherwise
        """
        return os.path.isdir(self.project_path)
    
    def get_absolute_path(self):
        """
        Get the absolute path of the project.
        
        Returns:
            str: Absolute path of the project
        """
        return os.path.abspath(self.project_path)
    
    def __str__(self):
        """String representation of the Query object."""
        return f"Query(path='{self.project_path}')"
    
    def __repr__(self):
        """String representation for debugging."""
        return self.__str__()
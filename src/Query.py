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
        self.source_files = []
        self.include_folders = []
        self.current_output_folder = None
        self.current_include = None
        self.current_source = None
        self.current_function = None
        self.current_header_content = None
        self.current_implementation_content = None
        self.current_source_content = None
        self.coverage_data = None
        self.coverage_iteration_results = []
        self.generated_code = None
        self.generated_ut_file = None
        
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
    
    def set_source_files(self, source_files):
        """
        Set the source files for the project.
        
        Args:
            source_files (list): List of source file paths
        """
        self.source_files = source_files
    
    def get_source_files(self):
        """
        Get the source files for the project.
        
        Returns:
            list: List of source file paths
        """
        return self.source_files
    
    def set_include_folders(self, include_folders):
        """
        Set the include folders for the project.
        
        Args:
            include_folders (list): List of include folder paths
        """
        self.include_folders = include_folders
    
    def get_include_folders(self):
        """
        Get the include folders for the project.
        
        Returns:
            list: List of include folder paths
        """
        return self.include_folders
    
    def set_current_output_folder(self, output_folder):
        """
        Set the current output folder.
        
        Args:
            output_folder (str): Path to the output folder
        """
        self.current_output_folder = output_folder
    
    def get_current_output_folder(self):
        """
        Get the current output folder.
        
        Returns:
            str: Path to the current output folder
        """
        return self.current_output_folder
    
    def set_current_include(self, include):
        """
        Set the current include file.
        
        Args:
            include (str): Path to the current include file
        """
        self.current_include = include
    
    def get_current_include(self):
        """
        Get the current include file.
        
        Returns:
            str: Path to the current include file
        """
        return self.current_include
    
    def set_current_source(self, source):
        """
        Set the current source file.
        
        Args:
            source (str): Path to the current source file
        """
        self.current_source = source
    
    def get_current_source(self):
        """
        Get the current source file.
        
        Returns:
            str: Path to the current source file
        """
        return self.current_source
    
    def set_current_function(self, function):
        """
        Set the current function name.
        
        Args:
            function (str): Name of the current function
        """
        self.current_function = function
    
    def get_current_function(self):
        """
        Get the current function name.
        
        Returns:
            str: Name of the current function
        """
        return self.current_function
    
    def set_current_header_content(self, content):
        """
        Set the current header content.
        
        Args:
            content (str): Header file content
        """
        self.current_header_content = content
    
    def get_current_header_content(self):
        """
        Get the current header content.
        
        Returns:
            str: Header file content
        """
        return self.current_header_content
    
    def set_current_implementation_content(self, content):
        """
        Set the current implementation content.
        
        Args:
            content (str): Implementation file content
        """
        self.current_implementation_content = content
    
    def get_current_implementation_content(self):
        """
        Get the current implementation content.
        
        Returns:
            str: Implementation file content
        """
        return self.current_implementation_content
    
    def set_current_source_content(self, content):
        """
        Set the current source content.
        
        Args:
            content (str): Source file content
        """
        self.current_source_content = content
    
    def get_current_source_content(self):
        """
        Get the current source content.
        
        Returns:
            str: Source file content
        """
        return self.current_source_content
    
    def set_coverage_data(self, data):
        """
        Set the coverage data.
        
        Args:
            data: Coverage data object
        """
        self.coverage_data = data
    
    def get_coverage_data(self):
        """
        Get the coverage data.
        
        Returns:
            Coverage data object
        """
        return self.coverage_data
    
    def set_coverage_iteration_results(self, results):
        """
        Set the coverage iteration results.
        
        Args:
            results (list): List of iteration results
        """
        self.coverage_iteration_results = results
    
    def get_coverage_iteration_results(self):
        """
        Get the coverage iteration results.
        
        Returns:
            list: List of iteration results
        """
        return self.coverage_iteration_results
    
    def set_generated_code(self, code):
        """
        Set the generated code.
        
        Args:
            code (str): Generated code content
        """
        self.generated_code = code
    
    def get_generated_code(self):
        """
        Get the generated code.
        
        Returns:
            str: Generated code content
        """
        return self.generated_code
    
    def set_generated_ut_file(self, filename):
        """
        Set the generated unit test file path.
        
        Args:
            filename (str): Path to generated unit test file
        """
        self.generated_ut_file = filename
    
    def get_generated_ut_file(self):
        """
        Get the generated unit test file path.
        
        Returns:
            str: Path to generated unit test file
        """
        return self.generated_ut_file
    
    def __str__(self):
        """String representation of the Query object."""
        return f"Query(path='{self.project_path}')"
    
    def __repr__(self):
        """String representation for debugging."""
        return self.__str__()
import array
from tkinter import SE
from xmlrpc.client import Boolean


class Query:
    _instance = None  # Class-level variable to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, input_data):
        self.input_data = input_data
        self.generated_code = ""
        self.generated_ut = ""
        self.generated_code_file = ""
        self.generated_ut_file = ""
        self.generated_ut_comments = ""
        self.gtestCompiledResult = ""
        self.gtestSecondAttempt = False
        self.generatedCodeSecondAttempt = False
        self.gtestErrors = ""
        self.codeErrors = ""
        #Subsequent are for coverage unit testing
        self.include_folders=[]
        self.source_files=[]
        self.current_source = ""
        self.current_include = ""
        self.current_source_content = ""
        self.current_header_content = ""
        self.current_implementation_content = ""
        self.current_output_folder = ""


    def get_current_output_folder(self):
        return self.current_output_folder

    def set_current_output_folder(self, data:str) :
        self.current_output_folder = data

    def get_current_source_content(self) :
        return self.current_source_content 

    def set_current_source_content(self, data:str) :
        self.current_source_content = data

    def get_current_header_content(self) :
        return self.current_header_content

    def set_current_header_content(self, data:str) :
        self.current_header_content = data

    def get_current_implementation_content(self) :
        return self.current_implementation_content

    def set_current_implementation_content(self, data:str):
        self.current_implementation_content = data

    def get_current_source(self):
        return self.current_source

    def set_current_source(self, data:str):
        self.current_source = data

    def get_current_include(self):
        return self.current_include

    def set_current_include(self, data:str):
        self.current_include = data

    def get_input_data(self):
        return self.input_data

    def set_include_folders(self, data: list):
        self.include_folders = data

    def get_include_folders(self):
        return self.include_folders

    def set_source_files(self, data:list) :
        self.source_files = data

    def get_source_files(self):
        return self.source_files

    def set_generated_ut_comments(self, data: str):
        self.generated_ut_comments = data

    def get_generated_ut_comments(self):    
        return self.generated_ut_comments

    def set_generated_code(self, data: str):
        self.generated_code = data

    def get_generated_code(self):
        return self.generated_code

    def set_generated_ut (self, data:str):
        self.generated_ut = data

    def get_generated_ut(self):
        return self.generated_ut

    def set_generated_code_file(self, data: str):
        self.generated_code_file = data

    def get_generated_code_file(self):
        return self.generated_code_file

    def set_generated_ut_file(self, data: str):
        self.generated_ut_file = data

    def get_generated_ut_file(self):    
        return self.generated_ut_file

    def set_gtestCompiledResult(self, data: str):
        self.gtestCompiledResult = data

    def get_gtestCompiledResult(self):
        return self.gtestCompiledResult

    def set_gtestSecondAttempt(self, data: Boolean) :
        self.gtestSecondAttempt = data

    def get_gtestSecondAttempt(self) :
        return self.gtestSecondAttempt

    def set_generatedCodeSecondAttempt(self, data: Boolean):
        self.generatedCodeSecondAttempt = data

    def get_generatedCodeSecondAttempt(self) :
        return self.generatedCodeSecondAttempt

    def set_gtestErrors (self, data:str):
        self.gtestErrors = data

    def get_gtestErrors (self):
        return self.gtestErrors

    def set_codeErrors (self, data:str):
        self.codeErrors = data

    def get_codeErrors (self):
        return self.codeErrors






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
        self.gtestCompiledResult = ""
        self.gtestSecondAttempt = False
        self.generatedCodeSecondAttempt = False

    def get_input_data(self):
        return self.input_data

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





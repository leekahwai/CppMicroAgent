from tkinter import SE


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


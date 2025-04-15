

import code
from http import client
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
import json
import time
from flow_manager import flow

class StateFilterGTestCode():
    def __init__(self):
        print("Initializing [StateFilterGTestCode]")

    def run(self, input_data):
        flow.transition("StateFilterGTestCode")
        print ("[StateFilterGTestCode] Filtering Google Test codes... Please Wait....")
        configReader = ConfigReader()
        
        response_text = input_data.get_generated_ut_comments()


        # Use GEMMA Model
        print ("\n\nFiltering response from GTEST Model")
        query = "Filter for the google test codes and main test from here. Insert main if it's not inside. Do not add explanation. Code: " + response_text
        client2 = OllamaClient()
        response_str = client2.query(configReader.get_model_used(), query)
        
        
        # Split multiple JSON objects and process them separately
        responses = response_str.strip().split("\n")



        response_text = ""
        for resp in responses:
            response_json = json.loads(resp)
            if not response_json["done"]:  # Only process responses where "done" is false
                print(response_json["response"], end="")  # Print without newline
                # Extract response
                response_text += (response_json["response"])
                
        codeWriter = CodeWriter(input_data, response_text, "output", "Test", True)
        filename = codeWriter.process_code()
        input_data.set_generated_ut_file(filename)
        if (response_text != ""):
            input_data.set_generated_ut(response_text)
            return True, input_data
        else:   
            print ("[StateGenerateGTestCodeFromInput] No googletest code generated. Terminating.")
            return False, input_data
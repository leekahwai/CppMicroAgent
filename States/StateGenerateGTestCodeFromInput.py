

import code
from http import client
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
import json
import time

class StateGenerateGTestCodeFromInput():
    def __init__(self):
        print("Initializing [StateGenerateGTestCodeFromInput]")

    def run(self, input_data):
        print ("[StateGenerateGTestCodeFromInput] Generating Google Test codes... Please Wait....")
        client = OllamaClient()
        configReader = ConfigReader()
        modelused = configReader.get_model_used()

        if len(input_data.get_generated_code()) < 2:
            raise ValueError("Code is too short to process.")

        # Remove first and last line
        processed_lines = input_data.get_generated_code()[1:-1]
        input_data.set_generated_code("".join(processed_lines))

        if input_data.get_gtestSecondAttempt() == True:
            query = "The following Gtest is wrong. Rewrite. \n Current GTest Code: \n" + input_data.get_generated_ut() + "\n Error is: \n" + input_data.get_gtestErrors() + "\n Original Code is: \n" + input_data.get_generated_code()+ "\n Use the following #include " + input_data.get_generated_code_file() ;
        else:
            query = "Generate the corresponding C++ googletest unit test with appropriate assertions for the following code in a single cpp file. Add doxygen comments.  Code: \n\n" + input_data.get_generated_code() + "\n //  " + input_data.get_generated_code_file();
        # Using GTest Model
        # print(query)
        time.sleep(1)
        gtest_model = configReader.get_gtest_model()
        if input_data.get_gtestSecondAttempt() == True:
            gtest_model = configReader.get_model_used()
        response_str = client.query(gtest_model, query)
        
        response_text = ""
        responses = response_str.strip().split("\n")

        for resp in responses:
            response_json = json.loads(resp)
            if not response_json["done"]:  # Only process responses where "done" is false
                print(response_json["response"], end="")  # Print without newline
                # Extract response
                response_text += (response_json["response"])


        time.sleep(2) # Sleep few seconds before switching model
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
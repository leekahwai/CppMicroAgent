

import code
from http import client
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
import json
import time
from flow_manager import flow

class StateGenerateGTestCodeFromInput():
    def __init__(self):
        print("Initializing [StateGenerateGTestCodeFromInput]")

    def run(self, input_data):
        flow.transition("StateGenerateGTestCodeFromInput")
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
            query = "The following Gtest is wrong. Ensure 1 test and 1 main is included. Rewrite. \n Current GTest Code: \n" + input_data.get_generated_ut() + "\n Error is: \n" + input_data.get_gtestErrors() + "\n Original Code is: \n" + input_data.get_generated_code()+ "\n Use the following #include " + input_data.get_generated_code_file() ;
        else:
            query = "Generate the corresponding C++ googletest unit test with appropriate assertions for the following code in a single cpp file. Ensure at least one test and main is included. Add doxygen comments.  Code: \n\n" + input_data.get_generated_code() + "\n //  " + input_data.get_generated_code_file();
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
                input_data.set_generated_ut_comments(response_text)

        
        return True, input_data
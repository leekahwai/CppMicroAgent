

import code
from http import client
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
import json
import time

from States.Query import Query

class StateVerifyFailedCompiledGTest():
    def __init__(self):
        print("Initializing [StateVerifyFailedCompiledGTest]")

    def run(self, input_data):
        print ("[StateVerifyFailedCompiledGTest] Verifying GTest Compilation Error Reason... Please Wait....")
        client = OllamaClient()
        configReader = ConfigReader()
        modelused = configReader.get_model_used()

        # Check Compiled GTest Results
        processed_lines = input_data.get_gtestCompiledResult()
        query = "Does the following files contain error(s) pertaining to Test.cpp only? Answer with a simple Yes or No: \n\n" + processed_lines + " GTest Test.cpp: \n" + input_data.get_generated_ut() + " Original Generated Code: " + input_data.get_generated_code();
        # Using GTest Model
        print(query)
        time.sleep(1)
        response_str = client.query(configReader.get_gtest_model(), query)
        
        response_text = ""
        responses = response_str.strip().split("\n")

        for resp in responses:
            response_json = json.loads(resp)
            if not response_json["done"]:  # Only process responses where "done" is false
                print(response_json["response"], end="")  # Print without newline
                # Extract response
                response_text += (response_json["response"])

        if (response_text == "Yes") or (response_text == "Yes."):
            print ("[StateVerifyFailedCompiledGTest] Error comes from GTest only. Modify input data")
            input_data.set_gtestSecondAttempt(True)
            input_data.set_gtestErrors(processed_lines)

            #TODO   To go back to StateGenerateGTestCodeFromInput.py and restart the attempt 
            #       Also use a different query based on gtestSecondAttempt


            return True, input_data
        else:   
            print ("[StateGenerateGTestCodeFromInput] Error comes from the code generation. Return with now information of the generated code.")
            return False, input_data
        

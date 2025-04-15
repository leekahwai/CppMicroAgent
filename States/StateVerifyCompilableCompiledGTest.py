

import code
from http import client
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
import json
import time
import os
import subprocess
from flow_manager import flow

from States.Query import Query

class StateVerifyCompilableCompiledGTest():
    def __init__(self):
        self.configReader = ConfigReader()
        print("Initializing [StateVerifyCompilableCompiledGTest]")

    def run(self, input_data):
        flow.transition("StateVerifyCompilableCompiledGTest")
        print ("[StateVerifyCompilableCompiledGTest] Verifying GTest Results... Please Wait....")
        client = OllamaClient()
        configReader = ConfigReader()
        modelused = configReader.get_model_used()

        current_path = os.path.abspath(os.getcwd())
        # Construct paths using os.path.join for clarity
        test_exe = os.path.join(current_path, "output", "Test.exe")
        output_txt = os.path.join(current_path, "output", "GTestRun.txt")

        # Build a single command string
        gpp_command = f'"{test_exe}" > "{output_txt}"'

        result = subprocess.run(
            gpp_command,
            shell=True,
            cwd=os.path.join(current_path, "output")
        )

        # Read in the GTestRun.txt
        pathToGTestResults = current_path + "\\output"+ "\\GTestRun.txt"
        with open(pathToGTestResults, 'r') as file:
            contents = file.read()
            # To store contents of gtest compilation into input_data
            input_data.set_gtestCompiledResult(contents)

        # Check Compiled GTest Results
        processed_lines = contents
        query = "Does the following GTest passed? Answer with a simple Yes or No: \n\n" + processed_lines + " GTest Test.cpp: \n" + input_data.get_generated_ut() + " Original Generated Code: " + input_data.get_generated_code();
        # Using GTest Model
        print(query)
        time.sleep(1)
        response_str = client.query(configReader.get_model_used(), query)
        
        response_text = ""
        responses = response_str.strip().split("\n")

        for resp in responses:
            response_json = json.loads(resp)
            if not response_json["done"]:  # Only process responses where "done" is false
                print(response_json["response"], end="")  # Print without newline
                # Extract response
                response_text += (response_json["response"])

        response_text = response_text[:3]
        if (response_text == "Yes"):
            print ("[StateVerifyCompilableCompiledGTest] All Test Passed Generated from GTest")
            return True, input_data
        else:   
            print ("[StateGenerateGTestCodeFromInput] Error comes from the code generation. Return with now information of the generated code.")
            input_data.set_gtestSecondAttempt(True)
            input_data.set_gtestErrors(processed_lines)

            
            return False, input_data
        


import code
from http import client
from re import I
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
from HeaderFileCleaner import HeaderFileCleaner
import json
from States.Query import Query
from flow_manager import flow

class StateGenerateCodeFromInput():
    def __init__(self):
        print("Initializing [StateA]")

    def run(self, input_data):
        flow.transition("StateGenerateCodeFromInput")
        print ("\n[StateGenerateCodeFromInput] Removing previous generated codes... ")
        

        folders_to_clean = [
            "output",
            "output/test",
            "CoverageReport*"
        ]

        cleaner = HeaderFileCleaner(folders_to_clean)
        cleaner.remove_header_files()


        print ("[StateGenerateCodeFromInput] Generating codes... Please Wait....")
        if input_data.get_generatedCodeSecondAttempt() == True:
            query = "Generate the following c++ coding request in a class header file without explanation. Use template if required.  Ensure this is compilable. Use pragma once as header guard. Add doxygen comments.  Coding Request: " + input_data.get_input_data();
        else:
            query = "Proceed to generate the following c++ coding request in a class header file without explanation. Use template if required. Ensure all operations are implemented. Use pragma once as header guard. Add doxygen comments.  Coding Request: " + input_data.get_input_data();
        client = OllamaClient()
        configReader = ConfigReader()
        modelused = configReader.get_codegen_model()
        response_str = client.query(configReader.get_codegen_model(), query)
        # Split multiple JSON objects and process them separately
        responses = response_str.strip().split("\n")

        response_text = ""
        for resp in responses:
            response_json = json.loads(resp)
            if not response_json["done"]:  # Only process responses where "done" is false
                print(response_json["response"], end="")  # Print without newline
                # Extract response
                response_text += (response_json["response"])
                
        codeWriter = CodeWriter(input_data, response_text, "output")
        filename = codeWriter.process_code()
        input_data.set_generated_code_file(filename)
        if (response_text != ""):
            input_data.set_generated_code(response_text) 
            return True, input_data
        else:   
            print ("[StateGenerateCodeFromInput] No code generated. Terminating.")
            return False, input_data
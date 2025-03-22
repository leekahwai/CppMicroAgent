
import code
from http import client
from re import I
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
from HeaderFileCleaner import HeaderFileCleaner
import json
from States.Query import Query

class StateGenerateCodeFromInput():
    def __init__(self):
        print("Initializing [StateA]")

    def run(self, input_data):

        print ("\n[StateGenerateCodeFromInput] Removing previous generated codes... ")
        

        folders_to_clean = [
            "output",
            "output/test",
        ]

        cleaner = HeaderFileCleaner(folders_to_clean)
        cleaner.remove_header_files()


        print ("[StateGenerateCodeFromInput] Generating codes... Please Wait....")
        query = "Proceed to generate the following c++ coding request in a class header file without explanation. Add doxygen comments.  Coding Request: " + input_data.get_input_data();
        client = OllamaClient()
        configReader = ConfigReader()
        modelused = configReader.get_model_used()
        response_str = client.query(configReader.get_model_used(), query)
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
        codeWriter.process_code()
        if (response_text != ""):
            input_data.set_generated_code(response_text) 
            return True, input_data
        else:   
            print ("[StateGenerateCodeFromInput] No code generated. Terminating.")
            return False, input_data
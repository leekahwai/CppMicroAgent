from http import client
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
import json

class StateVerifyGenerateCodeQuery():
    def __init__(self):
        print("Initializing [StateVerifyGenerateCodeQuery]")

    def run(self, input_data):
        print ("[StateVerifyGenerateCodeQuery] Processing input... Verify whether request is a C++ code generation")
        query = "Can you verify whether the following text is asking you very specifically to generate a C++ code? Only reply with a Yes or No. Following Text: " + input_data.get_input_data();
        client = OllamaClient()
        configReader = ConfigReader()
        modelused = configReader.get_model_used()
        response_str = client.query(configReader.get_model_used(), query)
        # Split multiple JSON objects and process them separately
        responses = response_str.strip().split("\n")

        response_text = "No"
        for resp in responses:
            response_json = json.loads(resp)
            if not response_json["done"]:  # Only process responses where "done" is false
                print(response_json["response"], end="")  # Print without newline
                # Extract response
                response_text = response_json["response"]
                break


        if (response_text == "Yes"):
            return True, input_data
        else:
            print ("[StateVerifyGenerateCodeQuery] Request is not asking to generate C++ code. Terminating.")
            return False, input_data
        


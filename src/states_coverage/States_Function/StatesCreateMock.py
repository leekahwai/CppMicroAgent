
from ...flow_manager import flow
from ...Query import Query
from ...OllamaClient import OllamaClient
from ...ConfigReader import ConfigReader
from ...CodeWriter import CodeWriter
import os
import re
import json

class StatesCreateMock():
    def __init__(self):
        self.client = OllamaClient()
        self.configReader = ConfigReader()
        print("Initializing [States_Function::StateCreateMock]")

    def run(self, input_data):
        flow.transition("States_Function::StateCreateMock")
        print("[StateCreateMock] Reached StateCreateMock state.")

        header_file = input_data.get_current_include() 
        source_file = input_data.get_current_source() 
        h_filename = os.path.basename(header_file)   # → "SampleApp.h"

        # compile once
        include_re = re.compile(r'^\s*#include\s*"([^"]+)"')

        # scan both header and source
        includes = []
        for path in (header_file, source_file):
            with open(path, 'r') as f:
                for line in f:
                    m = include_re.match(line)
                    if m:
                        includes.append(m.group(1))

        # drop the header itself if present
        includes = [inc for inc in includes if inc != h_filename]

        # only iterate if we found any includes
        if includes:
            for inc in includes:
                # → replace this with whatever you need to do per include
                print(f"Found include: {inc}")
                
                modelused = self.configReader.get_codegen_model()
                query = "Generate the following mock header file, without explanation and using pragma once using the following filename: " + \
                    inc + ".\n Use structures and not classes, and only create namespaces when neccessary. Create a mock so that the following source file can compile, \n\n" + input_data.get_current_source_content().replace('\ufeff', '') +\
                    "\n\n and header file using it: \n\n" + input_data.get_current_header_content().replace('\ufeff', '')
                response_str = self.client.query(self.configReader.get_codegen_model(), query)
                # Split multiple JSON objects and process them separately
                responses = response_str.strip().split("\n")

                response_text = ""
                for resp in responses:
                    response_json = json.loads(resp)
                    if not response_json["done"]:  # Only process responses where "done" is false
                        print(response_json["response"], end="")  # Print without newline
                        # Extract response
                        response_text += (response_json["response"])
                
                codeWriter = CodeWriter(input_data, response_text, input_data.get_current_output_folder())
                name_without_ext, _ = os.path.splitext(inc)
                codeWriter.set_class_name(name_without_ext)
                filename = codeWriter.process_code(True, )
                return True, input_data
        else:
            print("No user headers found to process.")

        return False, None # Stop state machine

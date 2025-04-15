

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

class StateRunOpenCppCoverage():
    def __init__(self):
        self.configReader = ConfigReader()
        print("Initializing [StateRunOpenCppCoverage]")

    def run(self, input_data):
        flow.transition("StateRunOpenCppCoverage")
        print ("[StateRunOpenCppCoverage] Generating OpenCppCoverage... Please Wait....")
        client = OllamaClient()
        configReader = ConfigReader()
        opencppdir = configReader.getOpenCppDir()

        current_path = os.path.abspath(os.getcwd())
        # Construct paths using os.path.join for clarity
        test_exe = os.path.join(current_path, "output", "Test.exe")
        opencpp_exe = os.path.join(opencppdir, "OpenCppCoverage.exe")
        output_header = os.path.join(current_path, "output", "GTestRun.txt")

        # Build a single command string
        gpp_command = f'"{opencpp_exe}" '
        gpp_command += test_exe + " "
        gpp_command += "--modules="
        gpp_command += test_exe + " "
        gpp_command += "--sources="
        gpp_command += "SimpleDivision.h" #input_data.get_generated_code_file()

        print (gpp_command)

        result = subprocess.run(
            gpp_command,
            shell=True,
            cwd=os.path.join(current_path, "output")
        )

        return True, input_data
        

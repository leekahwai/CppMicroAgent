import code
from http import client
from OllamaClient import OllamaClient
from ConfigReader import ConfigReader
from CodeWriter import CodeWriter
import json
import time
import os
import subprocess

class StateAttempCompile():
    def __init__(self):
        print("Initializing [StateAttempCompile]")

    def run(self, input_data):
        print ("[StateAttempCompile] Attempting compilation....")
        configReader = ConfigReader()

        # 1. Get the absolute current path
        current_path = os.path.abspath(os.getcwd())
        print("Current Path:", current_path)

        # 2. Move up two folders above the current path
        two_levels_up = os.path.abspath(os.path.join(current_path, "..", ".."))
        print("Two Levels Up:", two_levels_up)

        # 3. Construct the path to MinGW\bin (i.e., <TwoLevelsUp>\MinGW\bin)
        mingw_bin_path = os.path.join(current_path, "MinGW", "bin")
        print("MinGW Bin Path:", mingw_bin_path)

        # 4. Build the g++ command
        # Here, <CurrentPath> is replaced with the absolute current path from step 1.
        gpp_command = [
            os.path.join(mingw_bin_path, "g++"),  # path to the g++ executable in MinGW\bin
            "-v",
            "-std=c++14",
            "-I", os.path.join(current_path, "output"),
            "-L", os.path.join(current_path, "output", "gtest"),
            "-lgtest",
            "-lgtest_main",
            os.path.join(current_path, "output", "Test.cpp"),
            "-o", os.path.join(current_path, "output", "Test.exe"),
            ">"+ os.path.join(current_path, "output", "verbose.txt")+ " 2>&1"
        ]

        # Display the command for debugging purposes
        print("Running command:", " ".join(gpp_command))

        try:
            result = subprocess.run(gpp_command, capture_output=True, text=True, cwd=mingw_bin_path)
            if result.returncode != 0:
                print("Compilation failed with return code:", result.returncode)
                print("Standard Output:\n", result.stdout)
                print("Standard Error:\n", result.stderr)
            else:
                print("Compilation succeeded.")
                print("Standard Output:\n", result.stdout)
                print("Standard Error:\n", result.stderr)
        except Exception as e:
            print("An error occurred while executing the command:", e)

            # Wait for the process to finish and print its return code
            subprocess.wait()
        print(f"\nProcess finished with return code: {result.returncode}")

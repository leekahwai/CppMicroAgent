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

class StateAttempCompile():
    def __init__(self):
        self.configReader = ConfigReader()
        print("Initializing [StateAttempCompile]")

    def check_vc_installation(self):
        print ("Verifying installation of Visual Studio...")
        vc_install_dir = self.configReader.get_vc_installdir()
        if os.path.exists(vc_install_dir):
            print("[StateInit] Visual Studio installation found.")
            return True
        else:
            print("[StateInit] Visual Studio installation missing!")
            return False

    def run(self, input_data):
        print ("[StateAttempCompile] Attempting compilation....")
        flow.transition("StateAttempCompile")

        # 1. Get the absolute current path
        current_path = os.path.abspath(os.getcwd())
        print("Current Path:", current_path)

        # 2. Move up two folders above the current path
        two_levels_up = os.path.abspath(os.path.join(current_path, "..", ".."))
        print("Two Levels Up:", two_levels_up)

        # 3. Construct the path to MinGW\bin (i.e., <TwoLevelsUp>\MinGW\bin)
        mingw_bin_path = os.path.join(current_path, "MinGW", "bin")
        print("MinGW Bin Path:", mingw_bin_path)

        vc_bin_path = os.path.join(self.configReader.get_vc_installdir(), "Hostx64", "x64", "bin")
        vc_inc_path = os.path.join(self.configReader.get_vc_installdir(), "include")
        win10_inc_path = os.path.join(self.configReader.get_win10dev_installdir(), "")

        # 4. Build the g++ command
        # Here, <CurrentPath> is replaced with the absolute current path from step 1.
        
        #gpp_command = "g++" + " -v" + " -std=c++14" + " -I ", os.path.join(current_path, "output")+ " -L " + os.path.join(current_path, "output", "gtest") + " -lgtest" + " -lgtest_main " + os.path.join(current_path, "output", "Test.cpp") +  " -o " + os.path.join(current_path, "output", "Test.exe")+ " >"+ os.path.join(current_path, "output", "verbose.txt")+ " 2>&1";
        path = ""
        compiler = ""
        gpp_command = []
        if self.check_vc_installation():
            path = self.configReader.get_vc_installdir()
            compiler = "cl.exe"
            '''
            gpp_command = [
                f'"{os.path.join(self.configReader.get_vc_installdir(), "bin", "Hostx64", "x64", "cl.exe"))}"', 
                "/std:c++14",
                "/MTd",
                "/D_DEBUG",
                "/EHsc", 
                f'/I"{os.path.join(current_path, "output")}"',
                f'/I"{os.path.join(self.configReader.get_vc_installdir(), "include")}"', 
                f'/I"{os.path.join(self.configReader.get_win10dev_installdir(), "ucrt")}"',
                f'{os.path.join(current_path, "output", "Test.cpp")}',
                f'{os.path.join(current_path, "output", "gtest", "gtest.lib")}',
                f'{os.path.join(current_path, "output", "gtest", "gtest_main.lib")}',
                f'"{os.path.join(self.configReader.get_vc_installdir(), "lib", "x64", "libcmtd.lib"}"',
                f'"{os.path.join(self.configReader.get_vc_installdir(), "lib", "x64", "libcpmtd.lib")}"',
                f'"{os.path.join(self.configReader.get_vc_installdir(), "lib", "x64", "oldnames.lib")}"',
                f'"{os.path.join(self.configReader.get_vc_installdir(), "lib", "x64", "libvcruntimed.lib")}"',
                f'"{os.path.join(self.configReader.get_win10dev_libdir(), "um", "x64", "kernel32.lib")}"',
                f'"{os.path.join(self.configReader.get_win10dev_libdir(), "um", "x64", "uuid.lib")}"',
                f'"{os.path.join(self.configReader.get_win10dev_libdir(), "ucrt", "x64", "libucrtd.lib")}"',
                f'"{os.path.join(self.configReader.get_win10dev_libdir(), "um", "x64", "kernel32.lib")}"',
                "/Fe",
                f'"{os.path.join(current_path, "output", "Test.exe"}"'
            ]
            '''
            gpp_command = f'"{self.configReader.get_vc_installdir()+"/bin/Hostx64/x64/cl.exe"}"'
            gpp_command += " /std:c++14 /MTd /D_DEBUG /EHsc /Zi"
            gpp_command += f' /fd"{current_path + "/output/Test.pdb"}"'
            gpp_command += f' /I"{current_path + "/output"}"'
            gpp_command += f' /I"{self.configReader.get_vc_installdir()+ "/include"}"'
            gpp_command += f' /I"{self.configReader.get_win10dev_installdir()+ "/ucrt"}"'
            gpp_command += f' "{current_path+ "/output"+ "/Test.cpp"}"'
            gpp_command += f' "{current_path+ "/output"+ "/gtest"+ "/gtest.lib"}"'
            gpp_command += f' "{current_path+ "/output"+ "/gtest"+ "/gtest_main.lib"}"'
            gpp_command += f' "{self.configReader.get_vc_installdir()+ "/lib"+ "/x64"+ "/libcmtd.lib"}"'
            gpp_command += f' "{self.configReader.get_vc_installdir()+ "/lib"+ "/x64"+ "/libcpmtd.lib"}"'
            gpp_command += f' "{self.configReader.get_vc_installdir()+ "/lib"+ "/x64"+ "/oldnames.lib"}"'
            gpp_command += f' "{self.configReader.get_vc_installdir()+ "/lib"+ "/x64"+ "/libvcruntimed.lib"}"'
            gpp_command += f' "{self.configReader.get_win10dev_libdir()+ "/um"+ "/x64"+ "/kernel32.lib"}"'
            gpp_command += f' "{self.configReader.get_win10dev_libdir()+ "/um"+ "/x64"+ "/uuid.lib"}"'
            gpp_command += f' "{self.configReader.get_win10dev_libdir()+ "/ucrt"+ "/x64"+ "/libucrtd.lib"}"'
            gpp_command += f' "{self.configReader.get_win10dev_libdir()+ "/um"+ "/x64"+ "/kernel32.lib"}"'
            gpp_command += " /Fe"
            gpp_command += f'"{current_path+ "/output"+ "/Test.exe"}"'
            gpp_command += " >"
            gpp_command += f'"{current_path+ "/output"+ "/compiledGTestResult.txt"}"'

        else:
            path = mingw_bin_path
            compiler = "g++.exe"

            gpp_command = [
                compiler,  # path to the g++ executable in MinGW\bin
                "-v",
                "-std=c++14",
                "-I", os.path.join(current_path, "output"),
                "-L", os.path.join(current_path, "output", "gtest"),
                "-lgtest",
                "-lgtest_main",
                os.path.join(current_path, "output", "Test.cpp"),
                "-o", os.path.join(current_path, "output", "Test.exe"),
                ">", os.path.join(current_path, "output", "compiledGTestResult.txt")
            ]
        
        # Display the command for debugging purposes
        print("Running command:", "".join(gpp_command))

        try:
            verbose_path = os.path.join(current_path, "output", "verbose.txt")

            if self.check_vc_installation():
                with open(verbose_path, "w") as verbose_file:
                    result = subprocess.run(
                        gpp_command,
                        shell=True,
                        cwd=os.path.join(self.configReader.get_vc_installdir(),""),
                        stdout=verbose_file,
                        stderr=subprocess.STDOUT  # combines stderr into stdout
                    )
            else:
                with open(verbose_path, "w") as verbose_file:
                    result = subprocess.run(
                        gpp_command,
                        cwd=mingw_bin_path,
                        stdout=verbose_file,
                        stderr=subprocess.STDOUT  # combines stderr into stdout
                    )

            #result = subprocess.run(gpp_command, capture_output=True, text=True, cwd=mingw_bin_path)
            if result.returncode != 0:
                print("GTest Compilation failed:", result.returncode)
                # Read GTest compilation
                # Open file
                pathToGTestResults = current_path + "\\output"+ "\\compiledGTestResult.txt"
                with open(pathToGTestResults, 'r') as file:
                    contents = file.read()
                    # To store contents of gtest compilation into input_data
                    input_data.set_gtestCompiledResult(contents)

                return False, input_data
            else:
                print("Compilation succeeded.")
                print("Standard Output:\n", result.stdout)
                print("Standard Error:\n", result.stderr)
                return True, input_data
        except Exception as e:
            print("An error occurred while executing the command:", e)

            # Wait for the process to finish and print its return code
            subprocess.wait()
            return False, input_data
        print(f"\nProcess finished with return code: {result.returncode}")

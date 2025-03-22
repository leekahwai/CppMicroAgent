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
            gpp_command = [
                "cl.exe",
                "/std:c++14",
                f'/I"{os.path.join(current_path, "output")}"',
                f'/I"{os.path.join(self.configReader.get_vc_installdir(), "Hostx64", "x64", "bin")}"',
                f'/I"{os.path.join(self.configReader.get_win10dev_installdir(), "")}"',
                f'{os.path.join(current_path, "output", "Test.cpp")}',
                f'{os.path.join(current_path, "output", "gtest", "gtest.lib")}',
                f'{os.path.join(current_path, "output", "gtest", "gtest_main.lib")}',
                f'/Fe"{os.path.join(current_path, "output", "Test.exe")}"'
            ]

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
                "-o", os.path.join(current_path, "output", "Test.exe")
            ]

            '''
            Following command needs to be incoporated for it to work. Update accordingly
            "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.43.34808\bin\Hostx64\x64\cl.exe" /std:c++14 /MTd /D_DEBUG /EHsc^
             /I"D:\TFS\Dev\CppMicroAgent\prj\CppMicroAgent\output" ^
             /I"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.43.34808\include" ^
             /I"C:\Program Files (x86)\Windows Kits\10\Include\10.0.22000.0\ucrt" ^
             "D:\TFS\Dev\CppMicroAgent\prj\CppMicroAgent\output\Test.cpp" ^
             "D:\TFS\Dev\CppMicroAgent\prj\CppMicroAgent\output\gtest\gtest.lib" ^
             "D:\TFS\Dev\CppMicroAgent\prj\CppMicroAgent\output\gtest\gtest_main.lib" ^
             "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.43.34808\lib\x64\libcmtd.lib" ^
             "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.43.34808\lib\x64\libcpmtd.lib" ^
             "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.43.34808\lib\x64\oldnames.lib" ^
             "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.43.34808\lib\x64\libvcruntimed.lib" ^
             "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\um\x64\kernel32.lib" ^
             "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\um\x64\uuid.lib" ^
             "C:\Program Files (x86)\Windows Kits\10\Lib\10.0.22621.0\ucrt\x64\libucrtd.lib" ^
             /Fe"D:\TFS\Dev\CppMicroAgent\prj\CppMicroAgent\output\Test.exe"


            '''
        
        # Display the command for debugging purposes
        print("Running command:", " ".join(gpp_command))

        try:
            verbose_path = os.path.join(current_path, "output", "verbose.txt")

            if self.check_vc_installation():
                with open(verbose_path, "w") as verbose_file:
                    result = subprocess.run(
                        gpp_command,
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

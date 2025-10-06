import os
import platform

from ConfigReader import ConfigReader
from flow_manager import flow


class StateInit():

    def __init__(self):
        self.configReader = ConfigReader()

    def run(self, input_data):
        flow.transition("StateInit")
        print("[StateInit] Processing input:", input_data)
        
        # Check if we're on Linux
        if platform.system() == "Linux":
            if self.check_linux_toolchain():
                return self.check_ollama_installation(), input_data
            else:
                return False, input_data
        else:
            # Original Windows logic
            if (self.configReader.get_vc_installdir() != ""):
                if self.check_vc_installation():
                    return self.check_ollama_installation(), input_data
                else:
                    return False, input_data
            elif (self.check_mingw_installation()):
                return self.check_ollama_installation(), input_data
        return False, input_data
    
    def check_linux_toolchain(self):
        print("Verifying installation of Linux C++ toolchain...")
        
        # Check for g++
        gcc_path = self.configReader.get_gcc_compiler()
        if not os.path.exists(gcc_path):
            print(f"[StateInit] g++ not found at: {gcc_path}")
            return False
        
        # Check for gcov
        gcov_path = self.configReader.get_gcov_tool()
        if not os.path.exists(gcov_path):
            print(f"[StateInit] gcov not found at: {gcov_path}")
            return False
            
        # Check for lcov
        lcov_path = self.configReader.get_lcov_tool()
        if not os.path.exists(lcov_path):
            print(f"[StateInit] lcov not found at: {lcov_path}")
            return False
            
        print("[StateInit] Linux C++ toolchain found.")
        return True
    
    def check_vc_installation(self):
        print ("Verifying installation of Visual Studio...")
        vc_install_dir = self.configReader.get_vc_installdir()
        if os.path.exists(vc_install_dir):
            print("[StateInit] Visual Studio installation found.")
            return True
        else:
            print("[StateInit] Visual Studio installation missing!")
            return False

    def check_mingw_installation(self):
        print ("Verifying installation of MinGW...")
        # Get the directory two levels up from the current file location
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
        mingw_path = os.path.join(base_dir, "MinGW")
        mingw_bin_path = os.path.join(mingw_path, "bin")
        
        if os.path.exists(mingw_path) and os.path.exists(mingw_bin_path):
            print("[StateInit] MinGW installation found.")
            return True
        else:
            print("[StateInit] MinGW installation missing!")
            return False

    def check_ollama_installation(self):
        # Check Linux environment
        if platform.system() == "Linux":
            # Check if ollama is available in PATH
            import shutil
            if shutil.which('ollama') is not None:
                print("Ollama is installed and available in PATH")
                return self.check_ollama_models_linux()
            else:
                print("Ollama is not installed or not in PATH")
                return False
        else:
            # Original Windows logic
            # Expand environment variables
            ollama_dir = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama")
        
            # Check if the directory exists
            if os.path.exists(ollama_dir):
                print(f"Ollama is installed at: {ollama_dir}")
                return self.check_ollama_data_folder()
            else:
                print("Ollama is not installed in the default location.")
                return False

    def check_ollama_models_linux(self):
        """Check if the configured models are available in Linux"""
        try:
            import subprocess
            # Run 'ollama list' to get available models
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode != 0:
                print("Failed to list Ollama models")
                return False
                
            available_models = result.stdout
            
            # Check if our configured model is available
            model_name = self.configReader.get_model_used()
            if model_name in available_models:
                print(f"Ollama model '{model_name}' is available")
                return True
            else:
                print(f"Ollama model '{model_name}' is not found. Available models:")
                print(available_models)
                return False
                
        except Exception as e:
            print(f"Error checking Ollama models: {e}")
            return False

    def check_ollama_data_folder(self):
        # Expand environment variables to get the full path
        ollama_data_folder = os.path.expandvars(r"%USERPROFILE%\.ollama")
    
        # Check if the folder exists
        if os.path.exists(ollama_data_folder):
            print(f"Ollama data folder exists: {ollama_data_folder}")
            return self.check_ollama_data_model_specified_in_config()
        else:
            print("Ollama data folder not found.")
            return False

    def split_model_version(self, model_string):
        """Splits a model string like 'llama3.2:latest' into two parts: model name and version."""
        parts = model_string.split(":", 1)  # Split at the first colon
        if len(parts) == 2:
            return parts[0], parts[1]
        return parts[0], None  # If there's no colon, return the model name and None

    def check_ollama_data_model_specified_in_config(self):
        # Expand environment variables to get the full path
        ollama_data_folder = os.path.expandvars(r"%USERPROFILE%\.ollama")
    
        library_path = os.path.join(ollama_data_folder, "models\\manifests\\registry.ollama.ai\\library")
        
        model, version = self.split_model_version(self.configReader.get_model_used())
        model_path = os.path.join(library_path, model)
        specificModelPath = os.path.join(model_path, version)

        # Check if the folder exists
        if os.path.exists(specificModelPath):
            print(f"Ollama Model Exists: {ollama_data_folder}")
            return True
        else:
            print("Ollama model: " + model + ":" + version + " is not found.")
            return False




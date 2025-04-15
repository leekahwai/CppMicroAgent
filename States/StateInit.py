import os

from ConfigReader import ConfigReader
from flow_manager import flow



class StateInit():

    def __init__(self):
        self.configReader = ConfigReader()

    def run(self, input_data):
        flow.transition("StateInit")
        print("[StateInit] Processing input:", input_data)
        if (self.configReader.get_vc_installdir() != ""):
            if self.check_vc_installation():
                return self.check_ollama_installation(), input_data
            else:
                return False, input
        elif (self.check_mingw_installation()):
            return self.check_ollama_installation(), input_data
        return False, input_data
    
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
        # Expand environment variables
        ollama_dir = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Ollama")
    
        # Check if the directory exists
        if os.path.exists(ollama_dir):
            print(f"Ollama is installed at: {ollama_dir}")
            return self.check_ollama_data_folder()
        else:
            print("Ollama is not installed in the default location.")
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




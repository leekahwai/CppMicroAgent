from flow_manager import flow
import os
import re
import shutil
from States_Coverage.States_Function.StateMachine import StateMachine as StateMachineFunction
from States.Query import Query

class StateIterateSourceFiles():
    def __init__(self):
        print("Initializing [StateIterateSourceFiles]")

    import re

    # Function to handle C-style functions (e.g., `int main()`)
    def extract_c_style_functions(self, source_file):
        # Regex pattern for C-style functions (no class name, e.g., `int main()`)
        c_function_regex = r"([a-zA-Z_][a-zA-Z0-9_]*\s+)+([a-zA-Z_][a-zA-Z0-9_]*\s*)\(([^)]*)\)\s*(?:;|\{|\s*\})"

        function_list = []

        # Open the source C++ file
        with open(source_file, 'r') as file:
            file_contents = file.read()

            # Remove comments (single-line and multiline)
            file_contents = re.sub(r"//.*?$|/\*.*?\*/", "", file_contents, flags=re.DOTALL | re.MULTILINE)

            # Find all C-style function matches using regex
            functions = re.findall(c_function_regex, file_contents)

            # Add matched C functions to the function list
            for function in functions:
                # Format function name and parameters
                return_type_and_name = function[0].strip()
                function_name = function[1].strip()
                parameters = function[2].strip()

                # Store the function signature
                function_list.append({
                    'return_type_and_name': return_type_and_name,
                    'function_name': function_name,
                    'parameters': parameters
                })

        return function_list

    def extract_cpp_member_functions(self, source_file):
        cpp_function_regex = r"""
            (?:template\s*<[^>]+>\s*)?                              # Optional template<...>
            (?:
                (?:
                    (?P<ret_type>[A-Za-z_]\w*(?:\s*<[^>]+>)?        # Return type (e.g. int, MyType<T>)
                                  (?:\s*[*&]\s*)*)
                |
                    auto                                           # or 'auto' for trailing-return syntax
                )
                \s+
            )?                                                     # <-- now optional, so ctors/dtors match
            (?P<cls>[A-Za-z_]\w*::)                                # Class scope, e.g. Foo::
            (?P<name>~?[A-Za-z_]\w*)                               # Function name or destructor (~Foo)
            \s*\(                                                  # Opening paren for parameters
                (?P<params>[^\)]*)                                 #   everything up to ')'
            \)
            \s*(?:->\s*(?P<trailing_ret>[^\s\{;]+)\s*)?            # Optional trailing return
            (?:\s*const)?                                          # Optional 'const'
            (?:\s*:[^{;]+)?                                        # Optional constructor initializer list
            \s*(?:\{|;)                                            # '{' for body or ';' for declaration
        """

        with open(source_file, 'r') as f:
            contents = f.read()
        # strip comments
        contents = re.sub(r"//.*?$|/\*.*?\*/", "", contents,
                          flags=re.DOTALL | re.MULTILINE)

        function_list = []
        for m in re.finditer(cpp_function_regex, contents, flags=re.VERBOSE):
            cls        = m.group("cls")
            name       = m.group("name")
            params     = m.group("params").strip()
            # prefer trailing-return if present, else the normal return-type, else empty
            ret_type   = (m.group("trailing_ret") or m.group("ret_type") or "").strip()

            function_list.append({
                "return_type":   ret_type,
                "function_name": f"{cls}{name}",
                "parameters":    params
            })

        return function_list






    # Function that combines both C-style and C++ functions
    def extract_functions(self, source_file):
        # First, extract C-style functions
        c_functions = self.extract_c_style_functions(source_file)

        # Then, extract C++ member functions
        cpp_functions = self.extract_cpp_member_functions(source_file)

        # Combine both lists
        return c_functions + cpp_functions

    def extract_function_implementation(self, source_file, function_name):
        # 1) Read file and strip comments
        with open(source_file, 'r') as f:
            text = f.read()
        text = re.sub(r"//.*?$|/\*.*?\*/", "", text,
                      flags=re.DOTALL | re.MULTILINE)

        # 2) Build a regex for the signature up through the first '{'
        fn_re = re.escape(function_name)
        sig_pattern = (
            r"(?:template\s*<[^>]+>\s*)?"     # optional template<>
            r"[^\S\n]*"                       # any leading whitespace
            r"(?:[^\s]+\s+)*"                # optional return-type tokens
            + fn_re +                         # the function name
            r"\s*\([^)]*\)\s*"               # parameter list
            r"(?:const\s*)?"                 # optional 'const'
            r"(?:->\s*[^{\s]+?\s*)?"         # optional trailing-return
            r"\{"                            # the opening brace
        )

        # 3) Find the signature
        m = re.search(sig_pattern, text, flags=re.DOTALL)
        if not m:
            return None

        # 4) Locate the first brace and walk to its matching closing brace
        start = m.start()
        brace_idx = text.find("{", m.end() - 1)
        if brace_idx < 0:
            return None

        depth = 1
        idx = brace_idx + 1
        length = len(text)
        while idx < length and depth > 0:
            c = text[idx]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
            idx += 1

        if depth != 0:
            # Unbalanced braces
            return None

        # 5) Return the full implementation (signature + body)
        return text[start:idx]



    def run(self, input_data):
        flow.transition("StateIterateSourceFiles")
        print("[StateEnd] Reached StateIterateSourceFiles.")

        # Define the folder path
        unit_test_coverage_dir = os.path.join("output", "UnitTestCoverage")
    
        # Check if the folder already exists and remove it along with its contents
        if os.path.exists(unit_test_coverage_dir):
            print(f"Removing existing folder: {unit_test_coverage_dir}")
            shutil.rmtree(unit_test_coverage_dir)
    
        # Create the new folder
        print(f"Creating folder: {unit_test_coverage_dir}")
        os.makedirs(unit_test_coverage_dir)

        # Iterate each of the folders in input_data.get_source_files
        for file_path in input_data.get_source_files():
            # Generate subdirectory path based on file name or path
            file_name = os.path.basename(file_path)  # Get file name from the path
            subdirectory_path = os.path.join(unit_test_coverage_dir, file_name)
        
            # Create the subdirectory
            if not os.path.exists(subdirectory_path):
                    print(f"Creating subdirectory: {subdirectory_path}")
                    os.makedirs(subdirectory_path)
                # Read the cpp file and store the list of cpp and c functions in a list first. 
                #cmake_dir = input_data.get_input_data()  # Assuming input_data has a method to get the directory path
                #for dir in input_data.get_source_files():
                    # Join cmake_dir with each folder in include_dirs
                    file_path = file_path.lstrip('/')
                    cmake_dir = input_data.get_input_data()
                    sourceFile  = os.path.join(cmake_dir, file_path)#os.path.join(cmake_dir, dir)
                    # Extract C++/C functions from the source file
                    functions = self.extract_functions(sourceFile)

                    # Print the found functions (or do other processing)
                    for function in functions:
                        # Check if the function name contains '::' (class::function)
                        if '::' in function['function_name']:
                            # Extract class name and function name
                            class_name, func_name = function['function_name'].split('::')
        
                            # Generate the folder path for the class and function
                            class_folder = os.path.join(subdirectory_path, class_name)
                            function_folder = os.path.join(class_folder, func_name)

                            # Create the folder for the function inside the class folder
                            if not os.path.exists(function_folder):
                                print(f"Creating folder for function: {function_folder}")
                                os.makedirs(function_folder)
                                print(self.extract_function_implementation(sourceFile, function['function_name']))
                                print(self.extract_function_implementation(sourceFile, function['function_name']))
                                exact_implementation = self.extract_function_implementation(sourceFile, function['function_name'])

                                # 1. Your existing source file path
                                source_file = sourceFile

                                # 2. Derive the expected header filename (SampleApp.h)
                                base = os.path.splitext(os.path.basename(source_file))[0]
                                header_name = base + ".h"

                                # 3. Get the list of all header file paths
                                all_headers = input_data.get_include_folders()

                                # 4. Find the first header whose basename matches
                                header_file = next(
                                    (hdr for hdr in all_headers if os.path.basename(hdr).lower() == header_name.lower()),
                                    None
                                )
                                if header_file is None:
                                    raise FileNotFoundError(f"Could not find {header_name} in include list")

                                source_content = ""
                                header_content = ""

                                # 5. Read both files into variables
                                with open(source_file, 'r', encoding='utf-8') as f:
                                    source_content = f.read()

                                with open(header_file, 'r', encoding='utf-8') as f:
                                    header_content = f.read()

                                # Now source_content and header_content contain the full text of each file
                                # ——— now, if you only want the two filenames (no path) ———
                                cpp_filename  = os.path.basename(source_file)   # → "SampleApp.cpp"
                                h_filename    = os.path.basename(header_file)   # → "SampleApp.h"

                                query = input_data
                                query.set_current_output_folder(function_folder)
                                query.set_current_include(header_file)
                                query.set_current_source(source_file)
                                query.set_current_header_content(header_content)
                                query.set_current_source_content(source_content)
                                query.set_current_implementation_content(exact_implementation)
                                
                                sm = StateMachineFunction(query)
                                sm.run()
                        else:
                            # If it's just a function name (no class), create a folder for the function
                            function_folder = os.path.join(subdirectory_path, function['function_name'])
        
                            # Create the folder for the function if it doesn't exist
                            if not os.path.exists(function_folder):
                                print(f"Creating folder for function: {function_folder}")
                                os.makedirs(function_folder)
                                print(self.extract_function_implementation(sourceFile, function['function_name']))
                                exact_implementation = self.extract_function_implementation(sourceFile, function['function_name'])

                                # 1. Your existing source file path
                                source_file = sourceFile

                                # 2. Derive the expected header filename (SampleApp.h)
                                base = os.path.splitext(os.path.basename(source_file))[0]
                                header_name = base + ".h"

                                # 3. Get the list of all header file paths
                                all_headers = input_data.get_include_folders()

                                # 4. Find the first header whose basename matches
                                header_file = next(
                                    (hdr for hdr in all_headers if os.path.basename(hdr).lower() == header_name.lower()),
                                    None
                                )
                                if header_file is None:
                                    raise FileNotFoundError(f"Could not find {header_name} in include list")

                                source_content = ""
                                header_content = ""

                                # 5. Read both files into variables
                                with open(source_file, 'r', encoding='utf-8') as f:
                                    source_content = f.read()

                                with open(header_file, 'r', encoding='utf-8') as f:
                                    header_content = f.read()

                                # Now source_content and header_content contain the full text of each file
                                # ——— now, if you only want the two filenames (no path) ———
                                cpp_filename  = os.path.basename(source_file)   # → "SampleApp.cpp"
                                h_filename    = os.path.basename(header_file)   # → "SampleApp.h"

                                query = input_data
                                query.set_current_output_folder(function_folder)
                                query.set_current_include(header_file)
                                query.set_current_source(source_file)
                                query.set_current_header_content(header_content)
                                query.set_current_source_content(source_content)
                                query.set_current_implementation_content(exact_implementation)
                                
                                sm = StateMachineFunction(query)
                                sm.run()

    
        print(f"[StateEnd] Reached {unit_test_coverage_dir} creation state.")

        return False, None # Stop state machine


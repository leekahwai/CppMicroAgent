from ..flow_manager import flow
import os
import re

class StateParseCMake():
    def __init__(self):
        print("Initializing [StateParseCMake]")

    def run(self, input_data):
        cmake_dir = input_data.get_input_data()  # Assuming input_data has a method to get the directory path
        cmake_file = os.path.join(cmake_dir, "CMakeLists.txt")
        
        # Initialize lists to store the source files and include directories
        source_files = []
        include_dirs = []

        if os.path.exists(cmake_file):
            with open(cmake_file, 'r') as file:
                cmake_content = file.read()

                # Extract sources from the SOURCES variable
                sources_match = re.search(r'set\(\s*SOURCES\s+(.*?)\)', cmake_content, re.DOTALL)
                if sources_match:
                    sources = sources_match.group(1).strip()
                    # Split by new lines or spaces
                    source_files = [file.strip() for file in sources.splitlines() if file.strip()]

                # Extract include directories from the include_directories call
                include_match = re.findall(r'include_directories\(\s*(.*?)\)', cmake_content, re.DOTALL)
                if include_match:
                    for includes in include_match:
                        include_dirs.extend([dir.strip() for dir in includes.splitlines() if dir.strip()])

                # Find all options and process them dynamically
                options_match = re.findall(r'option\(\s*(USE_[A-Za-z_]+)\s+"[^\"]+"\s+(ON|OFF)\)', cmake_content)
                for option_name, option_value in options_match:
                    if option_value == "ON":
                        # Find the corresponding include() call for this option
                        if_block_match = re.search(r'if\s*\(\s*' + re.escape(option_name) + r'\s*\)\s*(.*?)\s*endif\(\)', cmake_content, re.DOTALL)
                        
                        # If the block exists, process the cmake file inside
                        if if_block_match:
                            if_block_content = if_block_match.group(1).strip()
                            
                            # Look for the include statement within the if block and extract the cmake file path
                            include_match = re.findall(r'include\(\s*(.*?)\)', if_block_content)
                            for include_file in include_match:
                                cmake_file_path = os.path.join(cmake_dir, include_file.strip())
                                # Replace ${CMAKE_SOURCE_DIR} with the actual cmake_dir path
                                cmake_file_path = cmake_file_path.strip().replace("${CMAKE_SOURCE_DIR}", "")
           
                                self._process_additional_cmake(cmake_dir, cmake_file_path, source_files, include_dirs)

            # Now remove "${CMAKE_SOURCE_DIR}" from both source_files and include_dirs
            source_files = [file.replace("${CMAKE_SOURCE_DIR}", "") for file in source_files]
            include_dirs = [dir.replace("${CMAKE_SOURCE_DIR}", "") for dir in include_dirs]


            # Print the lists or process them as needed
            print("Source Files:", source_files)
            print("Include Directories:", include_dirs)

            # Create a new list to hold the updated include directories
            updated_include_dirs = []

            # Iterate over each directory in include_dirs and prepend cmake_dir
            updated_include_dirs.append(os.path.join(cmake_dir,""))
            for dir in include_dirs:
                # Join cmake_dir with each folder in include_dirs
                updated_include_dirs.append(os.path.join(cmake_dir, dir))

            # This will store the unique headers
            final_include_dirs = set()

            # Iterate over each directory in the updated include_dirs
            for dir in updated_include_dirs:
                # Check if the directory exists
                if os.path.isdir(dir):
                    # Walk through the directory to find .h and .hpp files
                    for root, dirs, files in os.walk(dir):
                        for file in files:
                            if file.endswith(('.h', '.hpp')):  # Check if it's a header file
                                # Add the full path to the set to ensure uniqueness
                                final_include_dirs.add(os.path.join(root, file))

            # Normalize paths (Linux uses forward slashes)
            normalized_include_dirs = [os.path.normpath(dir) for dir in final_include_dirs]

            # Filter out paths containing 'out/build' (Linux equivalent)
            filtered_include_dirs = [dir for dir in normalized_include_dirs if 'out/build' not in dir and 'out\\build' not in dir]

            # Remove duplicates and sort the paths
            include_dirs = sorted(set(filtered_include_dirs))



            # Print the updated include_dirs
            print("Updated Include Directories:", include_dirs)

            # Assuming input_data has the methods set_source_files and set_include_folders
            input_data.set_source_files(source_files)
            input_data.set_include_folders(include_dirs)
        else:
            print(f"Error: The CMakeLists.txt file does not exist in the provided directory: {cmake_dir}")
            return False, None # Stop state machine
        return True, input_data

    def _process_additional_cmake(self, cmake_dir, cmake_file, source_files, include_dirs):
        # Process additional CMake file for sources and include directories
        cmake_file_path = os.path.join(cmake_dir, cmake_file)

        if os.path.exists(cmake_file_path):
            with open(cmake_file_path, 'r') as file:
                cmake_content = file.read()

                # Extract sources from list(APPEND SOURCES ...)
                sources_match = re.findall(r'list\(\s*APPEND\s*SOURCES\s+(.*?)\)', cmake_content, re.DOTALL)
                for match in sources_match:
                    sources = match.strip()
                    # Split by new lines or spaces
                    source_files.extend([file.strip() for file in sources.splitlines() if file.strip()])

                # Extract include directories from include_directories call
                include_match = re.findall(r'include_directories\(\s*(.*?)\)', cmake_content, re.DOTALL)
                for includes in include_match:
                    include_dirs.extend([dir.strip() for dir in includes.splitlines() if dir.strip()])
        else:
            print(f"Error: The additional CMake file does not exist: {cmake_file_path}")
import re
from States.Query import Query

class CodeWriter:
    def __init__(self, input_data: Query, cpp_code: str, directory: str, filename: str = "", flagUT :bool = False):
        self.input_data = input_data
        self.cpp_code = cpp_code
        self.directory = directory
        self.class_name = None
        self.filename = filename
        self.flagUT = flagUT

    def set_class_name(self, data:str):
        self.class_name = data

    def extract_class_name(self):
        """Extracts the class name from the C++ code while ignoring comments."""
        lines = self.cpp_code.split("\n")
        inside_comment = False  # To track multi-line comments

        for line in lines:
            line = line.strip()

            # Handle multi-line comments
            if "/*" in line:
                inside_comment = True
            if "*/" in line:
                inside_comment = False
                continue  # Skip this line

            if inside_comment or line.startswith("//"):
                continue  # Skip commented lines

            # Find a class definition
            if self.filename != "":
                self.class_name = self.filename
                return
            else:
                match = re.match(r"class\s+([A-Za-z_]\w*)", line)
                if match:
                    self.class_name = match.group(1)
                    return

        raise ValueError("No valid class definition found in the provided C++ code.")

    def process_code(self, already_has_name=False):
        """Removes the first and last lines of the C++ code and saves it as <ClassName>.h."""
        lines = self.cpp_code.strip().split("\n")

        if len(lines) < 2:
            raise ValueError("Code is too short to process.")

        # Remove first and last line
        processed_lines = lines[1:-1]

        # Extract class name
        if (already_has_name == False):
            self.extract_class_name()

        # Save the processed content
        extension = ".h"
        if (self.filename != "") and (already_has_name == False):
            extension = ".cpp"

        

        curr_filename = f"{self.class_name}" + extension
        output_file = "" + self.directory + "/" +  curr_filename

        if self.flagUT == True:
            self.input_data.set_generated_ut_file(curr_filename)
        else:
            self.input_data.set_generated_code(curr_filename)

        
        with open(output_file, "w") as file:
            file.write("\n".join(processed_lines) + "\n")

        print(f"Processed file saved as {output_file}")
        return curr_filename

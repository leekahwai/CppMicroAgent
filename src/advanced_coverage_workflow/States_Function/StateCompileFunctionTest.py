"""
StateCompileFunctionTest - Compile the generated test with retry logic
"""

from ...flow_manager import flow
from ...OllamaClient import OllamaClient
from ...ConfigReader import ConfigReader
import os
import subprocess
import json

class StateCompileFunctionTest():
    def __init__(self):
        self.client = OllamaClient()
        self.configReader = ConfigReader()
        self.max_retries = 3
        print("Initializing [States_Function::StateCompileFunctionTest]")

    def run(self, input_data):
        flow.transition("States_Function::StateCompileFunctionTest")
        print("[StateCompileFunctionTest] Compiling function test...")

        test_file = input_data.get_generated_ut_file()
        output_folder = input_data.get_current_output_folder()
        
        if not test_file or not os.path.exists(test_file):
            print("[StateCompileFunctionTest] No test file found!")
            return False, input_data
        
        # Try to compile, retry with error feedback if it fails
        retry_count = 0
        compilation_successful = False
        
        while retry_count < self.max_retries and not compilation_successful:
            print(f"\n[StateCompileFunctionTest] Compilation attempt {retry_count + 1}/{self.max_retries}")
            
            success, error_output = self._compile_test(test_file, output_folder, input_data)
            
            if success:
                compilation_successful = True
                print("[StateCompileFunctionTest] ✅ Compilation successful!")
            else:
                retry_count += 1
                print(f"[StateCompileFunctionTest] ❌ Compilation failed (attempt {retry_count})")
                
                if retry_count < self.max_retries:
                    print("[StateCompileFunctionTest] Regenerating test with error feedback...")
                    # Regenerate test with error feedback
                    new_test_code = self._regenerate_test_with_error(
                        input_data, 
                        error_output,
                        retry_count
                    )
                    
                    if new_test_code:
                        # Save the corrected test
                        with open(test_file, 'w', encoding='utf-8') as f:
                            f.write(new_test_code)
                        input_data.set_generated_code(new_test_code)
                        print(f"[StateCompileFunctionTest] Test regenerated, retrying compilation...")
                    else:
                        print("[StateCompileFunctionTest] Failed to regenerate test")
                        break
        
        if compilation_successful:
            return True, input_data
        else:
            print(f"[StateCompileFunctionTest] ❌ Failed to compile after {self.max_retries} attempts")
            return False, input_data

    def _compile_test(self, test_file, output_folder, input_data):
        """Compile the test file with coverage flags"""
        
        # Get project information
        project_path = input_data.get_input_data()
        source_file = input_data.get_current_source()
        
        # Create a temporary build directory for this function test
        build_dir = os.path.join(output_folder, "build")
        os.makedirs(build_dir, exist_ok=True)
        
        # Prepare compilation command
        # We need to compile: test file + original source file (function implementation)
        executable = os.path.join(build_dir, "test_executable")
        
        # Build include paths - ORDER MATTERS!
        # 1. Mock headers FIRST (highest priority) so they override real dependencies
        # 2. Source file directory (for the actual header being tested)
        # 3. Project directories (for any other includes)
        include_paths = [
            f"-I{output_folder}",  # Mock headers FIRST
            f"-I{os.path.dirname(source_file)}",  # Source directory with real header
            f"-I{project_path}",
            f"-I{project_path}/inc",
            f"-I{project_path}/src",
        ]
        
        # Add all subdirectories under project as includes (for finding headers)
        for root, dirs, files in os.walk(project_path):
            if 'build' not in root and '.git' not in root:
                include_paths.append(f"-I{root}")
        
        # Compilation flags with coverage
        compile_flags = [
            "-std=c++17",
            "-g",
            "-O0",
            "--coverage",
            "-fprofile-arcs",
            "-ftest-coverage"
        ]
        
        # Find googletest paths
        googletest_base = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "googletest-1.16.0")
        gtest_include = os.path.join(googletest_base, "googletest", "include")
        gtest_src_dir = os.path.join(googletest_base, "googletest")
        gtest_all = os.path.join(googletest_base, "googletest", "src", "gtest-all.cc")
        gtest_main = os.path.join(googletest_base, "googletest", "src", "gtest_main.cc")
        
        # Build the compilation command
        # Include gtest source files directly if libraries are not available
        # Use absolute paths for all files to avoid path issues when running from build_dir
        abs_test_file = os.path.abspath(test_file)
        abs_source_file = os.path.abspath(source_file)
        abs_gtest_all = os.path.abspath(gtest_all)
        abs_gtest_main = os.path.abspath(gtest_main)
        
        compile_cmd = [
            "g++",
            *compile_flags,
            *include_paths,
            f"-I{gtest_include}",
            f"-I{gtest_src_dir}",
            abs_test_file,
            abs_source_file,
            abs_gtest_all,
            abs_gtest_main,
            "-lpthread",
            "-o", executable
        ]
        
        print(f"[StateCompileFunctionTest] Compile command: {' '.join(compile_cmd)}")
        
        try:
            result = subprocess.run(
                compile_cmd,
                cwd=build_dir,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"[StateCompileFunctionTest] Executable created: {executable}")
                # Store executable path for coverage state
                input_data.set_generated_ut_file(executable)
                return True, ""
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                print(f"[StateCompileFunctionTest] Compilation error:\n{error_msg}")
                return False, error_msg
                
        except subprocess.TimeoutExpired:
            print("[StateCompileFunctionTest] Compilation timed out")
            return False, "Compilation timed out after 60 seconds"
        except Exception as e:
            print(f"[StateCompileFunctionTest] Compilation exception: {e}")
            return False, str(e)

    def _regenerate_test_with_error(self, input_data, error_output, retry_count):
        """Regenerate test with compilation error feedback"""
        
        print("[StateCompileFunctionTest] Asking LLM to fix compilation errors...")
        
        original_code = input_data.get_generated_code()
        function_implementation = input_data.get_current_implementation_content()
        header_content = input_data.get_current_header_content()
        output_folder = input_data.get_current_output_folder()
        
        # List available mock headers
        mock_headers = []
        if os.path.exists(output_folder):
            mock_headers = [f for f in os.listdir(output_folder) if f.endswith('.h')]
        
        # Create error correction prompt
        prompt = f"""The following Google Test code failed to compile. Please fix ALL compilation errors and generate a corrected version.

ORIGINAL TEST CODE (DOES NOT COMPILE):
```cpp
{original_code}
```

COMPILATION ERRORS:
```
{error_output[:2000]}
```

FUNCTION BEING TESTED:
```cpp
{function_implementation}
```

HEADER FILE:
```cpp
{header_content[:1000]}
```

AVAILABLE MOCK HEADERS IN THE SAME DIRECTORY:
{', '.join(mock_headers) if mock_headers else 'None'}

IMPORTANT INSTRUCTIONS:
1. Fix ALL compilation errors shown above
2. Common issues to check:
   - Missing #include statements
   - Incorrect header paths (use quotes for local headers)
   - Missing namespace qualifiers
   - Undefined types or functions
   - Incorrect mock usage
   - Missing variable initializations
3. Include mock headers using: #include "MockHeaderName.h"
4. Make sure all types are properly defined
5. Ensure test compiles with: g++ -std=c++17 -I. -lgtest -lgtest_main -lpthread

RETRY ATTEMPT: {retry_count}/{self.max_retries}

Generate ONLY the corrected C++ test code, no explanations:
"""
        
        try:
            response_str = self.client.query(self.configReader.get_gtest_model(), prompt)
            
            # Parse response
            response_text = ""
            responses = response_str.strip().split("\n")
            
            for resp in responses:
                try:
                    response_json = json.loads(resp)
                    if not response_json.get("done", False):
                        response_text += response_json.get("response", "")
                except json.JSONDecodeError:
                    continue
            
            # Clean the code
            cleaned_code = self._clean_test_code(response_text)
            return cleaned_code
            
        except Exception as e:
            print(f"[StateCompileFunctionTest] Error regenerating test: {e}")
            return None

    def _clean_test_code(self, response_text):
        """Clean and format the generated test code"""
        
        if not response_text:
            return ""
        
        # Remove markdown code blocks
        lines = response_text.split('\n')
        cleaned_lines = []
        in_code_block = False
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block or not stripped.startswith('```'):
                cleaned_lines.append(line)
        
        cleaned_code = '\n'.join(cleaned_lines).strip()
        
        # Ensure gtest include
        if '#include <gtest/gtest.h>' not in cleaned_code and '#include "gtest/gtest.h"' not in cleaned_code:
            cleaned_code = '#include <gtest/gtest.h>\n\n' + cleaned_code
        
        return cleaned_code

"""
StateGenerateFunctionTest - Generate unit test for a specific function
"""

from ...flow_manager import flow
from ...OllamaClient import OllamaClient
from ...ConfigReader import ConfigReader
from ...CodeWriter import CodeWriter
import os
import json

class StateGenerateFunctionTest():
    def __init__(self):
        self.client = OllamaClient()
        self.configReader = ConfigReader()
        print("Initializing [States_Function::StateGenerateFunctionTest]")

    def run(self, input_data):
        flow.transition("States_Function::StateGenerateFunctionTest")
        print("[StateGenerateFunctionTest] Generating unit test for function...")

        # Get function-specific information
        function_implementation = input_data.get_current_implementation_content()
        header_content = input_data.get_current_header_content()
        source_content = input_data.get_current_source_content()
        output_folder = input_data.get_current_output_folder()
        
        # Extract function name from the implementation or current context
        function_name = self._extract_function_name(function_implementation)
        
        print(f"[StateGenerateFunctionTest] Generating test for function: {function_name}")
        
        # Create prompt for test generation
        prompt = self._create_test_generation_prompt(
            function_name,
            function_implementation,
            header_content,
            source_content,
            output_folder
        )
        
        # Query LLM for test generation
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
                        print(response_json.get("response", ""), end="")
                except json.JSONDecodeError:
                    continue
            
            # Clean and format the test code
            test_code = self._clean_test_code(response_text)
            
            # Save the test file
            test_filename = os.path.join(output_folder, f"test_{function_name}.cpp")
            with open(test_filename, 'w', encoding='utf-8') as f:
                f.write(test_code)
            
            print(f"\n[StateGenerateFunctionTest] Test saved: {test_filename}")
            
            # Store test file path in input_data for next state
            input_data.set_generated_ut_file(test_filename)
            input_data.set_generated_code(test_code)
            
            return True, input_data
            
        except Exception as e:
            print(f"[StateGenerateFunctionTest] Error generating test: {e}")
            return False, input_data

    def _extract_function_name(self, implementation):
        """Extract function name from implementation"""
        if not implementation:
            return "unknown_function"
        
        # Simple extraction - get first word after first opening parenthesis
        lines = implementation.split('\n')
        for line in lines:
            line = line.strip()
            if '(' in line and not line.startswith('//'):
                # Extract function name
                before_paren = line.split('(')[0]
                parts = before_paren.split()
                if parts:
                    func_name = parts[-1]
                    # Remove any namespace/class qualifiers
                    if '::' in func_name:
                        func_name = func_name.split('::')[-1]
                    # Remove any special characters
                    func_name = func_name.replace('*', '').replace('&', '').strip()
                    if func_name and not func_name.startswith('~'):
                        return func_name
                    elif func_name.startswith('~'):
                        return func_name[1:]  # Return destructor name without ~
        
        return "unknown_function"

    def _create_test_generation_prompt(self, function_name, implementation, header_content, source_content, output_folder):
        """Create comprehensive prompt for test generation"""
        
        # List mock headers available in the output folder
        mock_headers = []
        if os.path.exists(output_folder):
            mock_headers = [f for f in os.listdir(output_folder) if f.endswith('.h')]
        
        prompt = f"""Generate a complete, compilable Google Test (gtest) unit test for the following C++ function.

FUNCTION TO TEST:
```cpp
{implementation}
```

HEADER CONTEXT:
```cpp
{header_content}
```

SOURCE FILE CONTEXT:
```cpp
{source_content}
```

AVAILABLE MOCK HEADERS (already generated in the same directory):
{', '.join(mock_headers) if mock_headers else 'None'}

REQUIREMENTS:
1. Generate ONLY the test file code, no explanations
2. Include all necessary headers:
   - #include <gtest/gtest.h>
   - Include the original header file
   - Include any mock headers from the list above
3. Create a complete test suite with:
   - TEST() macro (or TEST_F() if using fixtures)
   - Meaningful test name: TEST(FunctionNameTest, TestCase)
   - Multiple test cases covering:
     * Normal/happy path
     * Edge cases
     * Boundary conditions
     * Error conditions (if applicable)
4. The test MUST compile without errors
5. Use proper assertions (EXPECT_*, ASSERT_*)
6. Mock any external dependencies using the available mock headers
7. Initialize all required variables and objects
8. Test ONLY the function: {function_name}
9. Make sure all paths and includes are correct
10. Do not include main() function - gtest provides it

OUTPUT FORMAT:
- Start with #include statements
- Then test code
- No markdown, no explanations, just pure C++ code
- Ensure code is complete and compilable

Generate the test code now:
"""
        return prompt

    def _clean_test_code(self, response_text):
        """Clean and format the generated test code"""
        
        if not response_text:
            return ""
        
        # Remove markdown code blocks if present
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
        
        # Ensure proper gtest include if not present
        if '#include <gtest/gtest.h>' not in cleaned_code and '#include "gtest/gtest.h"' not in cleaned_code:
            cleaned_code = '#include <gtest/gtest.h>\n\n' + cleaned_code
        
        return cleaned_code

import os
import subprocess
import tempfile
from ..flow_manager import flow
from ..ConfigReader import ConfigReader
from ..OllamaClient import OllamaClient
from ..CodeWriter import CodeWriter
import json

class StateGenerateUnitTests():
    def __init__(self):
        self.configReader = ConfigReader()
        self.client = OllamaClient()
        print("Initializing [StateGenerateUnitTests]")

    def run(self, input_data):
        flow.transition("StateGenerateUnitTests")
        print("[StateGenerateUnitTests] Generating comprehensive unit tests...")
        
        # Get coverage data to identify gaps
        coverage_data = input_data.get_coverage_data()
        cmake_dir = input_data.get_input_data()
        
        # Generate unit tests for each function based on coverage analysis
        self._generate_comprehensive_unit_tests(input_data, coverage_data, cmake_dir)
        
        print("[StateGenerateUnitTests] Unit test generation completed")
        return True, input_data

    def _generate_comprehensive_unit_tests(self, input_data, coverage_data, cmake_dir):
        """Generate comprehensive unit tests based on coverage analysis"""
        
        output_dir = "output/UnitTestCoverage"
        unit_tests_dir = os.path.join(output_dir, "unit_tests")
        os.makedirs(unit_tests_dir, exist_ok=True)
        
        source_files = input_data.get_source_files()
        
        for source_file in source_files:
            if source_file.startswith('/'):
                source_file = source_file[1:]
            
            source_path = os.path.join(cmake_dir, source_file)
            if not os.path.exists(source_path):
                continue
                
            print(f"[StateGenerateUnitTests] Generating tests for: {source_file}")
            
            # Read source content
            with open(source_path, 'r', encoding='utf-8') as f:
                source_content = f.read()
            
            # Get corresponding header file
            header_file = self._find_header_file(source_file, input_data.get_include_folders())
            header_content = ""
            if header_file:
                try:
                    with open(header_file, 'r', encoding='utf-8') as f:
                        header_content = f.read()
                except:
                    pass
            
            # Generate unit test using LLM
            test_content = self._generate_unit_test_with_llm(
                source_file, source_content, header_content, coverage_data
            )
            
            if test_content:
                # Save unit test file
                test_filename = f"test_{os.path.basename(source_file).replace('.cpp', '.cpp')}"
                test_path = os.path.join(unit_tests_dir, test_filename)
                
                with open(test_path, 'w') as f:
                    f.write(test_content)
                
                print(f"[StateGenerateUnitTests] Generated: {test_path}")

    def _find_header_file(self, source_file, include_folders):
        """Find corresponding header file for a source file"""
        base_name = os.path.splitext(os.path.basename(source_file))[0]
        header_name = base_name + ".h"
        
        for header_path in include_folders:
            if os.path.basename(header_path).lower() == header_name.lower():
                return header_path
        return None

    def _generate_unit_test_with_llm(self, source_file, source_content, header_content, coverage_data):
        """Generate comprehensive unit test using LLM with coverage awareness"""
        
        # Analyze coverage gaps for this specific file
        coverage_info = self._analyze_coverage_for_file(source_file, coverage_data)
        
        # Create comprehensive prompt for unit test generation
        prompt = self._create_unit_test_prompt(source_file, source_content, header_content, coverage_info)
        
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
                except:
                    continue
            
            return self._clean_and_format_test_code(response_text)
            
        except Exception as e:
            print(f"[StateGenerateUnitTests] Error generating test for {source_file}: {e}")
            return None

    def _analyze_coverage_for_file(self, source_file, coverage_data):
        """Analyze coverage gaps for a specific source file"""
        
        coverage_info = {
            "file": source_file,
            "has_coverage_data": False,
            "uncovered_lines": [],
            "uncovered_functions": [],
            "coverage_percentage": 0.0,
            "recommendations": []
        }
        
        if not coverage_data or "error" in coverage_data:
            coverage_info["recommendations"].append("Generate comprehensive tests (no coverage data available)")
            return coverage_info
        
        # Check if we have specific coverage data for this file
        build_dir = coverage_data.get("build_dir", "")
        if build_dir:
            # Look for .gcov file for this source file
            gcov_file = os.path.join(build_dir, f"{os.path.basename(source_file)}.gcov")
            if os.path.exists(gcov_file):
                coverage_info["has_coverage_data"] = True
                coverage_info.update(self._parse_gcov_file(gcov_file))
        
        # Generate recommendations based on coverage
        if coverage_info["coverage_percentage"] < 50:
            coverage_info["recommendations"].extend([
                "Focus on basic functionality tests",
                "Test all public methods",
                "Add boundary condition tests"
            ])
        elif coverage_info["coverage_percentage"] < 80:
            coverage_info["recommendations"].extend([
                "Add edge case testing",
                "Test error conditions",
                "Improve branch coverage"
            ])
        else:
            coverage_info["recommendations"].extend([
                "Add comprehensive integration tests",
                "Test complex scenarios",
                "Verify exception handling"
            ])
        
        return coverage_info

    def _parse_gcov_file(self, gcov_file):
        """Parse .gcov file to extract uncovered lines and functions"""
        
        result = {
            "uncovered_lines": [],
            "covered_lines": [],
            "coverage_percentage": 0.0
        }
        
        try:
            with open(gcov_file, 'r') as f:
                lines = f.readlines()
            
            total_lines = 0
            covered_lines = 0
            
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        execution_count = parts[0].strip()
                        source_line_num = parts[1].strip()
                        source_code = parts[2].strip()
                        
                        # Skip empty lines and comments
                        if not source_code or source_code.startswith('//') or source_code.startswith('/*'):
                            continue
                        
                        total_lines += 1
                        
                        if execution_count == '#####':
                            # Uncovered line
                            result["uncovered_lines"].append({
                                "line_number": source_line_num,
                                "code": source_code
                            })
                        elif execution_count.isdigit() and int(execution_count) > 0:
                            # Covered line
                            covered_lines += 1
                            result["covered_lines"].append({
                                "line_number": source_line_num,
                                "code": source_code,
                                "execution_count": int(execution_count)
                            })
            
            if total_lines > 0:
                result["coverage_percentage"] = (covered_lines / total_lines) * 100
                
        except Exception as e:
            print(f"[StateGenerateUnitTests] Error parsing gcov file {gcov_file}: {e}")
        
        return result

    def _create_unit_test_prompt(self, source_file, source_content, header_content, coverage_info):
        """Create comprehensive prompt for unit test generation"""
        
        # Extract the header filename from source_file
        source_header = os.path.splitext(os.path.basename(source_file))[0] + ".h"
        
        prompt = f"""Generate comprehensive unit tests using Google Test (gtest) framework for the following C++ source file.

TARGET FILE: {source_file}

SOURCE CODE:
```cpp
{source_content}
```

HEADER FILE:
```cpp
{header_content}
```

REQUIRED INCLUDES:
The unit test MUST include the following headers:
- #include "{source_header}" (the header file for the source being tested)
- #include <iostream>
- #include <string>
- #include <vector>
- #include <gtest/gtest.h>

COVERAGE ANALYSIS:
- Current coverage: {coverage_info['coverage_percentage']:.1f}%
- Has coverage data: {coverage_info['has_coverage_data']}
"""

        if coverage_info['uncovered_lines']:
            prompt += f"\nUNCOVERED LINES ({len(coverage_info['uncovered_lines'])} lines):\n"
            for line_info in coverage_info['uncovered_lines'][:10]:  # Show first 10
                prompt += f"  Line {line_info['line_number']}: {line_info['code']}\n"
            
            if len(coverage_info['uncovered_lines']) > 10:
                prompt += f"  ... and {len(coverage_info['uncovered_lines']) - 10} more lines\n"

        if coverage_info['recommendations']:
            prompt += f"\nTEST GENERATION FOCUS:\n"
            for rec in coverage_info['recommendations']:
                prompt += f"- {rec}\n"

        prompt += """

REQUIREMENTS:
1. Generate complete, compilable unit tests using Google Test (gtest/gmock)
2. Include all necessary #include statements
3. Create tests that specifically target uncovered code paths
4. Test edge cases, boundary conditions, and error scenarios
5. Use proper test fixtures and setup/teardown if needed
6. Mock external dependencies appropriately
7. Ensure tests are independent and can run in any order
8. Add comprehensive assertions to verify behavior
9. Include tests for constructor, destructor, and all public methods
10. Focus on achieving high line and branch coverage

UNIT TEST STRUCTURE:
- Use TEST() or TEST_F() macros
- Create meaningful test names that describe what is being tested
- Group related tests logically
- Include both positive and negative test cases

Generate ONLY the complete unit test code, no explanations.
"""

        return prompt

    def _clean_and_format_test_code(self, response_text):
        """Clean and format the generated test code"""
        
        if not response_text:
            return None
        
        # Remove markdown code blocks if present
        lines = response_text.split('\n')
        cleaned_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block or not line.strip().startswith('```'):
                cleaned_lines.append(line)
        
        cleaned_code = '\n'.join(cleaned_lines).strip()
        
        # Ensure proper includes if not present
        if '#include <gtest/gtest.h>' not in cleaned_code and '#include "gtest/gtest.h"' not in cleaned_code:
            cleaned_code = '#include <gtest/gtest.h>\n' + cleaned_code
        
        return cleaned_code
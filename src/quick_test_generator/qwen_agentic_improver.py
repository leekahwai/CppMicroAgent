#!/usr/bin/env python3
"""
Qwen CLI Agentic Test Generation Improvement Tool
Uses Qwen CLI with agentic capabilities to actually modify and create Python files
to make the parser and unit test generation more robust.

IMPORTANT: This tool improves the PYTHON code that generates C++ tests.
It does NOT create C++ test files directly.

WORKFLOW:
1. Option 3 (this tool) - Improves Python parser and test generator code
2. Option 1 - Uses the improved Python code to generate C++ unit tests  
3. Option 2 - Measures coverage of the generated C++ tests

This tool leverages qwen's --yolo mode to automatically apply improvements to:
- src/improved_cpp_parser.py (Python code that parses C++ files)
- src/ultimate_test_generator.py (Python code that generates C++ tests)
- src/quick_test_generator/test_utilities.py (Python utilities for test generation)
"""

import os
import re
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from config_reader import get_project_path, get_unittest_model


def run_qwen_agentic(prompt: str, yolo: bool = True) -> Tuple[bool, str]:
    """Run qwen CLI in agentic mode to make actual code changes
    
    Args:
        prompt: The instruction prompt for qwen
        yolo: If True, uses --yolo mode for automatic approval
    
    Returns:
        Tuple of (success, output)
    """
    print(f"\n🤖 Running Qwen CLI in {'YOLO (auto-approve)' if yolo else 'interactive'} mode...")
    
    cmd = ["qwen", "-p", prompt]
    if yolo:
        cmd.append("--yolo")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout for complex changes
            cwd=str(Path(__file__).parent.parent.parent)  # Run from repo root
        )
        
        output = result.stdout + result.stderr
        success = result.returncode == 0
        
        if success:
            print("✅ Qwen CLI completed successfully")
        else:
            print(f"⚠️  Qwen CLI returned code {result.returncode}")
        
        return success, output
        
    except subprocess.TimeoutExpired:
        print("❌ Qwen CLI timed out after 5 minutes")
        return False, "Timeout"
    except Exception as e:
        print(f"❌ Error running Qwen CLI: {e}")
        return False, str(e)


def analyze_project_structure(project_path: str) -> Dict:
    """Analyze the project structure to understand patterns"""
    print(f"\n📂 Analyzing project structure: {project_path}")
    
    analysis = {
        "source_files": [],
        "header_files": [],
        "class_patterns": [],
        "common_includes": set(),
        "namespace_patterns": [],
        "template_usage": False,
        "project_name": Path(project_path).name
    }
    
    # Find all C++ files
    for ext in ['*.cpp', '*.cc', '*.cxx']:
        analysis["source_files"].extend(Path(project_path).rglob(ext))
    
    for ext in ['*.h', '*.hpp', '*.hxx']:
        analysis["header_files"].extend(Path(project_path).rglob(ext))
    
    print(f"  Found {len(analysis['source_files'])} source files")
    print(f"  Found {len(analysis['header_files'])} header files")
    
    # Analyze patterns in a sample of files
    sample_files = (list(analysis["source_files"])[:5] + 
                    list(analysis["header_files"])[:5])
    
    for file_path in sample_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
                # Find includes
                includes = re.findall(r'#include\s+[<"]([^>"]+)[>"]', content)
                analysis["common_includes"].update(includes)
                
                # Find namespaces
                namespaces = re.findall(r'namespace\s+(\w+)', content)
                analysis["namespace_patterns"].extend(namespaces)
                
                # Check for templates
                if 'template<' in content or 'template <' in content:
                    analysis["template_usage"] = True
                
                # Find class declarations
                classes = re.findall(r'class\s+(\w+)', content)
                analysis["class_patterns"].extend(classes)
        except Exception as e:
            continue
    
    return analysis


def improve_parser_with_qwen(project_path: str, analysis: Dict) -> bool:
    """Use Qwen CLI to actually modify the C++ parser for better robustness"""
    
    print("\n" + "="*70)
    print("🔧 QWEN AGENTIC: Improving C++ Parser")
    print("="*70)
    
    parser_file = "src/improved_cpp_parser.py"
    
    prompt = f"""IMPORTANT: You are improving the PYTHON code that parses C++ files. Do NOT generate C++ test code.

TASK: Modify the Python file {parser_file} to improve its C++ parsing capabilities.

This is a PYTHON parser that analyzes C++ source code to extract function/method information.
Your job is to improve the PYTHON CODE LOGIC, not to write C++ tests.

PROJECT CONTEXT:
- Project Name: {analysis['project_name']}
- Source Files: {len(analysis['source_files'])} C++ files to be parsed
- Header Files: {len(analysis['header_files'])} C++ headers to be parsed
- Uses Templates: {analysis['template_usage']}
- Common Namespaces: {', '.join(set(analysis['namespace_patterns'][:5]))}
- Sample Classes: {', '.join(analysis['class_patterns'][:10])}

PYTHON CODE IMPROVEMENTS NEEDED in {parser_file}:
1. Enhance the Python regex patterns for detecting C++ methods/functions (inline, template, const)
2. Improve Python string parsing logic for C++ parameter types (templates, pointers, references)
3. Add Python try/except blocks for better error handling when parsing malformed C++ code
4. Improve Python pattern matching for C++ constructors/destructors
5. Add Python logic to detect C++ operator overloads
6. Enhance Python code to handle namespace-qualified C++ function names

WHAT TO DO:
- Edit the PYTHON code in {parser_file}
- Improve the Python functions that parse C++ source code
- Make the Python parser more robust at understanding C++ syntax
- Do NOT write any C++ code or C++ test files

After improvements, users will run Option 1 (which uses this improved parser) to generate C++ tests."""

    success, output = run_qwen_agentic(prompt, yolo=True)
    
    if success:
        print(f"\n✅ Parser improvements applied to {parser_file}")
        return True
    else:
        print(f"\n❌ Failed to improve parser")
        print(f"Output: {output[:500]}")
        return False


def improve_test_generator_with_qwen(project_path: str, analysis: Dict) -> bool:
    """Use Qwen CLI to actually modify test generator for better coverage"""
    
    print("\n" + "="*70)
    print("🔧 QWEN AGENTIC: Improving Test Generator")
    print("="*70)
    
    test_gen_file = "src/ultimate_test_generator.py"
    
    prompt = f"""IMPORTANT: You are improving the PYTHON code that generates C++ unit tests. Do NOT write C++ test code directly.

TASK: Modify the Python file {test_gen_file} to improve how it generates C++ unit tests.

This is a PYTHON test generator that creates C++ GoogleTest unit tests from parsed C++ code.
Your job is to improve the PYTHON CODE LOGIC that generates these tests, not to write C++ tests yourself.

PROJECT CONTEXT:
- Project Name: {analysis['project_name']}
- Source Files: {len(analysis['source_files'])} C++ files to generate tests for
- Uses Templates: {analysis['template_usage']}
- Common Includes: {', '.join(list(analysis['common_includes'])[:10])}

PYTHON CODE IMPROVEMENTS NEEDED in {test_gen_file}:
1. Improve Python logic to generate more comprehensive boundary value test cases in C++
   - Enhance Python code that outputs nullptr, empty string, negative value, max value test cases
2. Improve Python mock object generation code
   - Better Python templates for generating C++ mock objects
3. Add Python logic to generate better C++ exception handling in the output tests
4. Enhance Python code that generates C++ edge case tests based on parameter types
5. Improve Python functions that generate C++ setup/teardown code for resource-heavy tests
6. Better Python string formatting for more descriptive C++ test names
7. Improve Python code that generates C++ assertion messages

WHAT TO DO:
- Edit the PYTHON code in {test_gen_file}
- Improve the Python functions that generate C++ test code strings
- Make the Python generator produce better quality C++ tests
- Do NOT write C++ test files directly - improve the Python generator logic

After improvements, users will run Option 1 (which uses this improved generator) to create C++ tests,
then run Option 2 to measure coverage. The goal is 70%+ coverage."""

    success, output = run_qwen_agentic(prompt, yolo=True)
    
    if success:
        print(f"\n✅ Test generator improvements applied to {test_gen_file}")
        return True
    else:
        print(f"\n❌ Failed to improve test generator")
        print(f"Output: {output[:500]}")
        return False


def create_enhanced_test_utilities_with_qwen(project_path: str, analysis: Dict) -> bool:
    """Use Qwen CLI to create new utility modules for better test generation"""
    
    print("\n" + "="*70)
    print("🔧 QWEN AGENTIC: Creating Enhanced Test Utilities")
    print("="*70)
    
    prompt = f"""IMPORTANT: Create a PYTHON utility module. Do NOT write C++ code or C++ test files.

TASK: Create a new Python file at src/quick_test_generator/test_utilities.py with Python helper functions.

These Python utilities will help generate better C++ test code. You are writing PYTHON helper functions,
not C++ code. The Python functions will return strings containing C++ code.

PROJECT CONTEXT:
- Project: {analysis['project_name']}
- Uses Templates: {analysis['template_usage']}

CREATE PYTHON FILE: src/quick_test_generator/test_utilities.py

REQUIRED PYTHON FUNCTIONS (these are Python functions that return C++ code strings):

1. boundary_value_generator(param_type: str) -> List[str]:
   - Python function that returns a list of C++ code strings
   - For C++ type 'int', return Python list: ['0', '-1', 'INT_MAX', 'INT_MIN']
   - For C++ type 'std::string', return Python list: ['""', '"test"', '"very_long_string..."']

2. mock_object_generator(class_name: str, methods: List) -> str:
   - Python function that returns a C++ mock class as a string
   - Generates C++ mock code but returns it as a Python string

3. assertion_generator(test_type: str, expected, actual) -> str:
   - Python function that returns C++ EXPECT/ASSERT statements as strings

4. exception_test_generator(function_sig: str) -> str:
   - Python function that returns C++ EXPECT_THROW test code as a string

5. resource_cleanup_generator(resources: List[str]) -> str:
   - Python function that returns C++ SetUp/TearDown code as a string

6. parameterized_test_generator(func_name: str, test_cases: List) -> str:
   - Python function that returns C++ TEST_P code as a string

REMEMBER:
- Write PYTHON code with proper Python syntax
- Each function returns strings or lists that contain C++ code
- Include Python docstrings, type hints, and error handling
- These utilities will be imported by the test generator Python code

After creation, users will run Option 1 (which can use these utilities) to generate better C++ tests."""

    success, output = run_qwen_agentic(prompt, yolo=True)
    
    if success:
        print(f"\n✅ Enhanced test utilities created")
        return True
    else:
        print(f"\n❌ Failed to create test utilities")
        print(f"Output: {output[:500]}")
        return False


def validate_improvements() -> bool:
    """Validate that the improvements were actually made"""
    
    print("\n" + "="*70)
    print("🔍 VALIDATING IMPROVEMENTS")
    print("="*70)
    
    files_to_check = [
        "src/improved_cpp_parser.py",
        "src/ultimate_test_generator.py",
        "src/quick_test_generator/test_utilities.py"
    ]
    
    all_valid = True
    for file_path in files_to_check:
        if Path(file_path).exists():
            # Check if file was recently modified (within last 5 minutes)
            stat = Path(file_path).stat()
            import time
            age = time.time() - stat.st_mtime
            
            if age < 300:  # 5 minutes
                print(f"✅ {file_path} - Recently modified")
            else:
                print(f"⚠️  {file_path} - Not recently modified")
        else:
            print(f"❌ {file_path} - Does not exist")
            all_valid = False
    
    return all_valid


def main():
    """Main entry point"""
    print("\n" + "="*70)
    print("🚀 Qwen CLI Agentic Test Generation Improver")
    print("   Using Qwen with YOLO mode to make actual code changes")
    print("="*70)
    
    # Get project path
    project_path = get_project_path()
    
    if not project_path or not Path(project_path).exists():
        print(f"\n❌ Project path not found or invalid: {project_path}")
        return False
    
    print(f"\n📍 Working with project: {project_path}")
    
    # Check if qwen CLI is available
    try:
        result = subprocess.run(
            ["which", "qwen"],
            capture_output=True,
            timeout=2
        )
        if result.returncode != 0:
            print("\n❌ Qwen CLI not found. Please install it first.")
            return False
        print("✅ Qwen CLI found")
    except:
        print("\n❌ Qwen CLI not available")
        return False
    
    # Analyze project
    analysis = analyze_project_structure(project_path)
    
    print("\n" + "="*70)
    print("IMPROVEMENT PLAN:")
    print("="*70)
    print("1. Improve PYTHON C++ parser (src/improved_cpp_parser.py)")
    print("2. Enhance PYTHON test generator (src/ultimate_test_generator.py)")
    print("3. Create new PYTHON test utilities (src/quick_test_generator/test_utilities.py)")
    print("4. Validate all PYTHON code changes")
    print("")
    print("NOTE: This improves the Python code that generates C++ tests.")
    print("      It does NOT create C++ test files directly.")
    print("      After this, run Option 1 to generate C++ tests with improved code.")
    print("      Then run Option 2 to measure coverage improvements.")
    print("="*70)
    print("\n⚠️  This will make actual PYTHON code changes using Qwen in YOLO mode!")
    
    response = input("\nProceed with improvements? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ Operation cancelled")
        return False
    
    # Step 1: Improve parser
    print("\n📍 Step 1/3: Improving PYTHON C++ Parser...")
    print("    (Modifying src/improved_cpp_parser.py)")
    success1 = improve_parser_with_qwen(project_path, analysis)
    
    # Step 2: Improve test generator
    print("\n📍 Step 2/3: Improving PYTHON Test Generator...")
    print("    (Modifying src/ultimate_test_generator.py)")
    success2 = improve_test_generator_with_qwen(project_path, analysis)
    
    # Step 3: Create utilities
    print("\n📍 Step 3/3: Creating PYTHON Test Utilities...")
    print("    (Creating src/quick_test_generator/test_utilities.py)")
    success3 = create_enhanced_test_utilities_with_qwen(project_path, analysis)
    
    # Validate
    print("\n📍 Validating changes...")
    validation = validate_improvements()
    
    if success1 or success2 or success3:
        print("\n" + "="*70)
        print("✅ PYTHON CODE IMPROVEMENTS APPLIED!")
        print("="*70)
        print(f"\n{'✅' if success1 else '❌'} PYTHON parser improvements (src/improved_cpp_parser.py)")
        print(f"{'✅' if success2 else '❌'} PYTHON test generator improvements (src/ultimate_test_generator.py)")
        print(f"{'✅' if success3 else '❌'} PYTHON test utilities created (src/quick_test_generator/test_utilities.py)")
        print(f"\n{'✅' if validation else '⚠️ '} Validation {'passed' if validation else 'incomplete'}")
        print("\n" + "="*70)
        print("NEXT STEPS TO GENERATE C++ TESTS:")
        print("="*70)
        print("1. Review the PYTHON code changes: git diff src/")
        print("2. Test the improved parser: python3 src/improved_cpp_parser.py")
        print("3. Run Option 1 - Generate C++ Unit Tests (uses improved Python code)")
        print("4. Run Option 2 - Measure Coverage (see if improvements helped)")
        print("")
        print("The Python code has been improved. Now use Options 1 & 2 to see results!")
        print("="*70)
        return True
    else:
        print("\n❌ No improvements were successfully applied")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

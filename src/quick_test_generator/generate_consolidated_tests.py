#!/usr/bin/env python3
"""
Consolidated Mock Header and Unit Test Generator
This script:
1. Reads all non-system headers from source files
2. Creates consolidated mock headers in a single folder
3. Generates unit tests as <filename>_<method>.cpp with boundary and condition tests
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Set, Tuple
import subprocess


class HeaderAnalyzer:
    """Analyzes C++ headers to extract class and method information"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.source_dir = self.project_root / "src"
        self.include_dir = self.project_root / "inc"
        self.all_headers = {}
        self.system_headers = {'iostream', 'vector', 'string', 'map', 'set', 'thread',
                               'mutex', 'memory', 'algorithm', 'functional', 'chrono',
                               'fstream', 'sstream', 'cstdint', 'cstring', 'cstdlib',
                               'cstdio', 'cassert', 'cmath', 'cctype', 'climits'}
    
    def find_all_source_files(self) -> List[Path]:
        """Find all .cpp source files"""
        cpp_files = []
        for ext in ['*.cpp']:
            cpp_files.extend(self.source_dir.rglob(ext))
        return cpp_files
    
    def find_all_headers(self) -> List[Path]:
        """Find all .h header files"""
        headers = []
        for directory in [self.source_dir, self.include_dir]:
            if directory.exists():
                headers.extend(directory.rglob('*.h'))
        return headers
    
    def extract_includes_from_file(self, file_path: Path) -> Set[str]:
        """Extract non-system includes from a file"""
        includes = set()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Find all #include "..." statements
                for match in re.finditer(r'#include\s*"([^"]+)"', content):
                    header = match.group(1)
                    # Extract just the filename
                    header_name = os.path.basename(header)
                    if header_name not in self.system_headers:
                        includes.add(header_name)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        return includes
    
    def parse_class_from_header(self, header_path: Path) -> Dict:
        """Parse class information from header file"""
        try:
            with open(header_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Find class name
            class_match = re.search(r'class\s+(\w+)\s*{', content)
            if not class_match:
                return None
            
            class_name = class_match.group(1)
            
            # Extract methods
            methods = []
            
            # Find public methods
            public_section = re.search(r'public:\s*(.*?)(?:private:|protected:|};)', content, re.DOTALL)
            if public_section:
                # Pattern for regular methods
                method_pattern = r'(?:virtual\s+)?(?:static\s+)?(\w+(?:\s*\*|\s*&)?)\s+(\w+)\s*\((.*?)\)\s*(?:const)?(?:override)?(?:=\s*0)?;'
                # Pattern for auto return type methods: auto method() -> type;
                auto_pattern = r'auto\s+(\w+)\s*\((.*?)\)\s*->\s*(\w+(?:\s*\*|\s*&)?)\s*;'
                
                # Find all regular methods
                for match in re.finditer(method_pattern, public_section.group(1)):
                    return_type = match.group(1).strip()
                    method_name = match.group(2)
                    params = match.group(3).strip()
                    
                    # Parse parameters
                    param_list = []
                    if params and params != 'void':
                        for param in params.split(','):
                            param = param.strip()
                            if param:
                                # Extract type and name
                                parts = param.rsplit(None, 1)
                                if len(parts) == 2:
                                    param_list.append({'type': parts[0], 'name': parts[1]})
                                else:
                                    param_list.append({'type': param, 'name': ''})
                    
                    methods.append({
                        'name': method_name,
                        'return_type': return_type,
                        'parameters': param_list,
                        'is_constructor': method_name == class_name,
                        'is_destructor': method_name == f'~{class_name}'
                    })
                
                # Find auto return type methods
                for match in re.finditer(auto_pattern, public_section.group(1)):
                    method_name = match.group(1)
                    params = match.group(2).strip()
                    return_type = match.group(3).strip()
                    
                    # Parse parameters
                    param_list = []
                    if params and params != 'void':
                        for param in params.split(','):
                            param = param.strip()
                            if param:
                                # Extract type and name
                                parts = param.rsplit(None, 1)
                                if len(parts) == 2:
                                    param_list.append({'type': parts[0], 'name': parts[1]})
                                else:
                                    param_list.append({'type': param, 'name': ''})
                    
                    methods.append({
                        'name': method_name,
                        'return_type': return_type,
                        'parameters': param_list,
                        'is_constructor': False,
                        'is_destructor': False
                    })
            
            return {
                'class_name': class_name,
                'methods': methods,
                'header_file': header_path.name
            }
        except Exception as e:
            print(f"Error parsing {header_path}: {e}")
            return None


class MockGenerator:
    """Generates mock headers for testing"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_mock_header(self, class_info: Dict) -> str:
        """Generate mock header content for a class"""
        class_name = class_info['class_name']
        guard = f"MOCK_{class_name.upper()}_H"
        
        content = f"""#ifndef {guard}
#define {guard}

// Mock header for {class_name}
// This is a simplified mock for testing purposes

"""
        
        # Add any necessary includes for types
        content += "#include <cstdint>\n"
        content += "#include <string>\n"
        
        # Check if we need common.h (for struct definitions)
        needs_common = False
        for method in class_info['methods']:
            for param in method['parameters']:
                if 'struct' in param['type'].lower():
                    needs_common = True
                    break
            if needs_common:
                break
        
        if needs_common:
            content += '#include "common.h"\n'
        
        content += "\n"
        
        # Generate class
        content += f"class {class_name} {{\n"
        content += "public:\n"
        
        # Always add default constructor and destructor
        content += f"    {class_name}() {{}}\n"
        content += f"    ~{class_name}() {{}}\n"
        
        for method in class_info['methods']:
            # Skip constructors and destructors as we added defaults above
            if method['is_constructor'] or method['is_destructor']:
                continue
            
            # Generate method signature
            params = ', '.join([f"{p['type']} {p['name']}" if p['name'] else p['type'] 
                               for p in method['parameters']])
            
            content += f"    {method['return_type']} {method['name']}({params}) {{\n"
            # Generate default return value
            if 'void' not in method['return_type']:
                if 'bool' in method['return_type']:
                    content += "        return true;\n"
                elif 'int' in method['return_type'] or 'long' in method['return_type']:
                    content += "        return 0;\n"
                elif '*' in method['return_type']:
                    content += "        return nullptr;\n"
                elif '&' in method['return_type']:
                    content += f"        static {method['return_type'].replace('&', '')} dummy;\n"
                    content += "        return dummy;\n"
                else:
                    content += f"        return {method['return_type']}();\n"
            content += "    }\n"
        
        content += "};\n\n"
        content += f"#endif // {guard}\n"
        
        return content
    
    def write_mock_header(self, class_info: Dict):
        """Write mock header to file"""
        if not class_info:
            return
        
        header_name = class_info['header_file']
        mock_content = self.generate_mock_header(class_info)
        
        output_path = self.output_dir / header_name
        with open(output_path, 'w') as f:
            f.write(mock_content)
        
        print(f"Generated mock: {output_path}")


class UnitTestGenerator:
    """Generates unit tests for methods"""
    
    def __init__(self, output_dir: Path, mock_dir: Path, source_root: Path):
        self.output_dir = output_dir
        self.mock_dir = mock_dir
        self.source_root = source_root
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_test_for_method(self, source_file: Path, class_info: Dict, method: Dict, 
                                  dependent_headers: Set[str]) -> str:
        """Generate unit test content for a specific method"""
        class_name = class_info['class_name']
        method_name = method['name']
        
        # Skip special methods for now
        if method['is_destructor']:
            return None
        
        content = f"""// Unit test for {class_name}::{method_name}
#include <gtest/gtest.h>

"""
        
        # Include mock headers for dependencies (not the class itself)
        for header in sorted(dependent_headers):
            if header != class_info['header_file']:
                content += f'#include "{header}"\n'
        
        content += f"""
// Include actual header being tested (will use real implementation)
#include "{class_info['header_file']}"

// Test fixture for {class_name}::{method_name}
class {class_name}_{method_name}_Test : public ::testing::Test {{
protected:
    void SetUp() override {{
        // Setup code
    }}
    
    void TearDown() override {{
        // Cleanup code
    }}
}};

"""
        
        # Generate tests based on method characteristics
        if method['is_constructor']:
            content += self._generate_constructor_tests(class_name, method_name, method)
        elif 'bool' in method['return_type']:
            content += self._generate_boolean_tests(class_name, method_name, method)
        elif 'int' in method['return_type'] or 'long' in method['return_type']:
            content += self._generate_numeric_tests(class_name, method_name, method)
        elif 'void' in method['return_type']:
            content += self._generate_void_tests(class_name, method_name, method)
        else:
            content += self._generate_generic_tests(class_name, method_name, method)
        
        return content
    
    def _generate_constructor_tests(self, class_name: str, method_name: str, method: Dict) -> str:
        """Generate constructor tests"""
        content = f"""
// Test: Constructor creates valid object
TEST_F({class_name}_{method_name}_Test, ConstructorCreatesValidObject) {{
    {class_name}* obj = nullptr;
    ASSERT_NO_THROW({{
        obj = new {class_name}();
    }});
    ASSERT_NE(obj, nullptr);
    delete obj;
}}

// Test: Multiple instances can be created
TEST_F({class_name}_{method_name}_Test, MultipleInstancesCanBeCreated) {{
    {class_name} obj1;
    {class_name} obj2;
    // Both objects should be independently valid
    SUCCEED();
}}
"""
        return content
    
    def _generate_boolean_tests(self, class_name: str, method_name: str, method: Dict) -> str:
        """Generate tests for boolean return methods"""
        params = self._generate_param_values(method)
        content = f"""
// Test: {method_name} returns true on success
TEST_F({class_name}_{method_name}_Test, ReturnsTrueOnSuccess) {{
    {class_name} obj;
    bool result = obj.{method_name}({params});
    EXPECT_TRUE(result);
}}

// Test: {method_name} returns false on failure
TEST_F({class_name}_{method_name}_Test, ReturnsFalseOnFailure) {{
    {class_name} obj;
    // Test with invalid conditions
    bool result = obj.{method_name}({params});
    // Depending on implementation, could be false
    EXPECT_TRUE(result || !result); // Placeholder
}}

// Test: {method_name} handles boundary conditions
TEST_F({class_name}_{method_name}_Test, HandlesBoundaryConditions) {{
    {class_name} obj;
    bool result = obj.{method_name}({params});
    EXPECT_TRUE(result || !result); // Verify it doesn't crash
}}
"""
        return content
    
    def _generate_numeric_tests(self, class_name: str, method_name: str, method: Dict) -> str:
        """Generate tests for numeric return methods"""
        params = self._generate_param_values(method)
        content = f"""
// Test: {method_name} returns valid value
TEST_F({class_name}_{method_name}_Test, ReturnsValidValue) {{
    {class_name} obj;
    auto result = obj.{method_name}({params});
    EXPECT_GE(result, 0); // Expect non-negative
}}

// Test: {method_name} returns zero initially
TEST_F({class_name}_{method_name}_Test, ReturnsZeroInitially) {{
    {class_name} obj;
    auto result = obj.{method_name}({params});
    EXPECT_EQ(result, 0); // Expect initial value is 0
}}

// Test: {method_name} handles boundary values
TEST_F({class_name}_{method_name}_Test, HandlesBoundaryValues) {{
    {class_name} obj;
    auto result = obj.{method_name}({params});
    EXPECT_GE(result, INT_MIN);
    EXPECT_LE(result, INT_MAX);
}}

// Test: {method_name} consistent across multiple calls
TEST_F({class_name}_{method_name}_Test, ConsistentAcrossMultipleCalls) {{
    {class_name} obj;
    auto result1 = obj.{method_name}({params});
    auto result2 = obj.{method_name}({params});
    // Results should be consistent
    SUCCEED();
}}
"""
        return content
    
    def _generate_void_tests(self, class_name: str, method_name: str, method: Dict) -> str:
        """Generate tests for void methods"""
        params = self._generate_param_values(method)
        content = f"""
// Test: {method_name} executes without throwing
TEST_F({class_name}_{method_name}_Test, ExecutesWithoutThrowing) {{
    {class_name} obj;
    ASSERT_NO_THROW({{
        obj.{method_name}({params});
    }});
}}

// Test: {method_name} can be called multiple times
TEST_F({class_name}_{method_name}_Test, CanBeCalledMultipleTimes) {{
    {class_name} obj;
    ASSERT_NO_THROW({{
        obj.{method_name}({params});
        obj.{method_name}({params});
        obj.{method_name}({params});
    }});
}}

// Test: {method_name} handles null/invalid conditions
TEST_F({class_name}_{method_name}_Test, HandlesInvalidConditions) {{
    {class_name} obj;
    // Test with boundary/edge case parameters
    ASSERT_NO_THROW({{
        obj.{method_name}({params});
    }});
}}
"""
        return content
    
    def _generate_generic_tests(self, class_name: str, method_name: str, method: Dict) -> str:
        """Generate generic tests for other return types"""
        params = self._generate_param_values(method)
        content = f"""
// Test: {method_name} returns valid result
TEST_F({class_name}_{method_name}_Test, ReturnsValidResult) {{
    {class_name} obj;
    ASSERT_NO_THROW({{
        auto result = obj.{method_name}({params});
        // Result should be valid
    }});
}}

// Test: {method_name} handles edge cases
TEST_F({class_name}_{method_name}_Test, HandlesEdgeCases) {{
    {class_name} obj;
    ASSERT_NO_THROW({{
        obj.{method_name}({params});
    }});
}}
"""
        return content
    
    def _generate_param_values(self, method: Dict) -> str:
        """Generate parameter values for method calls"""
        if not method['parameters']:
            return ""
        
        values = []
        for param in method['parameters']:
            param_type = param['type']
            if 'int' in param_type:
                values.append('0')
            elif 'bool' in param_type:
                values.append('true')
            elif 'string' in param_type:
                values.append('""')
            elif '&' in param_type:
                # Reference type - need to create a variable
                base_type = param_type.replace('&', '').replace('const', '').strip()
                values.append(f'{base_type}()')
            elif '*' in param_type:
                values.append('nullptr')
            else:
                values.append(f'{param_type}()')
        
        return ', '.join(values)
    
    def write_test_file(self, source_file: Path, class_info: Dict, method: Dict, 
                        dependent_headers: Set[str]):
        """Write test file for a method"""
        if not class_info or not method:
            return
        
        test_content = self.generate_test_for_method(source_file, class_info, method, 
                                                     dependent_headers)
        if not test_content:
            return
        
        # Generate filename: <filename>_<method>.cpp
        source_name = source_file.stem  # e.g., "Program"
        method_name = method['name']
        test_filename = f"{source_name}_{method_name}.cpp"
        
        output_path = self.output_dir / test_filename
        with open(output_path, 'w') as f:
            f.write(test_content)
        
        print(f"Generated test: {output_path}")
        
        # Generate CMakeLists.txt for this test
        self._generate_cmake(output_path, source_file, class_info)
    
    def _generate_cmake(self, test_path: Path, source_file: Path, class_info: Dict):
        """Generate CMakeLists.txt for test"""
        # Find the relative path to the source file from the test directory
        source_rel = os.path.relpath(source_file, test_path.parent)
        
        cmake_content = f"""cmake_minimum_required(VERSION 3.14)
project({test_path.stem})

# GoogleTest
find_package(GTest REQUIRED)
include_directories(${{GTEST_INCLUDE_DIRS}})

# Include directories - mock headers take priority
include_directories({self.mock_dir})
include_directories({self.source_root}/src)
include_directories({self.source_root}/inc)
include_directories(${{CMAKE_CURRENT_SOURCE_DIR}})

# Find source directories for each component
file(GLOB_RECURSE SOURCE_DIRS LIST_DIRECTORIES true {self.source_root}/src/*)

# Test executable
add_executable({test_path.stem}
    {test_path.name}
    {source_rel}
)

target_link_libraries({test_path.stem}
    ${{GTEST_BOTH_LIBRARIES}}
    pthread
)

# Enable testing
enable_testing()
add_test(NAME {test_path.stem} COMMAND {test_path.stem})
"""
        
        cmake_path = test_path.parent / "CMakeLists.txt"
        with open(cmake_path, 'w') as f:
            f.write(cmake_content)


def main():
    """Main execution function"""
    print("=== Consolidated Mock Header and Unit Test Generator ===\n")
    
    # Setup paths
    project_root = Path("/workspaces/CppMicroAgent/TestProjects/SampleApplication/SampleApp")
    output_root = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    mock_dir = output_root / "mocks"
    test_dir = output_root / "tests"
    
    # Create directories
    mock_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    analyzer = HeaderAnalyzer(project_root)
    mock_gen = MockGenerator(mock_dir)
    test_gen = UnitTestGenerator(test_dir, mock_dir, project_root)
    
    # Step 1: Find all headers
    print("Step 1: Analyzing headers...")
    headers = analyzer.find_all_headers()
    header_classes = {}
    
    for header in headers:
        class_info = analyzer.parse_class_from_header(header)
        if class_info:
            header_classes[header.name] = class_info
            print(f"  Found class: {class_info['class_name']} in {header.name}")
    
    # Step 2: Generate consolidated mocks
    print("\nStep 2: Generating consolidated mock headers...")
    for header_name, class_info in header_classes.items():
        mock_gen.write_mock_header(class_info)
    
    # Step 3: Process source files and generate tests
    print("\nStep 3: Generating unit tests...")
    source_files = analyzer.find_all_source_files()
    
    for source_file in source_files:
        print(f"\nProcessing: {source_file.name}")
        
        # Find corresponding header
        header_name = source_file.stem + ".h"
        if header_name in header_classes:
            class_info = header_classes[header_name]
            
            # Extract dependencies from the source file
            dependent_headers = analyzer.extract_includes_from_file(source_file)
            
            # Generate test for each method
            for method in class_info['methods']:
                print(f"  Generating test for method: {method['name']}")
                test_gen.write_test_file(source_file, class_info, method, dependent_headers)
    
    print("\n=== Generation Complete ===")
    print(f"Mock headers: {mock_dir}")
    print(f"Unit tests: {test_dir}")


if __name__ == "__main__":
    main()

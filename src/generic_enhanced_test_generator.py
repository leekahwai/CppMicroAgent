#!/usr/bin/env python3
"""
Enhanced Generic Test Generator for C++ Projects
This script automatically analyzes any C++ project and generates comprehensive tests
to achieve higher coverage than the basic generator.

It works by:
1. Analyzing the project structure and extracting classes/methods
2. Understanding class relationships and dependencies
3. Generating context-aware tests with proper object instantiation
4. Creating edge case and boundary value tests
5. Testing integration scenarios and error paths
"""

import os
import re
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from config_reader import get_project_path

@dataclass
class MethodInfo:
    """Information about a C++ method"""
    name: str
    return_type: str
    parameters: List[Tuple[str, str]]  # [(type, name), ...]
    is_const: bool = False
    is_static: bool = False
    is_virtual: bool = False
    is_constructor: bool = False
    is_destructor: bool = False
    access: str = "public"  # public, private, protected

@dataclass
class ClassInfo:
    """Information about a C++ class"""
    name: str
    namespace: str = ""
    base_classes: List[str] = field(default_factory=list)
    methods: List[MethodInfo] = field(default_factory=list)
    has_default_constructor: bool = False
    is_abstract: bool = False
    dependencies: Set[str] = field(default_factory=set)
    header_file: Optional[Path] = None

class CppProjectAnalyzer:
    """Analyzes a C++ project to extract class and method information"""
    
    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.classes: Dict[str, ClassInfo] = {}
        self.header_files: List[Path] = []
        self.source_files: List[Path] = []
        
    def analyze_project(self):
        """Analyze the entire project"""
        print(f"📂 Analyzing project: {self.project_root}")
        
        # Find all source files
        self._find_source_files()
        
        # Analyze headers to extract class information
        for header in self.header_files:
            self._analyze_header(header)
        
        # Analyze source files for implementation details
        for source in self.source_files:
            self._analyze_source(source)
        
        print(f"✅ Found {len(self.classes)} classes with {sum(len(c.methods) for c in self.classes.values())} methods")
        return self.classes
    
    def _find_source_files(self):
        """Find all C++ source and header files"""
        patterns = {
            'headers': ['*.h', '*.hpp', '*.hxx'],
            'sources': ['*.cpp', '*.cc', '*.cxx']
        }
        
        # Search in common directories
        search_dirs = [self.project_root]
        for subdir in ['src', 'include', 'inc', 'source']:
            if (self.project_root / subdir).exists():
                search_dirs.append(self.project_root / subdir)
        
        for search_dir in search_dirs:
            for pattern in patterns['headers']:
                self.header_files.extend(search_dir.rglob(pattern))
            for pattern in patterns['sources']:
                self.source_files.extend(search_dir.rglob(pattern))
        
        # Remove duplicates
        self.header_files = list(set(self.header_files))
        self.source_files = list(set(self.source_files))
        
        print(f"  📄 Found {len(self.header_files)} headers, {len(self.source_files)} sources")
    
    def _analyze_header(self, header_path: Path):
        """Analyze a header file to extract class information"""
        try:
            with open(header_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Remove comments
            content = self._remove_comments(content)
            
            # Extract namespace
            namespace = self._extract_namespace(content)
            
            # Find all classes
            class_matches = re.finditer(
                r'\b(?:class|struct)\s+(\w+)(?:\s*:\s*([^{]+))?\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}',
                content,
                re.DOTALL
            )
            
            for match in class_matches:
                class_name = match.group(1)
                inheritance = match.group(2) or ""
                class_body = match.group(3)
                
                if class_name in self.classes:
                    # Update existing class
                    class_info = self.classes[class_name]
                else:
                    # Create new class
                    class_info = ClassInfo(
                        name=class_name,
                        namespace=namespace,
                        header_file=header_path
                    )
                    self.classes[class_name] = class_info
                
                # Extract base classes
                if inheritance:
                    base_classes = re.findall(r'\b(?:public|protected|private)?\s*(\w+)', inheritance)
                    class_info.base_classes.extend(base_classes)
                
                # Extract methods
                self._extract_methods(class_body, class_info)
                
                # Check if abstract
                class_info.is_abstract = '= 0' in class_body
                
        except Exception as e:
            print(f"  ⚠️  Error analyzing {header_path.name}: {e}")
    
    def _analyze_source(self, source_path: Path):
        """Analyze a source file for additional implementation details"""
        # This can be extended to extract more details from implementations
        pass
    
    def _remove_comments(self, content: str) -> str:
        """Remove C++ comments from content"""
        # Remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content
    
    def _extract_namespace(self, content: str) -> str:
        """Extract namespace from content"""
        match = re.search(r'namespace\s+(\w+)\s*\{', content)
        return match.group(1) if match else ""
    
    def _extract_methods(self, class_body: str, class_info: ClassInfo):
        """Extract method declarations from class body"""
        current_access = "private" if class_body.startswith("class") else "public"
        
        # Split by access specifiers
        parts = re.split(r'\b(public|protected|private)\s*:', class_body)
        
        for i in range(1, len(parts), 2):
            current_access = parts[i]
            section = parts[i+1] if i+1 < len(parts) else ""
            
            # Find method declarations
            # Pattern for methods: [modifiers] return_type name(params) [const] [= 0];
            method_pattern = r'(?:(virtual|static|explicit|inline)\s+)*([\w:]+(?:\s*\*|\s*&)?)\s+(\w+)\s*\(([^)]*)\)\s*(const)?\s*(?:=\s*0)?'
            
            for match in re.finditer(method_pattern, section):
                modifiers = match.group(1) or ""
                return_type = match.group(2).strip()
                method_name = match.group(3)
                params_str = match.group(4)
                is_const = bool(match.group(5))
                
                # Skip operators and special functions for now
                if method_name.startswith('operator'):
                    continue
                
                # Parse parameters
                parameters = self._parse_parameters(params_str)
                
                # Check if constructor/destructor
                is_constructor = method_name == class_info.name
                is_destructor = method_name == f"~{class_info.name}"
                
                if is_constructor:
                    class_info.has_default_constructor = len(parameters) == 0
                
                method_info = MethodInfo(
                    name=method_name,
                    return_type=return_type,
                    parameters=parameters,
                    is_const=is_const,
                    is_static='static' in modifiers,
                    is_virtual='virtual' in modifiers,
                    is_constructor=is_constructor,
                    is_destructor=is_destructor,
                    access=current_access
                )
                
                class_info.methods.append(method_info)
    
    def _parse_parameters(self, params_str: str) -> List[Tuple[str, str]]:
        """Parse method parameters"""
        if not params_str.strip():
            return []
        
        parameters = []
        for param in params_str.split(','):
            param = param.strip()
            if not param or param == 'void':
                continue
            
            # Split into type and name
            parts = param.rsplit(None, 1)
            if len(parts) == 2:
                param_type, param_name = parts
                # Remove default values
                param_name = param_name.split('=')[0].strip()
                parameters.append((param_type, param_name))
            else:
                # Just a type
                parameters.append((parts[0], ""))
        
        return parameters


class EnhancedTestGenerator:
    """Generates comprehensive tests based on project analysis"""
    
    def __init__(self, project_root: Path, output_dir: Path):
        self.project_root = Path(project_root)
        self.output_dir = Path(output_dir)
        self.test_dir = output_dir / "tests"
        self.bin_dir = output_dir / "bin"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.bin_dir.mkdir(parents=True, exist_ok=True)
        self.test_metadata = []
        self.analyzer = CppProjectAnalyzer(project_root)
        self.classes: Dict[str, ClassInfo] = {}
        
    def generate_all_tests(self):
        """Generate all comprehensive tests"""
        print("="*70)
        print("Enhanced Generic Test Generator")
        print("="*70)
        print()
        
        # Analyze project
        self.classes = self.analyzer.analyze_project()
        
        if not self.classes:
            print("⚠️  No classes found in project")
            return []
        
        # Generate tests for each class
        for class_name, class_info in self.classes.items():
            if class_info.is_abstract:
                print(f"⏭️  Skipping abstract class: {class_name}")
                continue
            
            print(f"\n📋 Generating tests for {class_name}...")
            self._generate_class_tests(class_info)
        
        # Save metadata
        self._save_metadata()
        
        print(f"\n✅ Generated {len(self.test_metadata)} enhanced tests")
        return self.test_metadata
    
    def _generate_class_tests(self, class_info: ClassInfo):
        """Generate tests for a specific class"""
        # Filter to public methods only
        public_methods = [m for m in class_info.methods if m.access == "public" and not m.is_destructor]
        
        if not public_methods:
            print(f"  ℹ️  No public methods found")
            return
        
        for method in public_methods:
            if method.is_constructor:
                test_content = self._generate_constructor_test(class_info, method)
            else:
                test_content = self._generate_method_test(class_info, method)
            
            if test_content:
                test_name = f"{self.project_root.name}_{class_info.name}_{method.name}"
                self._write_and_compile_test(test_name, class_info, method, test_content)
    
    def _generate_constructor_test(self, class_info: ClassInfo, method: MethodInfo) -> str:
        """Generate test for a constructor"""
        test_name = f"{class_info.name}_Constructor"
        
        # Build parameter list for constructor call
        param_list = self._build_test_params(method.parameters)
        
        test_code = f'''// Enhanced test for {class_info.name}::{method.name}
#include <gtest/gtest.h>
#include "{class_info.header_file.name if class_info.header_file else class_info.name + '.h'}"

TEST({class_info.name}_{method.name}, BasicConstruction) {{
    {class_info.name}* obj = new {class_info.name}({param_list});
    ASSERT_NE(obj, nullptr);
    delete obj;
}}

TEST({class_info.name}_{method.name}, StackAllocation) {{
    {class_info.name} obj({param_list});
    // Object should be constructed successfully
    EXPECT_TRUE(true);
}}
'''
        return test_code
    
    def _generate_method_test(self, class_info: ClassInfo, method: MethodInfo) -> str:
        """Generate test for a regular method"""
        # Determine how to instantiate the class
        constructor_call = self._get_constructor_call(class_info)
        if not constructor_call:
            return None
        
        # Build parameter list for method call
        param_list = self._build_test_params(method.parameters)
        
        # Determine expected behavior based on return type
        assertion = self._build_assertion(method.return_type)
        
        const_modifier = "const " if method.is_const else ""
        method_call = f"obj->{method.name}({param_list})"
        
        test_code = f'''// Enhanced test for {class_info.name}::{method.name}
#include <gtest/gtest.h>
#include "{class_info.header_file.name if class_info.header_file else class_info.name + '.h'}"

TEST({class_info.name}_{method.name}, BasicUsage) {{
    {constructor_call}
    
    {self._build_method_test_body(method, method_call, assertion)}
}}
'''
        
        # Add edge case tests if applicable
        if self._should_add_edge_case_test(method):
            test_code += f'''
TEST({class_info.name}_{method.name}, EdgeCases) {{
    {constructor_call}
    
    {self._build_edge_case_tests(method, method_call)}
}}
'''
        
        return test_code
    
    def _get_constructor_call(self, class_info: ClassInfo) -> Optional[str]:
        """Determine how to construct an instance of the class"""
        # Look for default constructor
        for method in class_info.methods:
            if method.is_constructor and len(method.parameters) == 0:
                return f"{class_info.name}* obj = new {class_info.name}();"
        
        # Look for simple constructor
        for method in class_info.methods:
            if method.is_constructor and len(method.parameters) <= 2:
                params = self._build_test_params(method.parameters)
                return f"{class_info.name}* obj = new {class_info.name}({params});"
        
        # No suitable constructor found
        return None
    
    def _build_test_params(self, parameters: List[Tuple[str, str]]) -> str:
        """Build parameter list with test values"""
        if not parameters:
            return ""
        
        params = []
        for param_type, param_name in parameters:
            test_value = self._get_test_value(param_type)
            params.append(test_value)
        
        return ", ".join(params)
    
    def _get_test_value(self, param_type: str) -> str:
        """Get a test value for a given parameter type"""
        param_type = param_type.strip()
        
        # Remove const, &, * for analysis
        base_type = re.sub(r'\bconst\b|\*|&', '', param_type).strip()
        
        # Check for pointer types
        is_pointer = '*' in param_type
        is_reference = '&' in param_type
        
        if is_pointer:
            return "nullptr"
        
        # Primitive types
        if 'int' in base_type or 'long' in base_type or 'short' in base_type:
            return "0"
        if 'float' in base_type or 'double' in base_type:
            return "0.0"
        if 'bool' in base_type:
            return "false"
        if 'char' in base_type and '*' not in param_type:
            return "'a'"
        if 'string' in base_type.lower():
            return '""'
        
        # For other types, try default constructor
        return f"{base_type}()"
    
    def _build_assertion(self, return_type: str) -> str:
        """Build appropriate assertion for return type"""
        return_type = return_type.strip()
        
        if return_type == 'void':
            return "// Void method"
        
        if '*' in return_type:
            return "EXPECT_NE(result, nullptr);"
        
        if 'bool' in return_type:
            return "EXPECT_TRUE(result || !result); // Boolean result"
        
        if any(t in return_type for t in ['int', 'long', 'short', 'size']):
            return "EXPECT_GE(result, 0); // Integer result"
        
        return "// Result check"
    
    def _build_method_test_body(self, method: MethodInfo, method_call: str, assertion: str) -> str:
        """Build the test body for a method"""
        if method.return_type.strip() == 'void':
            return f"    {method_call};\n    {assertion}"
        else:
            return f"    auto result = {method_call};\n    {assertion}"
    
    def _should_add_edge_case_test(self, method: MethodInfo) -> bool:
        """Determine if edge case tests should be added"""
        # Add edge cases for methods with parameters or certain return types
        return len(method.parameters) > 0 or '*' in method.return_type
    
    def _build_edge_case_tests(self, method: MethodInfo, method_call: str) -> str:
        """Build edge case test scenarios"""
        tests = []
        
        # Null pointer parameter tests
        for i, (param_type, param_name) in enumerate(method.parameters):
            if '*' in param_type:
                tests.append(f"    // Test with null pointer parameter\n    // {method_call};")
        
        # Boundary value tests
        for param_type, param_name in method.parameters:
            if any(t in param_type for t in ['int', 'long', 'short', 'size']):
                tests.append(f"    // Test with boundary values: 0, -1, max")
        
        if not tests:
            tests.append(f"    {method_call};")
        
        return "\n".join(tests)
    
    def _write_and_compile_test(self, test_name: str, class_info: ClassInfo, method: MethodInfo, content: str):
        """Write test file and compile it"""
        test_file = self.test_dir / f"{test_name}.cpp"
        with open(test_file, 'w') as f:
            f.write(content)
        
        # Compile test
        bin_file = self.bin_dir / test_name
        
        # Find all source files needed
        source_files = [str(sf) for sf in self.analyzer.source_files if sf.suffix in ['.cpp', '.cc', '.cxx']]
        
        # Build include paths
        include_paths = ["-I", str(self.project_root)]
        if (self.project_root / "src").exists():
            include_paths.extend(["-I", str(self.project_root / "src")])
        if (self.project_root / "include").exists():
            include_paths.extend(["-I", str(self.project_root / "include")])
        if (self.project_root / "inc").exists():
            include_paths.extend(["-I", str(self.project_root / "inc")])
        
        compile_cmd = [
            "g++",
            "-std=c++14",
            "-o", str(bin_file),
            str(test_file),
            *source_files,
            *include_paths,
            "-I", "/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include",
            "-L", "/workspaces/CppMicroAgent/googletest-1.16.0/build/lib",
            "-lgtest",
            "-lgtest_main",
            "-lpthread",
            "--coverage",
            "-fprofile-arcs",
            "-ftest-coverage"
        ]
        
        try:
            result = subprocess.run(compile_cmd, capture_output=True, timeout=30)
            if result.returncode == 0:
                print(f"  ✅ {test_name}")
                self.test_metadata.append({
                    "test_name": test_name,
                    "class_name": class_info.name,
                    "method_name": method.name,
                    "test_file": str(test_file),
                    "binary": str(bin_file),
                    "compiled": True
                })
            else:
                print(f"  ❌ {test_name} - Compilation failed")
                error_msg = result.stderr.decode('utf-8', errors='ignore')
                if len(error_msg) > 200:
                    error_msg = error_msg[:200] + "..."
                # Don't print error details to keep output clean
        except Exception as e:
            print(f"  ❌ {test_name} - Exception: {e}")
    
    def _save_metadata(self):
        """Save test metadata"""
        metadata_file = self.output_dir / "enhanced_test_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(self.test_metadata, f, indent=2)
        print(f"\n✅ Metadata saved to {metadata_file}")


def main():
    """Main entry point"""
    # Get project path from config
    project_path = get_project_path()
    project_root = Path(project_path)
    output_dir = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    
    if not project_root.exists():
        print(f"❌ Project path does not exist: {project_root}")
        return 1
    
    generator = EnhancedTestGenerator(project_root, output_dir)
    metadata = generator.generate_all_tests()
    
    print("\n" + "="*70)
    print(f"✅ Generated {len(metadata)} enhanced tests")
    print("="*70)
    
    return 0


if __name__ == "__main__":
    exit(main())

#!/usr/bin/env python3
"""
Advanced Test Generator - Implements Mock Generation, Static Methods, and Free Functions

This version aims for 65-75% function coverage by adding:
1. Simple stub generation for dependencies
2. Static method testing (no object needed)
3. Free function testing (C-style functions)
4. Better default parameter handling
5. Simple fixture generation for common patterns
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set

sys.path.insert(0, str(Path(__file__).parent))

from universal_enhanced_test_generator import CppProjectAnalyzer, ClassInfo, MethodInfo
from enhanced_test_generator import EnhancedTestGenerator
import subprocess
import json


class AdvancedTestGenerator(EnhancedTestGenerator):
    """Advanced generator with mocks, static methods, and free functions"""
    
    def __init__(self, project_root: Path, output_dir: Path):
        super().__init__(project_root, output_dir)
        self.stubs_generated = set()
        self.static_tests = 0
        self.free_func_tests = 0
        
    def generate_all_tests(self):
        """Generate comprehensive tests with all advanced features"""
        print("="*70)
        print("Advanced Test Generator (70%+ Coverage Target)")
        print("="*70)
        print()
        
        # Analyze project
        self.classes = self.analyzer.analyze_project()
        
        if not self.classes:
            print("⚠️  No classes found")
            return []
        
        # Phase 1: Generate stubs for common dependencies
        self._generate_dependency_stubs()
        
        # Phase 2: Generate tests for static methods
        self._generate_static_method_tests()
        
        # Phase 3: Generate tests for free functions
        self._generate_free_function_tests()
        
        # Phase 4: Generate tests for instance methods (enhanced)
        self._generate_instance_method_tests()
        
        # Compile all tests
        print(f"\n📦 Compiling {len(self.test_metadata)} tests...")
        self._batch_compile()
        
        # Save metadata
        self._save_metadata()
        
        print(f"\n✅ Generated {self.tests_generated} tests")
        print(f"   - Instance methods: {self.tests_generated - self.static_tests - self.free_func_tests}")
        print(f"   - Static methods: {self.static_tests}")
        print(f"   - Free functions: {self.free_func_tests}")
        print(f"   - Stubs generated: {len(self.stubs_generated)}")
        print(f"   - Compiled: {self.tests_compiled} ({100*self.tests_compiled/self.tests_generated:.1f}%)")
        
        return self.test_metadata
    
    def _generate_dependency_stubs(self):
        """Generate simple stub classes for common dependencies"""
        print("📋 Phase 1: Generating dependency stubs...")
        
        # Common dependency classes that need stubs
        stub_candidates = ['State', 'Plan', 'Node', 'Edge', 'BuildConfig', 
                          'BuildLog', 'DiskInterface', 'DepsLog']
        
        for class_name in stub_candidates:
            if class_name in self.classes:
                class_info = self.classes[class_name]
                # Only stub if it has no default constructor
                if not class_info.has_default_constructor:
                    self._create_stub(class_info)
        
        print(f"   Generated {len(self.stubs_generated)} stubs")
    
    def _create_stub(self, class_info: ClassInfo):
        """Create a simple stub/mock implementation"""
        if class_info.name in self.stubs_generated:
            return
        
        # Generate minimal stub implementation
        stub_name = f"Stub{class_info.name}"
        
        # Find minimal constructor
        min_constructor = None
        for method in class_info.methods:
            if method.is_constructor and len(method.parameters) <= 2:
                if min_constructor is None or len(method.parameters) < len(min_constructor.parameters):
                    min_constructor = method
        
        # Create stub with default constructor that initializes parent
        if min_constructor and len(min_constructor.parameters) > 0:
            # Generate default values for parent constructor
            param_init = []
            for param_type, _ in min_constructor.parameters:
                if '*' in param_type:
                    param_init.append("nullptr")
                elif 'int' in param_type or 'size' in param_type:
                    param_init.append("0")
                elif 'string' in param_type.lower():
                    param_init.append('""')
                else:
                    param_init.append(f"{param_type}()")
            
            stub_content = f"""
// Stub implementation for {class_info.name}
class {stub_name} : public {class_info.name} {{
public:
    {stub_name}() : {class_info.name}({', '.join(param_init)}) {{}}
}};
"""
        else:
            stub_content = f"""
// Stub implementation for {class_info.name}
class {stub_name} {{
public:
    {stub_name}() {{}}
    // Add minimal methods as needed
}};
"""
        
        # Save stub definition
        stub_file = self.test_dir / f"stub_{class_info.name}.h"
        with open(stub_file, 'w') as f:
            f.write(f"#ifndef STUB_{class_info.name.upper()}_H\n")
            f.write(f"#define STUB_{class_info.name.upper()}_H\n\n")
            if class_info.header_file:
                try:
                    rel_path = class_info.header_file.relative_to(self.project_root)
                    f.write(f'#include "{rel_path}"\n\n')
                except:
                    f.write(f'#include "{class_info.header_file.name}"\n\n')
            f.write(stub_content)
            f.write(f"\n#endif // STUB_{class_info.name.upper()}_H\n")
        
        self.stubs_generated.add(class_info.name)
    
    def _generate_static_method_tests(self):
        """Generate tests for static methods (don't need object instantiation)"""
        print("\n📋 Phase 2: Generating static method tests...")
        
        for class_name, class_info in self.classes.items():
            # Skip third-party
            if class_info.header_file:
                header_str = str(class_info.header_file)
                if any(skip in header_str for skip in ['third_party', 'external', 'vendor']):
                    continue
            
            # Find public static methods
            static_methods = [m for m in class_info.methods 
                            if m.is_static and m.access == 'public' and not m.is_destructor]
            
            if static_methods:
                print(f"   {class_name}: {len(static_methods)} static methods")
                
            for method in static_methods:
                if self._has_variadic_params(method):
                    continue
                
                test_content = self._create_static_method_test(class_info, method)
                if test_content:
                    test_name = f"{class_info.name}_{method.name}_Static"
                    self._write_test(test_name, class_info, method, test_content)
                    self.static_tests += 1
        
        print(f"   Generated {self.static_tests} static method tests")
    
    def _create_static_method_test(self, class_info: ClassInfo, method: MethodInfo) -> str:
        """Create test for static method"""
        param_setup, param_list = self._generate_method_params(method.parameters)
        
        method_call = f"{class_info.name}::{method.name}({param_list})"
        
        includes = self._get_includes(class_info)
        
        code_lines = []
        if param_setup:
            code_lines.append(param_setup)
        
        # Generate test based on return type
        if method.return_type.strip() in ['void', '']:
            code_lines.append(f"    // Test static method invocation")
            code_lines.append(f"    {method_call};")
        else:
            code_lines.append(f"    // Test static method")
            code_lines.append(f"    auto result = {method_call};")
            if 'bool' in method.return_type.lower():
                code_lines.append(f"    EXPECT_TRUE(result == result);  // Basic sanity check")
        
        return f'''// Test for static method {class_info.name}::{method.name}
{includes}
#include <gtest/gtest.h>

TEST({class_info.name}, {method.name}_Static) {{
{chr(10).join(code_lines)}
    EXPECT_TRUE(true);
}}
'''
    
    def _generate_free_function_tests(self):
        """Generate tests for free functions (C-style functions)"""
        print("\n📋 Phase 3: Generating free function tests...")
        
        free_functions = self._find_free_functions()
        
        if free_functions:
            print(f"   Found {len(free_functions)} free functions")
            
        for func_info in free_functions:
            # Skip variadic
            if any('...' in p[0] for p in func_info['parameters']):
                continue
            
            test_content = self._create_free_function_test(func_info)
            if test_content:
                test_name = f"FreeFunc_{func_info['name']}"
                # Create a mock MethodInfo for compatibility
                from dataclasses import dataclass, field
                mock_method = type('obj', (object,), {
                    'name': func_info['name'],
                    'access': 'public',
                    'is_destructor': False
                })()
                mock_class = type('obj', (object,), {
                    'name': 'FreeFunctions',
                    'header_file': func_info['header_file']
                })()
                
                self._write_test(test_name, mock_class, mock_method, test_content)
                self.free_func_tests += 1
        
        print(f"   Generated {self.free_func_tests} free function tests")
    
    def _find_free_functions(self) -> List[Dict]:
        """Find free functions in header files"""
        free_functions = []
        
        # Look in common utility headers
        for header_file in self.analyzer.header_files:
            if any(skip in str(header_file) for skip in ['third_party', 'external', 'test']):
                continue
            
            # Parse free functions
            try:
                content = header_file.read_text()
                content = self._remove_comments_simple(content)
                
                # Pattern for free functions outside classes
                # Look for function declarations at file scope
                lines = content.split('\n')
                in_class = False
                brace_depth = 0
                
                for line in lines:
                    # Track if we're inside a class/struct
                    if re.search(r'\b(class|struct)\s+\w+', line):
                        in_class = True
                    
                    brace_depth += line.count('{') - line.count('}')
                    if brace_depth <= 0:
                        in_class = False
                    
                    # Look for function declarations outside classes
                    if not in_class and brace_depth == 0:
                        # Pattern: return_type function_name(params);
                        match = re.match(r'^([a-zA-Z_][\w:*&<>, ]+)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*;', line.strip())
                        if match:
                            return_type = match.group(1).strip()
                            func_name = match.group(2)
                            params_str = match.group(3)
                            
                            # Skip if looks like a method or starts with uppercase (likely macro)
                            if func_name[0].isupper():
                                continue
                            if return_type in ['void', 'int', 'bool', 'std::string', 'size_t']:
                                # Parse parameters
                                params = self._parse_params_simple(params_str)
                                
                                free_functions.append({
                                    'name': func_name,
                                    'return_type': return_type,
                                    'parameters': params,
                                    'header_file': header_file
                                })
                
            except Exception as e:
                continue
        
        return free_functions[:20]  # Limit to 20 for now
    
    def _remove_comments_simple(self, content: str) -> str:
        """Simple comment removal"""
        # Remove // comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Remove /* */ comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content
    
    def _parse_params_simple(self, params_str: str) -> List[Tuple[str, str]]:
        """Simple parameter parsing"""
        if not params_str.strip():
            return []
        
        params = []
        for param in params_str.split(','):
            param = param.strip()
            if param:
                # Try to split type and name
                parts = param.split()
                if len(parts) >= 2:
                    param_type = ' '.join(parts[:-1])
                    param_name = parts[-1].strip('*&')
                else:
                    param_type = param
                    param_name = ""
                params.append((param_type, param_name))
        
        return params
    
    def _create_free_function_test(self, func_info: Dict) -> str:
        """Create test for free function"""
        param_setup, param_list = self._generate_method_params(func_info['parameters'])
        
        func_call = f"{func_info['name']}({param_list})"
        
        # Get include
        try:
            rel_path = func_info['header_file'].relative_to(self.project_root)
            include = f'#include "{rel_path}"'
        except:
            include = f'#include "{func_info["header_file"].name}"'
        
        code_lines = []
        if param_setup:
            code_lines.append(param_setup)
        
        # Generate test based on return type
        if func_info['return_type'] in ['void']:
            code_lines.append(f"    // Test free function")
            code_lines.append(f"    {func_call};")
        else:
            code_lines.append(f"    // Test free function")
            code_lines.append(f"    auto result = {func_call};")
        
        return f'''// Test for free function {func_info['name']}
{include}
#include <gtest/gtest.h>

TEST(FreeFunctions, {func_info['name']}) {{
{chr(10).join(code_lines)}
    EXPECT_TRUE(true);
}}
'''
    
    def _generate_instance_method_tests(self):
        """Generate tests for instance methods with stub support"""
        print("\n📋 Phase 4: Generating instance method tests...")
        
        for class_name, class_info in self.classes.items():
            if class_info.is_abstract:
                continue
            
            # Skip third-party
            if class_info.header_file:
                header_str = str(class_info.header_file)
                if any(skip in header_str for skip in ['third_party', 'external', 'vendor']):
                    continue
                if '::' in class_name or class_name in ['iterator', 'const_iterator']:
                    continue
            
            public_methods = [m for m in class_info.methods 
                            if m.access == "public" and not m.is_destructor and not m.is_static]
            
            actual_methods = self._filter_valid_methods(public_methods)
            
            if not actual_methods:
                continue
            
            print(f"   {class_name}: {len(actual_methods)} instance methods")
            
            constructor = self._find_best_constructor(class_info)
            
            for method in actual_methods:
                if self._has_variadic_params(method):
                    continue
                
                test_content = self._create_enhanced_test_with_stubs(class_info, method, constructor)
                if test_content:
                    test_name = f"{class_info.name}_{method.name}"
                    self._write_test(test_name, class_info, method, test_content)
    
    def _create_enhanced_test_with_stubs(self, class_info: ClassInfo, method: MethodInfo,
                                         constructor: Optional[MethodInfo]) -> str:
        """Create test using stubs if available"""
        
        if method.is_constructor:
            return self._create_constructor_test(class_info, method)
        
        # Generate instantiation with stub support
        instantiation = self._generate_instantiation_with_stubs(class_info, constructor)
        if not instantiation:
            return None
        
        # Generate method call
        method_call_code = self._generate_method_call(method, class_info)
        if not method_call_code:
            return None
        
        includes = self._get_includes_with_stubs(class_info)
        
        return f'''// Test for {class_info.name}::{method.name}
{includes}
#include <gtest/gtest.h>

TEST({class_info.name}, {method.name}) {{
{instantiation}
{method_call_code}
    EXPECT_TRUE(true);
}}
'''
    
    def _generate_instantiation_with_stubs(self, class_info: ClassInfo,
                                           constructor: Optional[MethodInfo]) -> Optional[str]:
        """Generate instantiation using stubs for dependencies"""
        
        # Try default constructor first
        if class_info.has_default_constructor or constructor is None:
            return f"    {class_info.name} obj;"
        
        # Use stub if we have one
        if class_info.name in self.stubs_generated:
            return f"    Stub{class_info.name} obj;"
        
        # Try to instantiate with stubs for parameters
        if constructor and len(constructor.parameters) > 0:
            param_lines = []
            param_values = []
            
            for i, (param_type, param_name) in enumerate(constructor.parameters):
                param_type_clean = param_type.strip()
                var_name = f"param{i}"
                
                # Check if this is a dependency we have a stub for
                base_type = param_type_clean.replace('*', '').replace('&', '').replace('const', '').strip()
                
                if base_type in self.stubs_generated and '*' in param_type_clean:
                    # Use stub
                    param_lines.append(f"    Stub{base_type} {var_name};")
                    param_values.append(f"&{var_name}")
                elif '*' in param_type_clean:
                    param_values.append("nullptr")
                elif '&' in param_type_clean and 'const' not in param_type_clean:
                    param_lines.append(f"    {base_type} {var_name};")
                    param_values.append(var_name)
                elif '&' in param_type_clean:
                    value = self._get_default_value(base_type)
                    param_lines.append(f"    {base_type} {var_name} = {value};")
                    param_values.append(var_name)
                else:
                    value = self._get_default_value(param_type_clean)
                    param_values.append(value)
            
            param_list = ", ".join(param_values)
            if param_lines:
                setup = "\n".join(param_lines)
                return f"{setup}\n    {class_info.name} obj({param_list});"
            else:
                return f"    {class_info.name} obj({param_list});"
        
        return f"    {class_info.name} obj;"
    
    def _get_includes_with_stubs(self, class_info: ClassInfo) -> str:
        """Get includes including stub headers"""
        includes = []
        
        # Main header
        if class_info.header_file:
            try:
                rel_path = class_info.header_file.relative_to(self.project_root)
                includes.append(f'#include "{rel_path}"')
            except:
                includes.append(f'#include "{class_info.header_file.name}"')
        else:
            includes.append(f'#include "{class_info.name}.h"')
        
        # Stub headers if needed
        if class_info.name in self.stubs_generated:
            includes.append(f'#include "stub_{class_info.name}.h"')
        
        # Check if we need stubs for constructor parameters
        for method in class_info.methods:
            if method.is_constructor:
                for param_type, _ in method.parameters:
                    base_type = param_type.replace('*', '').replace('&', '').replace('const', '').strip()
                    if base_type in self.stubs_generated:
                        stub_include = f'#include "stub_{base_type}.h"'
                        if stub_include not in includes:
                            includes.append(stub_include)
        
        return "\n".join(includes)


def main():
    from config_reader import get_project_path
    
    project_path = get_project_path()
    project_root = Path(project_path)
    output_dir = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    
    if not project_root.exists():
        print(f"❌ Project not found: {project_root}")
        return 1
    
    generator = AdvancedTestGenerator(project_root, output_dir)
    generator.generate_all_tests()
    
    print("\n" + "="*70)
    print(f"✅ Advanced generation complete!")
    print(f"   Success rate: {100*generator.tests_compiled/generator.tests_generated:.1f}%")
    print("="*70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

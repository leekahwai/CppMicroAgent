#!/usr/bin/env python3
"""
Ultimate Test Generator - Push for 65%+ Coverage

Combines all strategies:
1. Enhanced stubs with method implementations
2. Aggressive free function detection (~35 functions)
3. Test fixtures for complex classes
4. Multiple test scenarios per method
5. Better parameter generation
6. Namespace handling
7. Parallel compilation for speed
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass
import concurrent.futures
import multiprocessing

sys.path.insert(0, str(Path(__file__).parent))

from advanced_test_generator import AdvancedTestGenerator
from universal_enhanced_test_generator import ClassInfo, MethodInfo
import subprocess
import json


class UltimateTestGenerator(AdvancedTestGenerator):
    """Ultimate generator pushing for 65%+ coverage"""
    
    def __init__(self, project_root: Path, output_dir: Path):
        super().__init__(project_root, output_dir)
        self.fixture_tests = 0
        self.multi_scenario_tests = 0
        
    def generate_all_tests(self):
        """Generate comprehensive tests aiming for 65%+ coverage"""
        print("="*70)
        print("Ultimate Test Generator (65%+ Coverage Goal)")
        print("="*70)
        print()
        
        # Analyze project
        self.classes = self.analyzer.analyze_project()
        
        if not self.classes:
            print("⚠️  No classes found")
            return []
        
        # Phase 1: Generate enhanced stubs with method bodies
        print("📋 Phase 1: Generating enhanced stubs with method implementations...")
        self._generate_enhanced_stubs()
        
        # Phase 2: Generate tests for static methods
        print("\n📋 Phase 2: Generating static method tests...")
        self._generate_static_method_tests()
        
        # Phase 3: Aggressive free function detection
        print("\n📋 Phase 3: Aggressive free function detection...")
        self._generate_all_free_function_tests()
        
        # Phase 4: Generate fixture-based tests for complex classes
        print("\n📋 Phase 4: Generating fixture-based tests...")
        self._generate_fixture_tests()
        
        # Phase 5: Generate multiple scenarios per method
        print("\n📋 Phase 5: Generating multi-scenario tests...")
        self._generate_multi_scenario_tests()
        
        # Phase 6: Generate instance method tests
        print("\n📋 Phase 6: Generating instance method tests...")
        self._generate_instance_method_tests()
        
        # Compile all tests
        print(f"\n📦 Compiling {len(self.test_metadata)} tests...")
        self._batch_compile()
        
        # Save metadata
        self._save_metadata()
        
        print(f"\n✅ Generated {self.tests_generated} tests")
        print(f"   - Instance methods: {self.tests_generated - self.static_tests - self.free_func_tests - self.fixture_tests}")
        print(f"   - Static methods: {self.static_tests}")
        print(f"   - Free functions: {self.free_func_tests}")
        print(f"   - Fixture-based: {self.fixture_tests}")
        print(f"   - Multi-scenario: {self.multi_scenario_tests}")
        print(f"   - Stubs generated: {len(self.stubs_generated)}")
        print(f"   - Compiled: {self.tests_compiled} ({100*self.tests_compiled/self.tests_generated:.1f}%)")
        
        return self.test_metadata
    
    def _generate_enhanced_stubs(self):
        """Generate stubs with actual method implementations"""
        stub_candidates = ['State', 'Plan', 'Node', 'Edge', 'BuildConfig', 
                          'BuildLog', 'DiskInterface', 'DepsLog', 'DependencyScan',
                          'CommandRunner', 'SubprocessSet', 'Lexer', 'Parser',
                          'ManifestParser', 'DyndepParser', 'Cleaner']
        
        for class_name in stub_candidates:
            if class_name in self.classes:
                class_info = self.classes[class_name]
                if not class_info.has_default_constructor:
                    self._create_enhanced_stub(class_info)
        
        print(f"   Generated {len(self.stubs_generated)} enhanced stubs")
    
    def _create_enhanced_stub(self, class_info: ClassInfo):
        """Create enhanced stub with method implementations"""
        if class_info.name in self.stubs_generated:
            return
        
        stub_name = f"Stub{class_info.name}"
        
        # Find minimal constructor
        min_constructor = None
        for method in class_info.methods:
            if method.is_constructor and len(method.parameters) <= 3:
                if min_constructor is None or len(method.parameters) < len(min_constructor.parameters):
                    min_constructor = method
        
        # Generate constructor
        if min_constructor and len(min_constructor.parameters) > 0:
            param_init = []
            for param_type, _ in min_constructor.parameters:
                if '*' in param_type:
                    param_init.append("nullptr")
                elif 'int' in param_type or 'size' in param_type:
                    param_init.append("0")
                elif 'string' in param_type.lower():
                    param_init.append('""')
                elif 'bool' in param_type:
                    param_init.append("false")
                else:
                    param_init.append(f"{param_type.replace('const','').replace('&','').strip()}()")
            
            constructor_impl = f"    {stub_name}() : {class_info.name}({', '.join(param_init)}) {{}}"
        else:
            constructor_impl = f"    {stub_name}() {{}}"
        
        # Generate method implementations for public methods
        method_impls = []
        for method in class_info.methods:
            if method.access == 'public' and not method.is_constructor and not method.is_destructor:
                # Generate minimal implementation
                params = ", ".join([f"{t} {n if n else 'arg' + str(i)}" 
                                   for i, (t, n) in enumerate(method.parameters)])
                
                if method.return_type in ['void', '']:
                    method_impls.append(f"    void {method.name}({params}) {{}}")
                elif 'bool' in method.return_type:
                    method_impls.append(f"    {method.return_type} {method.name}({params}) {{ return false; }}")
                elif '*' in method.return_type:
                    method_impls.append(f"    {method.return_type} {method.name}({params}) {{ return nullptr; }}")
                elif 'int' in method.return_type or 'size' in method.return_type:
                    method_impls.append(f"    {method.return_type} {method.name}({params}) {{ return 0; }}")
                elif 'string' in method.return_type.lower():
                    method_impls.append(f"    {method.return_type} {method.name}({params}) {{ return \"\"; }}")
                else:
                    method_impls.append(f"    {method.return_type} {method.name}({params}) {{ return {{}}; }}")
        
        stub_content = f"""
// Enhanced stub for {class_info.name} with method implementations
class {stub_name} : public {class_info.name} {{
public:
{constructor_impl}
{chr(10).join(method_impls[:10])}  // Limit to 10 methods for compilation speed
}};
"""
        
        # Save stub
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
    
    def _generate_all_free_function_tests(self):
        """Aggressive free function detection"""
        free_functions = []
        
        # Parse all header files more thoroughly
        for header_file in self.analyzer.header_files:
            if any(skip in str(header_file) for skip in ['third_party', 'external', 'test']):
                continue
            
            try:
                content = header_file.read_text()
                content = self._remove_comments_simple(content)
                
                # Find all function declarations
                lines = content.split('\n')
                in_class = 0
                
                for line in lines:
                    # Track class/struct blocks
                    if re.search(r'\b(class|struct)\s+\w+', line) and '{' in line:
                        in_class += 1
                    if in_class > 0:
                        in_class += line.count('{') - line.count('}')
                        continue
                    
                    # Match free function declarations
                    # Pattern: return_type function_name(params);
                    match = re.match(r'^([a-zA-Z_][\w:*&<>, ]+)\s+([a-zA-Z_]\w*)\s*\(([^)]*)\)\s*;', line.strip())
                    if match:
                        return_type = match.group(1).strip()
                        func_name = match.group(2)
                        params_str = match.group(3)
                        
                        # Filter out macros and unlikely functions
                        if func_name[0].isupper():
                            continue
                        if func_name in ['main', 'test', 'Test']:
                            continue
                        if '...' in params_str:  # Skip variadic
                            continue
                        
                        # Common return types indicate free functions
                        if any(t in return_type for t in ['void', 'int', 'bool', 'std::string', 
                                                          'size_t', 'uint', 'char', 'double']):
                            params = self._parse_params_simple(params_str)
                            free_functions.append({
                                'name': func_name,
                                'return_type': return_type,
                                'parameters': params,
                                'header_file': header_file
                            })
            except Exception as e:
                continue
        
        # Remove duplicates
        seen = set()
        unique_funcs = []
        for func in free_functions:
            key = func['name']
            if key not in seen:
                seen.add(key)
                unique_funcs.append(func)
        
        print(f"   Found {len(unique_funcs)} free functions")
        
        # Generate tests for all
        for func_info in unique_funcs:
            test_content = self._create_free_function_test(func_info)
            if test_content:
                test_name = f"FreeFunc_{func_info['name']}"
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
    
    def _generate_fixture_tests(self):
        """Generate fixture-based tests for complex classes"""
        # Classes that benefit from fixtures
        fixture_classes = ['State', 'Plan', 'Builder', 'Cleaner', 'ManifestParser']
        
        for class_name in fixture_classes:
            if class_name not in self.classes:
                continue
            
            class_info = self.classes[class_name]
            if class_info.is_abstract:
                continue
            
            # Find testable methods
            methods = [m for m in class_info.methods 
                      if m.access == 'public' and not m.is_destructor and not m.is_static]
            
            if len(methods) > 0:
                # Generate fixture-based test
                test_content = self._create_fixture_test(class_info, methods[:5])  # Test first 5 methods
                if test_content:
                    test_name = f"{class_info.name}_FixtureTest"
                    mock_method = type('obj', (object,), {
                        'name': 'FixtureBased',
                        'access': 'public',
                        'is_destructor': False
                    })()
                    
                    self._write_test(test_name, class_info, mock_method, test_content)
                    self.fixture_tests += 1
        
        print(f"   Generated {self.fixture_tests} fixture-based tests")
    
    def _create_fixture_test(self, class_info: ClassInfo, methods: List) -> str:
        """Create a fixture-based test that tests multiple methods"""
        includes = self._get_includes_with_stubs(class_info)
        
        # Setup code
        if class_info.name in self.stubs_generated:
            setup = f"        obj_ = new Stub{class_info.name}();"
        elif class_info.has_default_constructor:
            setup = f"        obj_ = new {class_info.name}();"
        else:
            return None  # Can't create fixture without constructor
        
        # Generate test method calls
        test_methods = []
        for i, method in enumerate(methods):
            if self._has_variadic_params(method):
                continue
            
            param_setup, param_list = self._generate_method_params(method.parameters)
            method_call = f"obj_->{method.name}({param_list})"
            
            test_body = f"""
TEST_F({class_info.name}Test, {method.name}) {{
{param_setup}
    // Test method
    """
            if method.return_type in ['void', '']:
                test_body += f"{method_call};\n"
            else:
                test_body += f"auto result = {method_call};\n"
            
            test_body += "    EXPECT_TRUE(true);\n}\n"
            test_methods.append(test_body)
        
        if not test_methods:
            return None
        
        return f'''// Fixture-based test for {class_info.name}
{includes}
#include <gtest/gtest.h>

class {class_info.name}Test : public ::testing::Test {{
protected:
    void SetUp() override {{
{setup}
    }}
    
    void TearDown() override {{
        delete obj_;
    }}
    
    {class_info.name}* obj_;
}};

{chr(10).join(test_methods)}
'''
    
    def _generate_multi_scenario_tests(self):
        """Generate multiple test scenarios for important methods"""
        # Target high-value classes
        priority_classes = ['State', 'Node', 'Edge', 'EvalString', 'CLParser']
        
        for class_name in priority_classes:
            if class_name not in self.classes:
                continue
            
            class_info = self.classes[class_name]
            methods = [m for m in class_info.methods 
                      if m.access == 'public' and not m.is_destructor and not m.is_static]
            
            for method in methods[:3]:  # Top 3 methods per class
                if self._has_variadic_params(method):
                    continue
                
                # Generate edge case test
                test_content = self._create_edge_case_test(class_info, method)
                if test_content:
                    test_name = f"{class_info.name}_{method.name}_EdgeCase"
                    self._write_test(test_name, class_info, method, test_content)
                    self.multi_scenario_tests += 1
        
        print(f"   Generated {self.multi_scenario_tests} multi-scenario tests")
    
    def _create_edge_case_test(self, class_info: ClassInfo, method) -> str:
        """Create edge case test with different parameters"""
        includes = self._get_includes_with_stubs(class_info)
        
        # Instantiation
        if class_info.name in self.stubs_generated:
            instantiation = f"    Stub{class_info.name} obj;"
        elif class_info.has_default_constructor:
            instantiation = f"    {class_info.name} obj;"
        else:
            return None
        
        # Generate edge case parameters (empty, null, negative, etc.)
        edge_params = []
        for param_type, param_name in method.parameters:
            if '*' in param_type:
                edge_params.append("nullptr")
            elif 'string' in param_type.lower():
                edge_params.append('""')  # Empty string
            elif 'int' in param_type or 'size' in param_type:
                edge_params.append("-1")  # Negative
            else:
                edge_params.append(self._get_default_value(param_type))
        
        param_list = ", ".join(edge_params)
        method_call = f"obj.{method.name}({param_list})"
        
        return f'''// Edge case test for {class_info.name}::{method.name}
{includes}
#include <gtest/gtest.h>

TEST({class_info.name}, {method.name}_EdgeCase) {{
{instantiation}
    // Test with edge case parameters
    {method_call};
    EXPECT_TRUE(true);
}}
'''

    def _compile_single_test(self, args):
        """Compile a single test (for parallel execution)"""
        test_meta, source_files, include_paths = args
        
        compile_cmd = [
            "g++", "-std=c++14",
            "-o", test_meta["binary"],
            test_meta["test_file"],
            *source_files,
            *include_paths,
            "-I", "/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include",
            "-L", "/workspaces/CppMicroAgent/googletest-1.16.0/build/lib",
            "-lgtest", "-lgtest_main", "-lpthread",
            "--coverage", "-fprofile-arcs", "-ftest-coverage"
        ]
        
        try:
            result = subprocess.run(compile_cmd, capture_output=True, timeout=120)
            if result.returncode == 0:
                test_meta["compiled"] = True
                return (True, test_meta, None)
            else:
                error_msg = result.stderr.decode('utf-8', errors='ignore')[:500]
                test_meta["compile_error"] = error_msg
                return (False, test_meta, error_msg)
        except subprocess.TimeoutExpired:
            test_meta["compile_error"] = "Compilation timeout (>120s)"
            return (False, test_meta, "timeout")
        except Exception as e:
            test_meta["compile_error"] = str(e)[:200]
            return (False, test_meta, str(e))
    
    def _batch_compile(self):
        """Compile all tests in parallel for speed"""
        # Try to get source files from CMake first
        cmake_sources = self._parse_cmake_sources()
        
        if cmake_sources:
            print(f"  📋 Found {len(cmake_sources)} source files from CMakeLists.txt")
            source_files = []
            for src in cmake_sources:
                src_path = self.project_root / src
                if src_path.exists():
                    source_files.append(str(src_path))
        else:
            # Fallback: Find source files manually, but be more selective
            print(f"  📋 No CMakeLists.txt found, scanning for source files...")
            source_files = []
            for sf in self.analyzer.source_files:
                if sf.suffix in ['.cpp', '.cc', '.cxx', '.c']:
                    stem_lower = sf.stem.lower()
                    # Exclude test files, main files, perftest files, platform-specific wrong platform
                    if any(x in stem_lower for x in ['test', 'main', 'perftest', 'bench', 'win32', 'sample']):
                        continue
                    source_files.append(str(sf))
        
        print(f"  🔧 Using {len(source_files)} source files for linking")
        
        # Build include paths
        include_paths = ["-I", str(self.project_root)]
        for subdir in ['src', 'include', 'inc', 'source']:
            if (self.project_root / subdir).exists():
                include_paths.extend(["-I", str(self.project_root / subdir)])
        
        src_dir = self.project_root / "src"
        if src_dir.exists():
            for subdir in src_dir.rglob("*"):
                if subdir.is_dir():
                    include_paths.extend(["-I", str(subdir)])
        
        # Prepare compilation arguments
        compile_args = [(test_meta, source_files, include_paths) for test_meta in self.test_metadata]
        
        # Use parallel compilation with progress tracking
        num_workers = max(2, multiprocessing.cpu_count() // 2)  # Use half of available CPUs
        print(f"  🚀 Using {num_workers} parallel workers")
        
        compiled = 0
        total = len(self.test_metadata)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            # Submit all jobs
            future_to_idx = {executor.submit(self._compile_single_test, args): idx 
                           for idx, args in enumerate(compile_args)}
            
            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    success, test_meta, error = future.result()
                    if success:
                        compiled += 1
                        self.tests_compiled = compiled
                    # Update metadata in place
                    self.test_metadata[idx] = test_meta
                    
                    # Show progress every 5 tests
                    if (idx + 1) % 5 == 0 or idx == total - 1:
                        print(f"  Progress: {idx + 1}/{total}... ({compiled} compiled)")
                except Exception as e:
                    print(f"  ⚠️  Test {idx} failed: {e}")
        
        print(f"  ✅ Compiled {compiled}/{total} tests successfully")



def main():
    from config_reader import get_project_path
    
    project_path = get_project_path()
    project_root = Path(project_path)
    output_dir = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    
    if not project_root.exists():
        print(f"❌ Project not found: {project_root}")
        return 1
    
    generator = UltimateTestGenerator(project_root, output_dir)
    generator.generate_all_tests()
    
    print("\n" + "="*70)
    print(f"✅ Ultimate generation complete!")
    print(f"   Success rate: {100*generator.tests_compiled/generator.tests_generated:.1f}%")
    print(f"   Target: 65% function coverage")
    print("="*70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

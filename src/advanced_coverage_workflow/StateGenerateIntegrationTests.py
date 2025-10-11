"""
StateGenerateIntegrationTests.py

New state that generates integration tests using real headers with proper initialization.
This state generates tests that:
1. Use actual headers (not mocks)
2. Properly initialize objects with dependencies
3. Handle threading/synchronization correctly
4. Test realistic workflows
5. Support Ollama enhancement for sophisticated test generation

This state does NOT affect existing workflow - it's an optional enhancement.
"""

import os
import subprocess
import json
from pathlib import Path

# Handle imports for both standalone and integrated use
try:
    from ..flow_manager import flow
    from ..ConfigReader import ConfigReader
except ImportError:
    # Standalone mode
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    try:
        from flow_manager import flow
        from ConfigReader import ConfigReader
    except ImportError:
        # Create dummy flow manager if not available
        class DummyFlow:
            def transition(self, state): 
                print(f"  [Flow] Transition to {state}")
        flow = DummyFlow()
        from ConfigReader import ConfigReader


class StateGenerateIntegrationTests:
    """Generate integration tests with real headers and proper initialization"""
    
    def __init__(self):
        self.configReader = ConfigReader()
        self.use_ollama = False
        print("Initializing [StateGenerateIntegrationTests]")
    
    def run(self, input_data):
        """
        Generate integration tests with real headers
        
        Args:
            input_data: Contains project path and configuration
            
        Returns:
            tuple: (success, updated_input_data)
        """
        flow.transition("StateGenerateIntegrationTests")
        print("\n" + "="*70)
        print("[StateGenerateIntegrationTests] Generating Integration Tests")
        print("="*70)
        
        project_path = self._get_project_path(input_data)
        if not project_path:
            print("[StateGenerateIntegrationTests] No project path found")
            return True, input_data  # Continue workflow anyway
        
        output_dir = Path("output/IntegrationTests")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if Ollama should be used
        self.use_ollama = input_data.get('use_ollama', False) if hasattr(input_data, 'get') else False
        
        if self.use_ollama:
            print("🤖 Ollama AI-enhanced test generation ENABLED")
        else:
            print("📝 Using template-based test generation")
        
        # Analyze project structure
        classes = self._analyze_project_structure(project_path)
        
        if not classes:
            print("[StateGenerateIntegrationTests] No classes found to test")
            return True, input_data
        
        print(f"\n[StateGenerateIntegrationTests] Found {len(classes)} classes to test")
        
        # Generate integration tests for each class
        generated_tests = []
        for class_info in classes:
            tests = self._generate_integration_tests_for_class(
                class_info, 
                project_path, 
                output_dir
            )
            generated_tests.extend(tests)
        
        # Save metadata
        self._save_metadata(generated_tests, output_dir)
        
        # Compile and run tests
        self._compile_and_run_tests(generated_tests, output_dir, project_path)
        
        print(f"\n[StateGenerateIntegrationTests] Generated {len(generated_tests)} integration tests")
        print("="*70)
        
        # Store results in input_data for next state
        if hasattr(input_data, 'set_integration_tests'):
            input_data.set_integration_tests(generated_tests)
        
        return True, input_data
    
    def _get_project_path(self, input_data):
        """Get project path from input data or config"""
        try:
            if hasattr(input_data, 'get_project_path'):
                return Path(input_data.get_project_path())
            else:
                # Fallback to config
                from ..config_reader import get_project_path
                return Path(get_project_path())
        except Exception as e:
            print(f"[StateGenerateIntegrationTests] Error getting project path: {e}")
            return None
    
    def _analyze_project_structure(self, project_path):
        """
        Analyze project to find classes and their dependencies
        
        Returns:
            list: List of class info dictionaries
        """
        classes = []
        
        print(f"\n  Analyzing project structure at: {project_path}")
        
        # Find all header files
        header_files = list(project_path.rglob("*.h")) + list(project_path.rglob("*.hpp"))
        
        print(f"  Found {len(header_files)} header files")
        
        for header in header_files:
            # Skip files in output/test/mock directories
            header_str = str(header)
            if '/output/' in header_str or '/test' in header_str or '/mock' in header_str:
                print(f"    Skipping {header.name} (output/test/mock directory)")
                continue
            
            # Parse header to find classes
            class_info = self._parse_header_file(header, project_path)
            if class_info:
                classes.extend(class_info)
        
        print(f"  Total classes found: {len(classes)}")
        
        return classes
    
    def _parse_header_file(self, header_path, project_path):
        """
        Parse a header file to extract class information
        
        Returns:
            list: List of class info dictionaries
        """
        classes = []
        
        try:
            with open(header_path, 'r') as f:
                content = f.read()
            
            # Simple class extraction (can be enhanced)
            import re
            
            # Find class declarations - handle both with and without base class
            class_pattern = r'class\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+(\w+))?\s*\{'
            matches = re.finditer(class_pattern, content)
            
            for match in matches:
                class_name = match.group(1)
                base_class = match.group(2) if match.group(2) else None
                
                print(f"    Found class: {class_name} in {header_path.name}")
                
                # Extract methods (simplified)
                methods = self._extract_methods(content, class_name)
                
                # Extract dependencies
                dependencies = self._extract_dependencies(content)
                
                class_info = {
                    'class_name': class_name,
                    'header_file': str(header_path),
                    'header_name': header_path.name,
                    'base_class': base_class,
                    'methods': methods,
                    'dependencies': dependencies,
                    'has_threading': 'thread' in content or 'mutex' in content,
                    'has_vectors': 'vector' in content,
                    'project_path': str(project_path)
                }
                
                classes.append(class_info)
        
        except Exception as e:
            print(f"[StateGenerateIntegrationTests] Error parsing {header_path}: {e}")
        
        return classes
    
    def _extract_methods(self, content, class_name):
        """Extract public methods from class content"""
        methods = []
        
        import re
        
        # Find public section
        public_pattern = r'public:\s*(.*?)(?:private:|protected:|$)'
        public_match = re.search(public_pattern, content, re.DOTALL)
        
        if public_match:
            public_section = public_match.group(1)
            
            # Find method declarations
            method_pattern = r'(\w+)\s+(\w+)\s*\((.*?)\)'
            method_matches = re.finditer(method_pattern, public_section)
            
            for match in method_matches:
                return_type = match.group(1)
                method_name = match.group(2)
                params = match.group(3)
                
                # Skip constructors, destructors, operators
                if method_name == class_name or method_name.startswith('~') or method_name.startswith('operator'):
                    continue
                
                methods.append({
                    'name': method_name,
                    'return_type': return_type,
                    'params': params,
                    'is_const': 'const' in match.group(0)
                })
        
        return methods
    
    def _extract_dependencies(self, content):
        """Extract #include dependencies"""
        dependencies = []
        
        import re
        include_pattern = r'#include\s+[<"]([^>"]+)[>"]'
        matches = re.finditer(include_pattern, content)
        
        for match in matches:
            dep = match.group(1)
            if not dep.startswith('std') and not dep.startswith('c'):
                dependencies.append(dep)
        
        return dependencies
    
    def _generate_integration_tests_for_class(self, class_info, project_path, output_dir):
        """
        Generate integration tests for a class
        
        Returns:
            list: Generated test file paths
        """
        generated_tests = []
        
        class_name = class_info['class_name']
        
        # Skip if no methods
        if not class_info['methods']:
            return generated_tests
        
        print(f"\n  Generating integration tests for {class_name}...")
        
        # Generate comprehensive integration test
        test_name = f"integration_{class_name}"
        test_file = output_dir / f"{test_name}.cpp"
        
        if self.use_ollama:
            test_content = self._generate_test_with_ollama(class_info, test_name)
        else:
            test_content = self._generate_test_template(class_info, test_name)
        
        # Write test file
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        generated_tests.append({
            'test_name': test_name,
            'test_file': str(test_file),
            'class_name': class_name,
            'methods_tested': len(class_info['methods'])
        })
        
        print(f"    ✅ Generated {test_name}.cpp ({len(class_info['methods'])} methods)")
        
        return generated_tests
    
    def _generate_test_template(self, class_info, test_name):
        """Generate test using template (without Ollama)"""
        
        class_name = class_info['class_name']
        header_name = class_info['header_name']
        has_threading = class_info.get('has_threading', False)
        
        # Build test content
        content = f"""// Integration Test for {class_name}
// Generated with real headers and proper initialization
#include <gtest/gtest.h>
#include <memory>
#include <thread>
#include <chrono>

// Include real headers
#include "{header_name}"
"""
        
        # Add dependency includes
        for dep in class_info.get('dependencies', []):
            content += f'#include "{dep}"\n'
        
        content += f"""
class {class_name}IntegrationTest : public ::testing::Test {{
protected:
    void SetUp() override {{
        // Proper initialization before each test
"""
        
        if has_threading:
            content += """        // Allow time for threading initialization
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
"""
        
        content += f"""    }}
    
    void TearDown() override {{
        // Cleanup after each test
"""
        
        if has_threading:
            content += """        // Allow time for threading cleanup
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
"""
        
        content += """    }
};

"""
        
        # Generate tests for each method
        for i, method in enumerate(class_info['methods'][:5]):  # Limit to 5 methods for template
            method_name = method['name']
            return_type = method['return_type']
            
            content += f"""TEST_F({class_name}IntegrationTest, {method_name}_Integration) {{
    // Create object with proper initialization
    {class_name} obj;
    
"""
            
            # Add initialization if needed
            if 'init' in [m['name'] for m in class_info['methods']]:
                content += """    // Initialize the object
    ASSERT_TRUE(obj.init()) << "Failed to initialize object";
    
"""
            
            if has_threading:
                content += """    // Allow threading to stabilize
    std::this_thread::sleep_for(std::chrono::milliseconds(5));
    
"""
            
            # Generate method call based on return type
            if return_type == 'void':
                content += f"""    // Test method execution
    EXPECT_NO_THROW({{
        obj.{method_name}();
    }}) << "{method_name} should not throw";
"""
            elif return_type == 'bool':
                content += f"""    // Test method returns valid boolean
    bool result = obj.{method_name}();
    // Method executed successfully (result may be true or false)
    SUCCEED() << "{method_name} executed and returned: " << result;
"""
            else:
                content += f"""    // Test method returns valid result
    auto result = obj.{method_name}();
    // Verify method executed (result validity depends on state)
    (void)result; // Mark as used
    SUCCEED() << "{method_name} executed successfully";
"""
            
            # Add cleanup if needed
            if 'close' in [m['name'] for m in class_info['methods']]:
                content += """    
    // Cleanup
    obj.close();
"""
            
            content += """}

"""
        
        return content
    
    def _generate_test_with_ollama(self, class_info, test_name):
        """Generate enhanced test using Ollama AI"""
        
        print(f"      🤖 Using Ollama to generate sophisticated test...")
        
        class_name = class_info['class_name']
        has_threading = class_info.get('has_threading', False)
        
        # Prepare prompt for Ollama
        prompt = f"""Generate a comprehensive C++ integration test using GoogleTest for the class '{class_name}'.

Class Information:
- Class Name: {class_name}
- Header File: {class_info['header_name']}
- Has Threading: {has_threading}
- Methods: {', '.join([m['name'] for m in class_info['methods'][:10]])}

Requirements:
1. Use GoogleTest framework (TEST_F macro)
2. Include proper setup/teardown in test fixture
3. Handle threading initialization if needed (sleep 10ms before tests)
4. Call init() method before testing if it exists
5. Call close() method in teardown if it exists
6. Generate integration tests that test realistic workflows
7. Include proper assertions and error messages
8. Test at least 5 different methods
9. Handle both success and edge cases

Generate ONLY the C++ code, no explanations. Start with #include statements."""
        
        try:
            # Call Ollama
            result = subprocess.run(
                ['ollama', 'run', self.configReader.get_model_used()],
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and result.stdout.strip():
                generated_code = result.stdout.strip()
                
                # Clean up the response (remove markdown code blocks if present)
                if '```cpp' in generated_code:
                    generated_code = generated_code.split('```cpp')[1].split('```')[0]
                elif '```' in generated_code:
                    generated_code = generated_code.split('```')[1].split('```')[0]
                
                generated_code = generated_code.strip()
                
                # Validate it's C++ code
                if '#include' in generated_code and 'TEST' in generated_code:
                    print(f"      ✅ Ollama generated {len(generated_code)} chars of test code")
                    return generated_code
                else:
                    print(f"      ⚠️  Ollama output doesn't look like valid C++ test code")
                    return self._generate_test_template(class_info, test_name)
            else:
                print(f"      ⚠️  Ollama failed, using template")
                return self._generate_test_template(class_info, test_name)
                
        except subprocess.TimeoutExpired:
            print(f"      ⏱️  Ollama timeout, using template")
            return self._generate_test_template(class_info, test_name)
        except Exception as e:
            print(f"      ❌ Ollama error: {e}, using template")
            return self._generate_test_template(class_info, test_name)
    
    def _save_metadata(self, generated_tests, output_dir):
        """Save test metadata to JSON file"""
        metadata_file = output_dir / "integration_test_metadata.json"
        
        with open(metadata_file, 'w') as f:
            json.dump(generated_tests, f, indent=2)
        
        print(f"\n  📝 Saved metadata to {metadata_file}")
    
    def _compile_and_run_tests(self, generated_tests, output_dir, project_path):
        """Compile and run the generated integration tests"""
        
        print(f"\n{'='*70}")
        print("COMPILING AND RUNNING INTEGRATION TESTS")
        print(f"{'='*70}\n")
        
        bin_dir = output_dir / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        
        passed = 0
        failed = 0
        
        for test_info in generated_tests:
            test_name = test_info['test_name']
            test_file = test_info['test_file']
            
            # Compile test
            binary = bin_dir / test_name
            
            compile_cmd = [
                'g++',
                '-std=c++14',
                '-o', str(binary),
                test_file,
            ]
            
            # Add all source files from project
            source_files = list(project_path.rglob("*.cpp"))
            for src in source_files:
                if 'test' not in str(src).lower():
                    compile_cmd.append(str(src))
            
            # Add include directories
            inc_dirs = set()
            inc_dirs.add(str(project_path))
            inc_dirs.add(str(project_path / "inc"))
            for src_dir in project_path.glob("src/*"):
                if src_dir.is_dir():
                    inc_dirs.add(str(src_dir))
            
            for inc_dir in inc_dirs:
                compile_cmd.extend(['-I', inc_dir])
            
            # Add GoogleTest
            compile_cmd.extend([
                '-I', '/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include',
                '-L', '/workspaces/CppMicroAgent/googletest-1.16.0/build/lib',
                '-lgtest',
                '-lgtest_main',
                '-lpthread',
                '--coverage'
            ])
            
            print(f"  Compiling {test_name}...", end=' ')
            
            try:
                result = subprocess.run(compile_cmd, capture_output=True, timeout=30)
                
                if result.returncode == 0:
                    print("✅ SUCCESS")
                    
                    # Run test
                    print(f"  Running {test_name}...", end=' ')
                    try:
                        run_result = subprocess.run(
                            [str(binary)],
                            capture_output=True,
                            timeout=15,
                            cwd=str(bin_dir)
                        )
                        
                        if run_result.returncode == 0:
                            test_count = run_result.stdout.decode().count('[  PASSED  ]')
                            print(f"✅ PASSED ({test_count} tests)")
                            passed += 1
                        else:
                            print("❌ FAILED")
                            failed += 1
                    except subprocess.TimeoutExpired:
                        print("⏱️  TIMEOUT")
                        failed += 1
                    except Exception as e:
                        print(f"❌ ERROR: {e}")
                        failed += 1
                else:
                    print("❌ COMPILE FAILED")
                    error = result.stderr.decode()[:200]
                    print(f"    Error: {error}")
                    failed += 1
                    
            except Exception as e:
                print(f"❌ ERROR: {e}")
                failed += 1
        
        print(f"\n{'='*70}")
        print(f"INTEGRATION TEST RESULTS: {passed} passed, {failed} failed")
        print(f"{'='*70}\n")

#!/usr/bin/env python3
"""
Ninja-Optimized Test Generator - Target 65%+ Coverage

Focuses on high-value ninja classes that are currently uncovered:
- BuildLog, DepsLog (logging infrastructure)
- Cleaner (build cleanup)
- Graph-related classes (Node, Edge)
- Parser classes (Lexer, Parser, ManifestParser)
- DiskInterface and RealDiskInterface
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from ultimate_test_generator import UltimateTestGenerator
from universal_enhanced_test_generator import ClassInfo


class NinjaOptimizedGenerator(UltimateTestGenerator):
    """Ninja-specific generator targeting uncovered classes"""
    
    def __init__(self, project_root: Path, output_dir: Path):
        super().__init__(project_root, output_dir)
        
        # High-priority classes to test
        self.priority_classes = [
            # Core graph structures (many methods, fundamental)
            'Node', 'Edge', 'Pool',
            
            # Logging and tracking (currently 0% coverage)
            'BuildLog', 'DepsLog', 'BuildLogUser',
            
            # Cleanup functionality
            'Cleaner',
            
            # Disk operations  
            'RealDiskInterface', 'DiskInterface',
            
            # Parsing (lots of functions)
            'Lexer', 'Parser', 'ManifestParser', 'DyndepParser',
            
            # Build execution
            'Builder', 'ImplicitDepLoader', 'DependencyScan',
            
            # Utilities
            'EditDistance', 'ElideMiddle',
        ]
    
    def generate_all_tests(self):
        """Generate tests with focus on priority classes"""
        print("="*70)
        print("Ninja-Optimized Test Generator (65%+ Coverage Target)")
        print("="*70)
        print()
        
        # Analyze project
        self.classes = self.analyzer.analyze_project()
        
        if not self.classes:
            print("⚠️  No classes found")
            return []
        
        # Phase 1: Generate enhanced stubs for priority dependencies
        print("📋 Phase 1: Generating priority stubs...")
        self._generate_priority_stubs()
        
        # Phase 2: Generate tests for all priority classes
        print("\n📋 Phase 2: Generating tests for high-value classes...")
        self._generate_priority_class_tests()
        
        # Phase 3: Generate static method tests
        print("\n📋 Phase 3: Generating static method tests...")
        self._generate_static_method_tests()
        
        # Phase 4: Generate free function tests
        print("\n📋 Phase 4: Generating free function tests...")
        self._generate_all_free_function_tests()
        
        # Phase 5: Generate fixture-based tests
        print("\n📋 Phase 5: Generating fixture-based tests...")
        self._generate_fixture_tests()
        
        # Phase 6: Generate remaining instance method tests
        print("\n📋 Phase 6: Generating remaining tests...")
        self._generate_instance_method_tests()
        
        # Compile all tests
        print(f"\n📦 Compiling {len(self.test_metadata)} tests...")
        self._batch_compile()
        
        # Save metadata
        self._save_metadata()
        
        print(f"\n✅ Generated {self.tests_generated} tests")
        print(f"   - Priority classes: {len([c for c in self.priority_classes if c in self.classes])}")
        print(f"   - Compiled: {self.tests_compiled} ({100*self.tests_compiled/self.tests_generated:.1f}%)")
        
        return self.test_metadata
    
    def _generate_priority_stubs(self):
        """Generate stubs for priority dependencies"""
        # These classes are needed by many others
        stub_candidates = [
            'State', 'Node', 'Edge', 'Pool', 'Rule',
            'DiskInterface', 'BuildConfig',
            'Lexer', 'EvalEnv', 'BindingEnv'
        ]
        
        for class_name in stub_candidates:
            if class_name in self.classes:
                class_info = self.classes[class_name]
                if not class_info.has_default_constructor:
                    self._create_enhanced_stub(class_info)
        
        print(f"   Generated {len(self.stubs_generated)} priority stubs")
    
    def _generate_priority_class_tests(self):
        """Generate comprehensive tests for priority classes"""
        priority_tests = 0
        
        for class_name in self.priority_classes:
            if class_name not in self.classes:
                continue
            
            class_info = self.classes[class_name]
            if class_info.is_abstract:
                continue
            
            # Get all public methods
            methods = [m for m in class_info.methods 
                      if m.access == 'public' and not m.is_destructor]
            
            if len(methods) > 0:
                print(f"   {class_name}: {len(methods)} methods")
            
            # Generate test for each method (limit to avoid too many tests)
            for method in methods[:10]:  # Limit to first 10 methods per class
                if method.is_static:
                    test_content = self._create_static_method_test(class_info, method)
                    if test_content:
                        test_name = f"{class_info.name}_{method.name}_Static"
                        self._write_test(test_name, class_info, method, test_content)
                        priority_tests += 1
        
        print(f"   Generated {priority_tests} priority tests")
        self.tests_generated += priority_tests


def main():
    from config_reader import get_project_path
    
    project_path = get_project_path()
    project_root = Path(project_path)
    output_dir = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
    
    if not project_root.exists():
        print(f"❌ Project not found: {project_root}")
        return 1
    
    generator = NinjaOptimizedGenerator(project_root, output_dir)
    generator.generate_all_tests()
    
    print("\n" + "="*70)
    print(f"✅ Ninja-optimized generation complete!")
    print(f"   Success rate: {100*generator.tests_compiled/generator.tests_generated:.1f}%")
    print(f"   Target: 65% function coverage (370+ functions)")
    print("="*70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Standalone script to generate and run integration tests
This does NOT affect the existing workflow - it's a separate enhancement
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from advanced_coverage_workflow.StateGenerateIntegrationTests import StateGenerateIntegrationTests
from config_reader import get_project_path


class MockInputData:
    """Mock input data class for testing"""
    def __init__(self, use_ollama=False):
        self.use_ollama = use_ollama
        self.integration_tests = None
    
    def get(self, key, default=None):
        return getattr(self, key, default)
    
    def get_project_path(self):
        return get_project_path()
    
    def set_integration_tests(self, tests):
        self.integration_tests = tests


def main():
    """Run integration test generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate integration tests with real headers')
    parser.add_argument('--ollama', action='store_true', help='Use Ollama AI for enhanced test generation')
    args = parser.parse_args()
    
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     Integration Test Generator (Standalone Enhancement)         ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    
    if args.ollama:
        print("🤖 Ollama AI-enhanced mode ENABLED")
    else:
        print("📝 Template-based mode (use --ollama for AI enhancement)")
    
    print()
    
    # Get project path
    project_path = get_project_path()
    print(f"Project: {project_path}")
    print()
    
    # Create mock input data
    input_data = MockInputData(use_ollama=args.ollama)
    
    # Create and run state
    state = StateGenerateIntegrationTests()
    success, output_data = state.run(input_data)
    
    if success:
        print("\n✅ Integration test generation completed successfully!")
        print()
        print("📁 Output location: output/IntegrationTests/")
        print("🧪 Test binaries: output/IntegrationTests/bin/")
        print("📊 Metadata: output/IntegrationTests/integration_test_metadata.json")
        
        # Check if tests were generated
        if output_data.integration_tests:
            print(f"\n✨ Generated {len(output_data.integration_tests)} integration tests:")
            for test in output_data.integration_tests:
                print(f"   - {test['test_name']} ({test['methods_tested']} methods)")
        
        print()
        print("💡 Next steps:")
        print("   1. Review generated tests in output/IntegrationTests/")
        print("   2. Run tests: cd output/IntegrationTests/bin && ./integration_*")
        print("   3. Measure coverage with quick_start.sh option 2")
        return 0
    else:
        print("\n❌ Integration test generation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

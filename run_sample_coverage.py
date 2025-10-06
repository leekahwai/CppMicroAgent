#!/usr/bin/env python3
"""
One-click execution: Complete iterative coverage analysis
"""
import os
import sys
from States.Query import Query
from States_Coverage.StateMachine import StateMachine
from ConfigReader import ConfigReader

def main():
    print("🔄 C++ MICRO AGENT - ONE-CLICK COMPLETE ANALYSIS")
    print("=" * 60)
    
    # Get project path from configuration
    configReader = ConfigReader()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.join(script_dir, configReader.get_default_project_path())
    
    print(f"📁 Project: {project_path}")
    print(f"🎯 Target: Generate unit tests with {configReader.get_coverage_target()}%+ coverage")
    print(f"🔄 Max Iterations: {configReader.get_max_iterations()}")
    print("🔄 Method: Iterative improvement with LLM feedback")
    print(f"🧹 Clean Output: {'Yes' if configReader.get_clean_output_before_run() else 'No (backup mode)'}")
    print()
    print("⚡ FULL WORKFLOW INCLUDES:")
    print("   1️⃣  Parse CMake project structure")
    print("   2️⃣  Generate dependency mocks")
    print("   3️⃣  Compile with coverage instrumentation") 
    print("   4️⃣  Generate comprehensive unit tests")
    print("   5️⃣  🔄 Iterative coverage improvement loop")
    print("   6️⃣  Generate final detailed reports")
    print()
    
    # Check if the project exists
    cmake_file = os.path.join(project_path, "CMakeLists.txt")
    if not os.path.exists(cmake_file):
        print(f"❌ Error: CMakeLists.txt not found at {cmake_file}")
        print(f"💡 Update the 'default_project_path' in CppMicroAgent.cfg")
        print(f"   Current setting: {configReader.get_default_project_path()}")
        return 1
    
    print("🚀 Starting complete analysis...")
    print("-" * 60)
    
    try:
        # ONE COMMAND DOES EVERYTHING
        query = Query(project_path)
        sm = StateMachine(query)
        sm.run()
        
        print("\n" + "=" * 60)
        print("✅ COMPLETE ANALYSIS FINISHED!")
        print("=" * 60)
        
        # Show comprehensive results
        iteration_results = query.get_coverage_iteration_results()
        coverage_data = query.get_coverage_data()
        
        if iteration_results:
            final_coverage = iteration_results.get("final_coverage", 0.0)
            iterations = iteration_results.get("iterations_completed", 0)
            target_achieved = iteration_results.get("target_achieved", False)
            
            print(f"📊 Final Coverage: {final_coverage:.1f}%")
            print(f"🔄 Iterations: {iterations}")
            print(f"🎯 Target Achieved: {'✅ Yes' if target_achieved else '❌ No'}")
            
            if target_achieved:
                print("🏆 SUCCESS: High-quality unit tests generated with target coverage!")
            else:
                print("🔄 PARTIAL: Coverage improved, may need manual optimization")
        
        print("\n📂 All Generated Files:")
        output_dir = os.path.join(configReader.get_output_directory(), "UnitTestCoverage")
        
        # Unit tests
        unit_tests_dir = os.path.join(output_dir, "unit_tests")
        if os.path.exists(unit_tests_dir):
            test_files = [f for f in os.listdir(unit_tests_dir) if f.endswith('.cpp')]
            print(f"   🧪 Unit Tests: {len(test_files)} files")
            for test_file in sorted(test_files):
                file_path = os.path.join(unit_tests_dir, test_file)
                file_size = os.path.getsize(file_path)
                print(f"      • {test_file} ({file_size} bytes)")
        
        # Dependency mocks
        mock_count = 0
        for root, dirs, files in os.walk(output_dir):
            mock_count += len([f for f in files if f.endswith('.h') and 'unit_tests' not in root])
        if mock_count > 0:
            print(f"   🎭 Dependency Mocks: {mock_count} header files")
        
        # Coverage reports
        if os.path.exists(os.path.join(output_dir, "coverage_data")):
            print(f"   📊 Coverage Analysis:")
            if os.path.exists(os.path.join(output_dir, "coverage_data", "lcov_html")):
                html_path = os.path.join(output_dir, "coverage_data", "lcov_html", "index.html")
                print(f"      🌐 Interactive HTML: {html_path}")
            
            coverage_info = os.path.join(output_dir, "coverage_data", "coverage.info")
            if os.path.exists(coverage_info):
                print(f"      📋 LCOV Data: {coverage_info}")
        
        # Main report
        report_file = os.path.join(output_dir, "coverage_report.txt")
        if os.path.exists(report_file):
            file_size = os.path.getsize(report_file)
            print(f"   📄 Comprehensive Report: {report_file} ({file_size} bytes)")
        
        print(f"\n📁 All files in: {os.path.abspath(output_dir)}")
        print("\n💡 View Results:")
        print("   python3 show_coverage_report.py     # Full detailed report")
        print("   python3 show_coverage_summary.py    # Quick summary")
        if 'html_path' in locals():
            print(f"   open {html_path}                    # Interactive coverage browser")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
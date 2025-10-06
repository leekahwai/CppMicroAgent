#!/usr/bin/env python3
"""
Test the reorganized structure and configuration
"""
import os
import sys
from ConfigReader import ConfigReader
from OutputManager import OutputManager

def main():
    print("🔧 C++ MICRO AGENT - STRUCTURE VERIFICATION")
    print("=" * 55)
    
    # Test configuration reading
    print("📋 CONFIGURATION SETTINGS:")
    try:
        configReader = ConfigReader()
        print(f"   🎯 Coverage Target: {configReader.get_coverage_target()}%")
        print(f"   🔄 Max Iterations: {configReader.get_max_iterations()}")
        print(f"   📁 Default Project: {configReader.get_default_project_path()}")
        print(f"   🧹 Clean Output: {configReader.get_clean_output_before_run()}")
        print(f"   📂 Output Directory: {configReader.get_output_directory()}")
        print("   ✅ Configuration loaded successfully")
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return 1
    
    print()
    print("📁 PROJECT STRUCTURE:")
    
    # Check project path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.join(script_dir, configReader.get_default_project_path())
    
    print(f"   📂 Project Path: {project_path}")
    if os.path.exists(project_path):
        print("   ✅ Project directory exists")
        
        cmake_file = os.path.join(project_path, "CMakeLists.txt")
        if os.path.exists(cmake_file):
            print("   ✅ CMakeLists.txt found")
        else:
            print("   ❌ CMakeLists.txt not found")
            
        # Check for source files
        src_files = []
        for root, dirs, files in os.walk(project_path):
            src_files.extend([f for f in files if f.endswith(('.cpp', '.c'))])
        
        print(f"   📄 Source files found: {len(src_files)}")
        if src_files:
            for src_file in src_files[:5]:  # Show first 5
                print(f"      • {src_file}")
            if len(src_files) > 5:
                print(f"      • ... and {len(src_files) - 5} more")
    else:
        print("   ❌ Project directory not found")
        print(f"   💡 Expected at: {project_path}")
    
    print()
    print("📂 ORGANIZED TEST PROJECTS STRUCTURE:")
    
    test_projects_dir = os.path.join(script_dir, "TestProjects")
    if os.path.exists(test_projects_dir):
        print(f"   📁 TestProjects/ directory exists")
        
        for item in os.listdir(test_projects_dir):
            item_path = os.path.join(test_projects_dir, item)
            if os.path.isdir(item_path):
                print(f"      📂 {item}/")
                
                # Check for CMakeLists.txt in subdirectories
                for subitem in os.listdir(item_path):
                    subitem_path = os.path.join(item_path, subitem)
                    if os.path.isdir(subitem_path):
                        cmake_path = os.path.join(subitem_path, "CMakeLists.txt")
                        if os.path.exists(cmake_path):
                            print(f"         📄 {subitem}/ (has CMakeLists.txt)")
                        else:
                            print(f"         📁 {subitem}/")
    else:
        print("   ❌ TestProjects directory not found")
    
    print()
    print("🗂️ OUTPUT MANAGER TEST:")
    
    try:
        outputManager = OutputManager()
        print(f"   📂 Output Base: {outputManager.output_base_dir}")
        print(f"   📊 Coverage Dir: {outputManager.coverage_dir}")
        print(f"   🧪 Unit Tests Dir: {outputManager.get_unit_tests_dir()}")
        print(f"   📈 Coverage Data Dir: {outputManager.get_coverage_data_dir()}")
        print("   ✅ OutputManager initialized successfully")
        
        # Test directory preparation (dry run)
        print("   🧹 Testing output cleanup configuration...")
        if configReader.get_clean_output_before_run():
            print("   ✅ Output will be cleaned before each run")
        else:
            print("   📦 Output will be backed up before each run")
            
    except Exception as e:
        print(f"   ❌ OutputManager error: {e}")
    
    print()
    print("💡 CONFIGURATION TIPS:")
    print("   • Edit CppMicroAgent.cfg to change project path")
    print("   • Set clean_output_before_run=false to keep previous results")
    print("   • Adjust coverage_target and max_iterations as needed")
    print("   • Add new projects to TestProjects/ directory")
    
    print()
    print("🚀 READY TO RUN:")
    print("   python3 CppMicroAgent.py (choose option 3)")
    print("   python3 run_sample_coverage.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
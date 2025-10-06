#!/usr/bin/env python3
"""
Enhanced coverage report generator that provides detailed analysis
"""
import os
import sys
from Query import Query
from states_coverage.StateGenerateCoverageReport import StateGenerateCoverageReport
from states_coverage.StateParseCMake import StateParseCMake

def generate_detailed_tree_report():
    """Generate a detailed tree structure report"""
    output_dir = "output/UnitTestCoverage"
    
    if not os.path.exists(output_dir):
        return "No coverage data directory found."
    
    tree_report = "\nDETAILED DIRECTORY STRUCTURE\n" + "="*40 + "\n\n"
    
    def add_tree_item(path, prefix="", is_last=True):
        nonlocal tree_report
        if os.path.basename(path) == "coverage_report.txt":
            return
            
        name = os.path.basename(path)
        connector = "└── " if is_last else "├── "
        tree_report += f"{prefix}{connector}{name}\n"
        
        if os.path.isdir(path):
            items = sorted([item for item in os.listdir(path) 
                          if not item.startswith('.') and item != "coverage_report.txt"])
            for i, item in enumerate(items):
                item_path = os.path.join(path, item)
                is_last_item = (i == len(items) - 1)
                next_prefix = prefix + ("    " if is_last else "│   ")
                add_tree_item(item_path, next_prefix, is_last_item)
    
    tree_report += "UnitTestCoverage/\n"
    items = sorted([item for item in os.listdir(output_dir) 
                   if not item.startswith('.') and item != "coverage_report.txt"])
    
    for i, item in enumerate(items):
        item_path = os.path.join(output_dir, item)
        is_last_item = (i == len(items) - 1)
        add_tree_item(item_path, "", is_last_item)
    
    return tree_report

def main():
    print("🔍 Enhanced Coverage Report Generator")
    print("=" * 50)
    
    # Get the sample project path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_path = os.path.join(script_dir, "sampleCpp", "SampleApp")
    
    print(f"📁 Analyzing project: {sample_path}")
    
    try:
        # Create query and parse CMake
        query = Query(sample_path)
        
        print("🔍 Parsing CMakeLists.txt...")
        cmake_parser = StateParseCMake()
        proceed, query = cmake_parser.run(query)
        
        if not proceed:
            print("❌ Failed to parse CMakeLists.txt")
            return 1
        
        print("📊 Generating coverage report...")
        report_generator = StateGenerateCoverageReport()
        proceed, _ = report_generator.run(query)
        
        if proceed:
            # Generate detailed tree structure
            tree_structure = generate_detailed_tree_report()
            
            # Append tree structure to the existing report
            report_file = "output/UnitTestCoverage/coverage_report.txt"
            with open(report_file, 'a') as f:
                f.write(tree_structure)
            
            print("✅ Enhanced coverage report generated!")
            print(f"📂 Report location: {report_file}")
            print("\n📋 Report Summary:")
            
            # Show quick summary
            with open(report_file, 'r') as f:
                content = f.read()
                if "Total Source Files Discovered:" in content:
                    line = [l for l in content.split('\n') if "Total Source Files Discovered:" in l][0]
                    print(f"   {line.strip()}")
                if "Total Header Files Discovered:" in content:
                    line = [l for l in content.split('\n') if "Total Header Files Discovered:" in l][0]
                    print(f"   {line.strip()}")
                if "Mock Headers Generated:" in content:
                    line = [l for l in content.split('\n') if "📋 Mock Headers Generated:" in l][0]
                    print(f"   {line.strip()}")
            
            return 0
        else:
            print("❌ Failed to generate coverage report")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
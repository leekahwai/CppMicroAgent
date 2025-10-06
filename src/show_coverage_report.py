#!/usr/bin/env python3
"""
Simple script to display the coverage report
"""
import os
import sys

def main():
    report_file = "output/UnitTestCoverage/coverage_report.txt"
    
    if not os.path.exists(report_file):
        print("❌ Coverage report not found!")
        print(f"   Expected location: {report_file}")
        print("   Run the coverage analysis first.")
        return 1
    
    print("📊 C++ MICRO AGENT - COVERAGE REPORT")
    print("=" * 50)
    
    try:
        with open(report_file, 'r') as f:
            content = f.read()
            print(content)
        
        print("\n" + "=" * 50)
        print(f"📂 Full report saved at: {os.path.abspath(report_file)}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error reading report: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
EXECUTION GUIDE for C++ Micro Agent
"""

def main():
    print("🚀 C++ MICRO AGENT - EXECUTION GUIDE")
    print("=" * 50)
    print()
    
    print("✅ SINGLE COMMAND EXECUTION OPTIONS:")
    print()
    
    print("🎯 OPTION 1: Main Application (Recommended)")
    print("   Command: python3 CppMicroAgent.py")
    print("   Choose option 3 when prompted")
    print("   Result: Complete iterative coverage analysis")
    print()
    
    print("🎯 OPTION 2: Direct One-Click")
    print("   Command: python3 run_sample_coverage.py")
    print("   Result: Same complete analysis, no menu")
    print()
    
    print("🎯 OPTION 3: Ultra-Simple")
    print("   Command: python3 one_click_run.py")
    print("   Result: Automatically selects option 3 for you")
    print()
    
    print("📋 WHAT HAPPENS IN ONE EXECUTION:")
    print("   1️⃣  Parse CMake project → Find all source files")
    print("   2️⃣  Generate dependency mocks → LLM creates .h files")
    print("   3️⃣  Compile with coverage → Build instrumented version")
    print("   4️⃣  Generate unit tests → LLM creates comprehensive tests")
    print("   5️⃣  🔄 ITERATIVE LOOP:")
    print("       • Compile unit tests with main code")
    print("       • Measure coverage with gcov/lcov")
    print("       • If coverage < 80%: regenerate better tests")
    print("       • Repeat up to 3 iterations")
    print("   6️⃣  Generate reports → Text + HTML coverage reports")
    print()
    
    print("📂 ALL OUTPUT IN ONE PLACE:")
    print("   output/UnitTestCoverage/")
    print("   ├── unit_tests/           # Generated .cpp test files")
    print("   ├── coverage_data/        # Coverage analysis & HTML reports")
    print("   ├── [mocks]/             # LLM-generated dependency mocks")
    print("   └── coverage_report.txt  # Comprehensive results")
    print()
    
    print("⚡ NO MULTIPLE COMMANDS NEEDED!")
    print("   Everything happens in sequence automatically")
    print("   One execution → Complete analysis → Ready-to-use results")
    print()
    
    print("🔧 THE EXTRA SCRIPTS ARE JUST FOR:")
    print("   • show_coverage_report.py    → View results after completion")
    print("   • show_coverage_summary.py   → Quick status check") 
    print("   • show_iterative_features.py → Demo of what was built")
    print("   • test_iterative_coverage.py → Development testing")
    print()
    
    print("🏆 BOTTOM LINE:")
    print("   Run ONE command → Get complete iterative unit test generation")
    print("   with high coverage through intelligent LLM feedback!")

if __name__ == "__main__":
    main()
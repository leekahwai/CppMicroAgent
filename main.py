#!/usr/bin/env python3
"""
CppMicroAgent - Main Entry Point
================================

This is the main entry point for the C++ Micro Agent coverage improvement system.
All core modules are now organized in the src/ directory for better project structure.

Usage:
    python3 main.py           # Interactive mode
    python3 main.py --help    # Show help
    python3 main.py --quick   # Quick one-click analysis
    python3 main.py --multi   # Multi-project analysis

Features:
    ✅ Cross-platform compatibility (Linux/Windows)
    ✅ Advanced coverage improvement with ML enhancement
    ✅ Multi-project batch analysis
    ✅ Intelligent iterative test generation
    ✅ Comprehensive reporting and visualization
"""

import sys
import os
import argparse

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def show_banner():
    """Display the application banner"""
    print("🚀 C++ MICRO AGENT - ADVANCED COVERAGE SYSTEM")
    print("=" * 60)
    print("🎯 Intelligent Coverage Improvement with ML Enhancement")
    print("📊 Multi-Project Analysis & Comprehensive Reporting")
    print("🔄 Iterative Test Generation & Gap Analysis")
    print("=" * 60)

def show_menu():
    """Display the main menu options"""
    print("\n📋 MAIN MENU:")
    print("1. 🎯 Complete Coverage Analysis (Recommended)")
    print("2. 📊 Multi-Project Batch Analysis")
    print("3. ⚡ Quick Sample Analysis")
    print("4. 📈 View Coverage Reports")
    print("5. 🔧 Configuration & Settings")
    print("6. ❌ Exit")
    print("-" * 40)

def run_complete_analysis():
    """Run complete coverage analysis"""
    print("🔄 Starting Complete Coverage Analysis...")
    try:
        from src.states_coverage.StateMachine import StateMachine
        from src.ConfigReader import ConfigReader
        from src.Query import Query
        
        configReader = ConfigReader()
        project_path = os.path.join(os.getcwd(), configReader.get_default_project_path())
        
        print(f"\n🔄 C++ MICRO AGENT - COMPLETE COVERAGE ANALYSIS")
        print("=" * 60)
        print(f"📁 Project: {project_path}")
        print(f"🎯 Target: Generate unit tests with {configReader.get_coverage_target()}%+ coverage")
        print(f"🔄 Max Iterations: {configReader.get_max_iterations()}")
        print("🔄 Method: Iterative improvement with LLM feedback")
        print(f"🧹 Clean Output: {'Yes' if configReader.get_clean_output_before_run() else 'No (backup mode)'}")
        print("-" * 60)
        
        # Check if project exists
        cmake_file = os.path.join(project_path, "CMakeLists.txt")
        if not os.path.exists(cmake_file):
            print(f"❌ Error: CMakeLists.txt not found at {cmake_file}")
            print(f"💡 Update the 'default_project_path' in CppMicroAgent.cfg")
            print(f"   Current setting: {configReader.get_default_project_path()}")
            return
        
        query = Query(project_path)
        sm = StateMachine(query)
        sm.run()
        
        # Show results summary
        print("\n" + "=" * 60)
        print("✅ COMPLETE COVERAGE ANALYSIS FINISHED!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Please ensure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_multi_project():
    """Run multi-project analysis"""
    print("📊 Starting Multi-Project Analysis...")
    try:
        from src.quick_multi_analysis import main as run_multi
        run_multi()
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Multi-project analysis module not available")
    except Exception as e:
        print(f"❌ Error: {e}")

def run_quick_analysis():
    """Run quick analysis"""
    print("⚡ Starting Quick Analysis...")
    run_complete_analysis()  # Use the same complete analysis since one_click_run.py was removed

def view_reports():
    """View existing reports"""
    print("📈 Viewing Coverage Reports...")
    if os.path.exists("output"):
        import subprocess
        subprocess.run([sys.executable, "-c", """
import os
if os.path.exists('output'):
    print('📁 Available Reports:')
    for root, dirs, files in os.walk('output'):
        level = root.replace('output', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}📁 {os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            if file.endswith(('.txt', '.html', '.md')):
                print(f'{subindent}📄 {file}')
else:
    print('❌ No reports found. Run an analysis first.')
"""])
    else:
        print("❌ No reports found. Run an analysis first.")

def show_configuration():
    """Show configuration options"""
    print("🔧 Configuration & Settings...")
    try:
        from src.ConfigReader import ConfigReader
        config = ConfigReader()
        print("\n📋 Current Configuration:")
        print(f"   🎯 Target Coverage: {config.get_coverage_target()}%")
        print(f"   🔄 Max Iterations: {config.get_max_iterations()}")
        print(f"   📁 Default Project: {config.get_default_project_path()}")
        print("\n💡 To modify settings, edit: CppMicroAgent.cfg")
    except Exception as e:
        print(f"❌ Error loading configuration: {e}")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description="C++ Micro Agent - Advanced Coverage Improvement System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 main.py              # Interactive mode
    python3 main.py --quick      # Quick one-click analysis
    python3 main.py --multi      # Multi-project analysis
    python3 main.py --reports    # View existing reports
        """
    )
    
    parser.add_argument('--quick', action='store_true', 
                       help='Run quick one-click analysis')
    parser.add_argument('--multi', action='store_true',
                       help='Run multi-project analysis')
    parser.add_argument('--reports', action='store_true',
                       help='View existing coverage reports')
    parser.add_argument('--config', action='store_true',
                       help='Show configuration settings')
    
    args = parser.parse_args()
    
    show_banner()
    
    # Handle command line arguments
    if args.quick:
        run_quick_analysis()
        return
    elif args.multi:
        run_multi_project()
        return
    elif args.reports:
        view_reports()
        return
    elif args.config:
        show_configuration()
        return
    
    # Interactive mode
    while True:
        show_menu()
        try:
            choice = input("🔸 Select option (1-6): ").strip()
            
            if choice == '1':
                run_complete_analysis()
            elif choice == '2':
                run_multi_project()
            elif choice == '3':
                run_quick_analysis()
            elif choice == '4':
                view_reports()
            elif choice == '5':
                show_configuration()
            elif choice == '6':
                print("👋 Thank you for using C++ Micro Agent!")
                break
            else:
                print("❌ Invalid option. Please select 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
        
        input("\n⏳ Press Enter to continue...")

if __name__ == "__main__":
    main()
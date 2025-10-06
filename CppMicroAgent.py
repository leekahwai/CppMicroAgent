import sys
import threading
import time
from States.StateMachine import StateMachine
from States_Coverage.StateMachine import StateMachine as StateMachineCoverage
from States.Query import Query
import flaskApp


def animate(stop_event):
    icon_frames = [ "🟢 LKW  ", "🟡 NWBNB", "🟠 LKW  ", "🔴 NWBNB", "🟠 LKW  ", "🟡 NWBNB"]  # A simple cycling icon
    index = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rListening: {icon_frames[index]} ")  # Overwrites the same line
        sys.stdout.flush()
        index = (index + 1) % len(icon_frames)
        time.sleep(0.2)

def listen_for_input(stop_event):
    try:
        print("\n")  # Ensure input appears on a new line
        stop_event.set()  # Temporarily stop animation while user types
            

        print ("Select the following choices:")
        print ("1. Generate code from input")
        print ("2. Generate unit tests from folder")
        print ("3. 🔄 Complete Coverage Analysis (Recommended)")
        print ("    → Parse project → Generate mocks → Create unit tests")
        print ("    → Iterative coverage improvement → Final report")
        my_input = input ("Enter your choice (1, 2, or 3): ")
        if my_input == "1":
            user_input = input(" Key in your code generation query > ")  # User input prompt
            print(f"\nYou entered: {user_input}\n")  # Ensure input is visible
            query = Query(user_input)
            
            sm = StateMachine(query)
            sm.run()
        elif my_input == "2":
            user_input = input(" Key in location of CMakeLists.txt > ")  # User input prompt
            print(f"\nYou entered: {user_input}\n")  # Ensure input is visible
            query = Query(user_input)
            
            sm = StateMachineCoverage(query)
            sm.run()
        elif my_input == "3":
            # Complete iterative coverage analysis workflow
            import os
            from ConfigReader import ConfigReader
            
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
            sm = StateMachineCoverage(query)
            sm.run()
            
            # Show results summary
            print("\n" + "=" * 60)
            print("✅ COMPLETE COVERAGE ANALYSIS FINISHED!")
            print("=" * 60)
            
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
                    print("🏆 SUCCESS: High-quality unit tests generated!")
                else:
                    print("🔄 PARTIAL: Some coverage improvement achieved")
            
            print("\n📂 Generated Files:")
            output_dir = configReader.get_output_directory()
            coverage_dir = os.path.join(output_dir, "UnitTestCoverage")
            
            # Unit tests
            unit_tests_dir = os.path.join(coverage_dir, "unit_tests")
            if os.path.exists(unit_tests_dir):
                test_files = [f for f in os.listdir(unit_tests_dir) if f.endswith('.cpp')]
                print(f"   🧪 Unit Tests: {len(test_files)} files in {unit_tests_dir}/")
                for test_file in sorted(test_files):
                    print(f"      • {test_file}")
            
            # Coverage reports
            if os.path.exists(os.path.join(coverage_dir, "coverage_data")):
                print(f"   📊 Coverage Data: {coverage_dir}/coverage_data/")
                if os.path.exists(os.path.join(coverage_dir, "coverage_data", "lcov_html")):
                    html_path = os.path.join(coverage_dir, "coverage_data", "lcov_html", "index.html")
                    print(f"      🌐 HTML Report: {html_path}")
            
            # Text report
            report_file = os.path.join(coverage_dir, "coverage_report.txt")
            if os.path.exists(report_file):
                print(f"   📄 Full Report: {report_file}")
            
            print("\n💡 Quick Commands:")
            print("   python3 show_coverage_report.py     # View full text report")
            print("   python3 show_coverage_summary.py    # Quick coverage summary")
            
        else:
            print("Invalid choice.")

        stop_event.clear()  # Resume animation
           
        
            
        

    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        stop_event.set()
        sys.exit(0)

if __name__ == "__main__":
    stop_event = threading.Event()
    
    # Start animation in a separate thread
    animation_thread = threading.Thread(target=animate, args=(stop_event,), daemon=True)
    animation_thread.start()
    
    # Give some time for animation to be visible before input appears
    flaskApp.start()
     
    time.sleep(1.0)
    # Start listening for input
    listen_for_input(stop_event)

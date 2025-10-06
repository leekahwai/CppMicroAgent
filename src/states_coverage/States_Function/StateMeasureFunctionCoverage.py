"""
StateMeasureFunctionCoverage - Measure coverage for a specific function test
"""

from flow_manager import flow
from ConfigReader import ConfigReader
import os
import subprocess
import json

class StateMeasureFunctionCoverage():
    def __init__(self):
        self.configReader = ConfigReader()
        print("Initializing [States_Function::StateMeasureFunctionCoverage]")

    def run(self, input_data):
        flow.transition("States_Function::StateMeasureFunctionCoverage")
        print("[StateMeasureFunctionCoverage] Measuring function coverage...")

        output_folder = input_data.get_current_output_folder()
        executable = input_data.get_generated_ut_file()
        
        if not executable or not os.path.exists(executable):
            print("[StateMeasureFunctionCoverage] No executable found!")
            return False, input_data
        
        build_dir = os.path.join(output_folder, "build")
        
        # Step 1: Run the test executable to generate .gcda files
        success = self._run_test_executable(executable, build_dir)
        
        if not success:
            print("[StateMeasureFunctionCoverage] Test execution failed")
            return False, input_data
        
        # Step 2: Generate coverage data using gcov
        coverage_data = self._generate_coverage_data(build_dir, input_data)
        
        # Step 3: Generate HTML coverage report
        self._generate_html_report(build_dir, coverage_data)
        
        # Step 4: Save coverage summary to file
        self._save_coverage_summary(output_folder, coverage_data)
        
        # Store coverage data for aggregation later
        input_data.set_coverage_data(coverage_data)
        
        print(f"[StateMeasureFunctionCoverage] ✅ Coverage: {coverage_data.get('coverage_percentage', 0):.1f}%")
        
        return True, input_data

    def _run_test_executable(self, executable, build_dir):
        """Run the test executable to generate coverage data"""
        
        print(f"[StateMeasureFunctionCoverage] Running test: {executable}")
        
        try:
            result = subprocess.run(
                [executable],
                cwd=build_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            print("[StateMeasureFunctionCoverage] Test output:")
            print(result.stdout)
            
            if result.returncode != 0:
                print(f"[StateMeasureFunctionCoverage] Test failed with return code: {result.returncode}")
                print(f"Error output: {result.stderr}")
                # Still continue - we want coverage even if tests fail
            
            return True
            
        except subprocess.TimeoutExpired:
            print("[StateMeasureFunctionCoverage] Test execution timed out")
            return False
        except Exception as e:
            print(f"[StateMeasureFunctionCoverage] Error running test: {e}")
            return False

    def _generate_coverage_data(self, build_dir, input_data):
        """Generate coverage data using gcov"""
        
        coverage_data = {
            "coverage_percentage": 0.0,
            "lines_covered": 0,
            "lines_total": 0,
            "functions_covered": 0,
            "functions_total": 0,
            "gcov_files": [],
            "build_dir": build_dir
        }
        
        try:
            # Find .gcda files
            gcda_files = []
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    if file.endswith('.gcda'):
                        gcda_files.append(os.path.join(root, file))
            
            if not gcda_files:
                print("[StateMeasureFunctionCoverage] No .gcda files found")
                return coverage_data
            
            print(f"[StateMeasureFunctionCoverage] Found {len(gcda_files)} .gcda files")
            
            # Run gcov
            gcov_cmd = [self.configReader.get_gcov_tool(), "-b", "-c"] + gcda_files
            result = subprocess.run(
                gcov_cmd,
                cwd=build_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                # Parse gcov output
                self._parse_gcov_output(result.stdout, coverage_data)
                
                # Find generated .gcov files
                gcov_files = []
                for root, dirs, files in os.walk(build_dir):
                    for file in files:
                        if file.endswith('.gcov'):
                            gcov_path = os.path.join(root, file)
                            gcov_files.append(gcov_path)
                            # Parse each .gcov file for detailed coverage
                            self._parse_gcov_file(gcov_path, coverage_data)
                
                coverage_data["gcov_files"] = gcov_files
                print(f"[StateMeasureFunctionCoverage] Generated {len(gcov_files)} .gcov files")
            else:
                print(f"[StateMeasureFunctionCoverage] gcov failed: {result.stderr}")
            
        except Exception as e:
            print(f"[StateMeasureFunctionCoverage] Error generating coverage: {e}")
        
        return coverage_data

    def _parse_gcov_output(self, gcov_output, coverage_data):
        """Parse gcov output for coverage percentage"""
        
        lines = gcov_output.split('\n')
        for line in lines:
            if 'Lines executed:' in line:
                parts = line.split()
                for part in parts:
                    if part.endswith('%'):
                        try:
                            coverage_data["coverage_percentage"] = float(part[:-1])
                        except:
                            pass

    def _parse_gcov_file(self, gcov_file, coverage_data):
        """Parse individual .gcov file for detailed coverage info"""
        
        try:
            with open(gcov_file, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        execution_count = parts[0].strip()
                        line_num = parts[1].strip()
                        code = parts[2].strip()
                        
                        # Skip empty lines and comments
                        if not code or code.startswith('//') or code.startswith('/*'):
                            continue
                        
                        if execution_count == '#####':
                            # Uncovered line
                            coverage_data["lines_total"] += 1
                        elif execution_count.replace('-', '').isdigit():
                            count = int(execution_count.replace('-', ''))
                            if count > 0:
                                # Covered line
                                coverage_data["lines_covered"] += 1
                                coverage_data["lines_total"] += 1
            
            # Recalculate percentage
            if coverage_data["lines_total"] > 0:
                coverage_data["coverage_percentage"] = (
                    coverage_data["lines_covered"] / coverage_data["lines_total"] * 100
                )
        
        except Exception as e:
            print(f"[StateMeasureFunctionCoverage] Error parsing {gcov_file}: {e}")

    def _generate_html_report(self, build_dir, coverage_data):
        """Generate HTML coverage report using lcov"""
        
        try:
            lcov_file = os.path.join(build_dir, "coverage.info")
            html_dir = os.path.join(build_dir, "coverage_html")
            
            # Run lcov to capture coverage
            lcov_cmd = [
                self.configReader.get_lcov_tool(),
                "--capture",
                "--directory", build_dir,
                "--output-file", lcov_file,
                "--ignore-errors", "gcov,source"
            ]
            
            result = subprocess.run(lcov_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Generate HTML report
                genhtml_cmd = [
                    "genhtml",
                    lcov_file,
                    "--output-directory", html_dir
                ]
                
                result = subprocess.run(genhtml_cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    coverage_data["html_report"] = html_dir
                    print(f"[StateMeasureFunctionCoverage] HTML report: {html_dir}/index.html")
        
        except Exception as e:
            print(f"[StateMeasureFunctionCoverage] Error generating HTML report: {e}")

    def _save_coverage_summary(self, output_folder, coverage_data):
        """Save coverage summary to a text file"""
        
        summary_file = os.path.join(output_folder, "coverage_summary.txt")
        
        try:
            with open(summary_file, 'w') as f:
                f.write("=" * 60 + "\n")
                f.write("FUNCTION COVERAGE SUMMARY\n")
                f.write("=" * 60 + "\n\n")
                f.write(f"Coverage Percentage: {coverage_data.get('coverage_percentage', 0):.1f}%\n")
                f.write(f"Lines Covered: {coverage_data.get('lines_covered', 0)}\n")
                f.write(f"Total Lines: {coverage_data.get('lines_total', 0)}\n")
                f.write(f"Functions Covered: {coverage_data.get('functions_covered', 0)}\n")
                f.write(f"Total Functions: {coverage_data.get('functions_total', 0)}\n\n")
                
                if coverage_data.get("gcov_files"):
                    f.write("Generated Coverage Files:\n")
                    for gcov_file in coverage_data["gcov_files"]:
                        f.write(f"  - {os.path.basename(gcov_file)}\n")
                
                if coverage_data.get("html_report"):
                    f.write(f"\nHTML Report: {coverage_data['html_report']}/index.html\n")
                
                f.write("\n" + "=" * 60 + "\n")
            
            print(f"[StateMeasureFunctionCoverage] Coverage summary saved: {summary_file}")
            
        except Exception as e:
            print(f"[StateMeasureFunctionCoverage] Error saving summary: {e}")

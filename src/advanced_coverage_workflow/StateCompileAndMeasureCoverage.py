import os
import subprocess
import tempfile
import shutil
from ..flow_manager import flow
from ..ConfigReader import ConfigReader

class StateCompileAndMeasureCoverage():
    def __init__(self):
        self.configReader = ConfigReader()
        print("Initializing [StateCompileAndMeasureCoverage]")

    def run(self, input_data):
        flow.transition("StateCompileAndMeasureCoverage")
        print("[StateCompileAndMeasureCoverage] Compiling with coverage instrumentation...")
        
        cmake_dir = input_data.get_input_data()
        output_dir = "output/UnitTestCoverage"
        coverage_dir = os.path.join(output_dir, "coverage_data")
        
        # Create coverage data directory
        os.makedirs(coverage_dir, exist_ok=True)
        
        try:
            # Compile with coverage
            success = self._compile_with_coverage(cmake_dir, coverage_dir, input_data)
            if not success:
                print("[StateCompileAndMeasureCoverage] Compilation failed, continuing without coverage data")
                input_data.set_coverage_data({"error": "Compilation failed"})
                return True, input_data  # Continue anyway
            
            # Run coverage analysis
            coverage_results = self._run_coverage_analysis(coverage_dir)
            input_data.set_coverage_data(coverage_results)
            
            print("[StateCompileAndMeasureCoverage] Coverage analysis completed")
            return True, input_data
            
        except Exception as e:
            print(f"[StateCompileAndMeasureCoverage] Error: {e}")
            input_data.set_coverage_data({"error": str(e)})
            return True, input_data  # Continue anyway

    def _compile_with_coverage(self, cmake_dir, coverage_dir, input_data):
        """Compile the project with coverage instrumentation"""
        
        # Create a temporary build directory
        build_dir = os.path.join(coverage_dir, "build")
        os.makedirs(build_dir, exist_ok=True)
        
        try:
            # Configure with CMake including coverage flags
            cmake_cmd = [
                "cmake",
                "-DCMAKE_BUILD_TYPE=Debug",
                "-DCMAKE_CXX_FLAGS=--coverage -g -O0",
                "-DCMAKE_C_FLAGS=--coverage -g -O0",
                "-DCMAKE_EXE_LINKER_FLAGS=--coverage",
                cmake_dir
            ]
            
            print(f"[StateCompileAndMeasureCoverage] Configuring: {' '.join(cmake_cmd)}")
            result = subprocess.run(cmake_cmd, cwd=build_dir, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[StateCompileAndMeasureCoverage] CMake configure failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
            
            # Build the project
            build_cmd = ["make", "-j4"]
            print(f"[StateCompileAndMeasureCoverage] Building: {' '.join(build_cmd)}")
            result = subprocess.run(build_cmd, cwd=build_dir, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"[StateCompileAndMeasureCoverage] Build failed:")
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                return False
            
            print("[StateCompileAndMeasureCoverage] Build successful")
            return True
            
        except Exception as e:
            print(f"[StateCompileAndMeasureCoverage] Compilation error: {e}")
            return False

    def _run_coverage_analysis(self, coverage_dir):
        """Run gcov and lcov to generate coverage data"""
        
        build_dir = os.path.join(coverage_dir, "build")
        coverage_results = {
            "build_dir": build_dir,
            "gcov_files": [],
            "lcov_summary": {},
            "coverage_percentage": 0.0,
            "lines_covered": 0,
            "lines_total": 0,
            "functions_covered": 0,
            "functions_total": 0
        }
        
        try:
            # Find .gcno files (generated during compilation)
            gcno_files = []
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    if file.endswith('.gcno'):
                        gcno_files.append(os.path.join(root, file))
            
            if not gcno_files:
                print("[StateCompileAndMeasureCoverage] No .gcno files found - coverage instrumentation may have failed")
                return coverage_results
            
            print(f"[StateCompileAndMeasureCoverage] Found {len(gcno_files)} .gcno files")
            
            # Try to run the executable to generate .gcda files
            executable_path = os.path.join(build_dir, "SampleApp")
            if os.path.exists(executable_path):
                print("[StateCompileAndMeasureCoverage] Running executable to generate coverage data...")
                try:
                    # Run with timeout to prevent hanging
                    result = subprocess.run([executable_path], 
                                          cwd=build_dir, 
                                          capture_output=True, 
                                          text=True, 
                                          timeout=10)
                    print(f"[StateCompileAndMeasureCoverage] Execution completed with return code: {result.returncode}")
                except subprocess.TimeoutExpired:
                    print("[StateCompileAndMeasureCoverage] Execution timed out (normal for interactive programs)")
                except Exception as e:
                    print(f"[StateCompileAndMeasureCoverage] Execution error: {e}")
            
            # Run gcov on source files
            self._run_gcov_analysis(build_dir, coverage_results)
            
            # Run lcov if available
            self._run_lcov_analysis(build_dir, coverage_dir, coverage_results)
            
            return coverage_results
            
        except Exception as e:
            print(f"[StateCompileAndMeasureCoverage] Coverage analysis error: {e}")
            coverage_results["error"] = str(e)
            return coverage_results

    def _run_gcov_analysis(self, build_dir, coverage_results):
        """Run gcov on source files"""
        
        try:
            # Find .gcda files
            gcda_files = []
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    if file.endswith('.gcda'):
                        gcda_files.append(os.path.join(root, file))
            
            if not gcda_files:
                print("[StateCompileAndMeasureCoverage] No .gcda files found - program may not have run")
                return
            
            print(f"[StateCompileAndMeasureCoverage] Found {len(gcda_files)} .gcda files")
            
            # Run gcov
            gcov_cmd = [self.configReader.get_gcov_tool(), "-b", "-c"] + gcda_files
            result = subprocess.run(gcov_cmd, cwd=build_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                coverage_results["gcov_output"] = result.stdout
                
                # Parse gcov output for basic statistics
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'Lines executed:' in line:
                        # Extract percentage
                        parts = line.split()
                        for i, part in enumerate(parts):
                            if part.endswith('%'):
                                try:
                                    coverage_results["coverage_percentage"] = float(part[:-1])
                                except:
                                    pass
                
                # Find generated .gcov files
                gcov_files = []
                for root, dirs, files in os.walk(build_dir):
                    for file in files:
                        if file.endswith('.gcov'):
                            gcov_files.append(os.path.join(root, file))
                
                coverage_results["gcov_files"] = gcov_files
                print(f"[StateCompileAndMeasureCoverage] Generated {len(gcov_files)} .gcov files")
            else:
                print(f"[StateCompileAndMeasureCoverage] gcov failed: {result.stderr}")
                
        except Exception as e:
            print(f"[StateCompileAndMeasureCoverage] gcov error: {e}")

    def _run_lcov_analysis(self, build_dir, coverage_dir, coverage_results):
        """Run lcov to generate detailed coverage report"""
        
        try:
            lcov_output_dir = os.path.join(coverage_dir, "lcov_html")
            os.makedirs(lcov_output_dir, exist_ok=True)
            
            # Generate lcov data file
            lcov_data_file = os.path.join(coverage_dir, "coverage.info")
            
            # Capture coverage data
            lcov_cmd = [
                self.configReader.get_lcov_tool(),
                "--capture",
                "--directory", build_dir,
                "--output-file", lcov_data_file
            ]
            
            result = subprocess.run(lcov_cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("[StateCompileAndMeasureCoverage] lcov data capture successful")
                
                # Generate HTML report
                genhtml_cmd = [
                    "genhtml",
                    lcov_data_file,
                    "--output-directory", lcov_output_dir
                ]
                
                result = subprocess.run(genhtml_cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"[StateCompileAndMeasureCoverage] HTML report generated at: {lcov_output_dir}")
                    coverage_results["lcov_html_dir"] = lcov_output_dir
                
                # Parse lcov summary
                self._parse_lcov_summary(lcov_data_file, coverage_results)
                
            else:
                print(f"[StateCompileAndMeasureCoverage] lcov failed: {result.stderr}")
                
        except Exception as e:
            print(f"[StateCompileAndMeasureCoverage] lcov error: {e}")

    def _parse_lcov_summary(self, lcov_data_file, coverage_results):
        """Parse lcov data file for summary statistics"""
        
        try:
            if not os.path.exists(lcov_data_file):
                return
            
            with open(lcov_data_file, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            current_file = None
            
            for line in lines:
                if line.startswith('SF:'):  # Source file
                    current_file = line[3:]
                elif line.startswith('LH:'):  # Lines hit
                    coverage_results["lines_covered"] += int(line[3:])
                elif line.startswith('LF:'):  # Lines found
                    coverage_results["lines_total"] += int(line[3:])
                elif line.startswith('FNH:'):  # Functions hit
                    coverage_results["functions_covered"] += int(line[4:])
                elif line.startswith('FNF:'):  # Functions found
                    coverage_results["functions_total"] += int(line[4:])
            
            # Calculate overall coverage percentage
            if coverage_results["lines_total"] > 0:
                coverage_results["coverage_percentage"] = (
                    coverage_results["lines_covered"] / coverage_results["lines_total"] * 100
                )
            
            print(f"[StateCompileAndMeasureCoverage] Coverage Summary:")
            print(f"  Lines: {coverage_results['lines_covered']}/{coverage_results['lines_total']} "
                  f"({coverage_results['coverage_percentage']:.1f}%)")
            print(f"  Functions: {coverage_results['functions_covered']}/{coverage_results['functions_total']}")
                
        except Exception as e:
            print(f"[StateCompileAndMeasureCoverage] Error parsing lcov summary: {e}")
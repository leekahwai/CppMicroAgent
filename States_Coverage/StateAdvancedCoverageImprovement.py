import os
import subprocess
import shutil
from flow_manager import flow
from ConfigReader import ConfigReader
from CoverageImprovementEngine import CoverageImprovementEngine

class StateAdvancedCoverageImprovement():
    def __init__(self):
        self.configReader = ConfigReader()
        self.max_iterations = self.configReader.get_max_iterations()
        self.target_coverage = self.configReader.get_coverage_target()
        self.improvement_engine = CoverageImprovementEngine()
        print("Initializing [StateAdvancedCoverageImprovement]")
        print(f"[StateAdvancedCoverageImprovement] Target coverage: {self.target_coverage}%")
        print(f"[StateAdvancedCoverageImprovement] Max iterations: {self.max_iterations}")

    def run(self, input_data):
        flow.transition("StateAdvancedCoverageImprovement")
        print("[StateAdvancedCoverageImprovement] Starting advanced coverage improvement...")
        
        iteration = 1
        current_coverage = 0.0
        improvement_history = []
        
        while iteration <= self.max_iterations:
            print(f"\n{'='*70}")
            print(f"ADVANCED ITERATION {iteration}/{self.max_iterations}")
            print(f"Target Coverage: {self.target_coverage}%")
            print(f"Current Coverage: {current_coverage:.1f}%")
            print(f"{'='*70}")
            
            # Step 1: Compile and measure current coverage
            success, coverage_data = self._compile_and_measure_coverage(input_data)
            
            if not success:
                print(f"[StateAdvancedCoverageImprovement] Compilation failed in iteration {iteration}")
                break
            
            current_coverage = coverage_data.get("coverage_percentage", 0.0)
            input_data.set_coverage_data(coverage_data)
            
            print(f"[StateAdvancedCoverageImprovement] Iteration {iteration} coverage: {current_coverage:.1f}%")
            
            # Step 2: Advanced coverage gap analysis
            source_files = input_data.get_source_files()
            project_path = input_data.get_input_data()
            
            improvement_analysis = self._run_advanced_analysis(
                coverage_data, source_files, project_path, iteration
            )
            
            # Track improvement history
            improvement_history.append({
                "iteration": iteration,
                "coverage": current_coverage,
                "improvements_found": improvement_analysis.get("total_improvements", 0),
                "strategies_applied": list(improvement_analysis.get("strategy_results", {}).keys())
            })
            
            # Step 3: Check if target achieved
            if current_coverage >= self.target_coverage:
                print(f"✅ Target coverage of {self.target_coverage}% achieved!")
                break
            
            # Step 4: If not last iteration, apply intelligent improvements
            if iteration < self.max_iterations:
                print(f"[StateAdvancedCoverageImprovement] Applying intelligent improvements...")
                
                # Generate and apply improvements
                self._apply_intelligent_improvements(
                    input_data, improvement_analysis, iteration
                )
                
                # Also regenerate tests with enhanced prompts
                self._regenerate_enhanced_tests(input_data, coverage_data, iteration)
            
            iteration += 1
        
        # Store final results with improvement history
        input_data.set_coverage_iteration_results({
            "final_coverage": current_coverage,
            "iterations_completed": iteration - 1,
            "target_achieved": current_coverage >= self.target_coverage,
            "target_coverage": self.target_coverage,
            "improvement_method": "advanced_intelligent_analysis",
            "improvement_history": improvement_history,
            "total_improvements_applied": sum(h.get("improvements_found", 0) for h in improvement_history)
        })
        
        print(f"\n[StateAdvancedCoverageImprovement] Advanced improvement completed after {iteration-1} iterations")
        print(f"Final coverage: {current_coverage:.1f}%")
        print(f"Total improvements applied: {sum(h.get('improvements_found', 0) for h in improvement_history)}")
        
        return True, input_data

    def _compile_and_measure_coverage(self, input_data):
        """Compile unit tests with main project and measure coverage"""
        
        cmake_dir = input_data.get_input_data()
        output_dir = "output/UnitTestCoverage"
        coverage_dir = os.path.join(output_dir, "coverage_data")
        unit_tests_dir = os.path.join(output_dir, "unit_tests")
        
        # Create temporary build directory for this iteration
        build_dir = os.path.join(coverage_dir, "build_advanced")
        if os.path.exists(build_dir):
            shutil.rmtree(build_dir)
        os.makedirs(build_dir, exist_ok=True)
        
        try:
            # Create enhanced CMakeLists.txt with additional coverage flags
            self._create_enhanced_cmake_file(cmake_dir, unit_tests_dir, build_dir)
            
            # Configure with enhanced coverage options
            cmake_cmd = [
                "cmake",
                "-DCMAKE_BUILD_TYPE=Debug",
                "-DCMAKE_CXX_FLAGS=--coverage -g -O0 -fprofile-arcs -ftest-coverage -fno-inline",
                "-DCMAKE_C_FLAGS=--coverage -g -O0 -fprofile-arcs -ftest-coverage -fno-inline", 
                "-DCMAKE_EXE_LINKER_FLAGS=--coverage",
                "."
            ]
            
            result = subprocess.run(cmake_cmd, cwd=build_dir, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[StateAdvancedCoverageImprovement] CMake failed: {result.stderr}")
                return False, {}
            
            # Build with verbose output for better diagnostics
            build_cmd = ["make", "-j4", "VERBOSE=1"]
            result = subprocess.run(build_cmd, cwd=build_dir, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[StateAdvancedCoverageImprovement] Build failed: {result.stderr}")
                return False, {}
            
            # Run unit tests with detailed output
            test_executable = os.path.join(build_dir, "run_tests")
            if os.path.exists(test_executable):
                print("[StateAdvancedCoverageImprovement] Running unit tests with detailed coverage...")
                result = subprocess.run([test_executable, "--gtest_output=xml:test_results.xml"], 
                                      cwd=build_dir, capture_output=True, text=True)
                print(f"[StateAdvancedCoverageImprovement] Tests completed with code: {result.returncode}")
            
            # Enhanced coverage measurement
            coverage_data = self._measure_enhanced_coverage(build_dir)
            coverage_data["build_dir"] = build_dir
            
            return True, coverage_data
            
        except Exception as e:
            print(f"[StateAdvancedCoverageImprovement] Error in compilation: {e}")
            return False, {}

    def _create_enhanced_cmake_file(self, original_cmake_dir, unit_tests_dir, build_dir):
        """Create enhanced CMakeLists.txt with better coverage instrumentation"""
        
        cmake_content = f"""
cmake_minimum_required(VERSION 3.8)
project(AdvancedTestProject)

# Enhanced C++ standard and compiler options
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(PkgConfig REQUIRED)
find_package(GTest REQUIRED)
include_directories(${{GTEST_INCLUDE_DIRS}})

# Enhanced coverage flags
set(COVERAGE_FLAGS "--coverage -g -O0 -fprofile-arcs -ftest-coverage -fno-inline -fno-inline-small-functions -fno-default-inline")

# Include original project directories
include_directories("{original_cmake_dir}")
include_directories("{original_cmake_dir}/inc")
include_directories("{original_cmake_dir}/src/Program")
include_directories("{original_cmake_dir}/src/ProgramApp")
include_directories("{original_cmake_dir}/src/InterfaceA")
include_directories("{original_cmake_dir}/src/InterfaceB")

# Add original source files (excluding main)
set(ORIGINAL_SOURCES
    "{original_cmake_dir}/src/Program/Program.cpp"
    "{original_cmake_dir}/src/ProgramApp/ProgramApp.cpp"
    "{original_cmake_dir}/src/InterfaceA/InterfaceA.cpp"
    "{original_cmake_dir}/src/InterfaceA/IntfA_rx.cpp"
    "{original_cmake_dir}/src/InterfaceA/IntfA_tx.cpp"
    "{original_cmake_dir}/src/InterfaceB/InterfaceB.cpp"
    "{original_cmake_dir}/src/InterfaceB/IntfB_rx.cpp"
    "{original_cmake_dir}/src/InterfaceB/IntfB_tx.cpp"
)

# Add all unit test files
file(GLOB TEST_SOURCES "{unit_tests_dir}/*.cpp")

# Create test executable with enhanced coverage
add_executable(run_tests ${{ORIGINAL_SOURCES}} ${{TEST_SOURCES}})

# Link libraries
target_link_libraries(run_tests ${{GTEST_LIBRARIES}} pthread)

# Apply enhanced coverage flags
target_compile_options(run_tests PRIVATE ${{COVERAGE_FLAGS}})
target_link_libraries(run_tests --coverage)

# Enable testing
enable_testing()
add_test(NAME unit_tests COMMAND run_tests)
"""
        
        cmake_file_path = os.path.join(build_dir, "CMakeLists.txt")
        with open(cmake_file_path, 'w') as f:
            f.write(cmake_content)

    def _measure_enhanced_coverage(self, build_dir):
        """Enhanced coverage measurement with detailed analysis"""
        
        coverage_data = {
            "coverage_percentage": 0.0,
            "lines_covered": 0,
            "lines_total": 0,
            "functions_covered": 0,
            "functions_total": 0,
            "branch_coverage": 0.0,
            "gcov_files": [],
            "uncovered_lines": [],
            "uncovered_functions": []
        }
        
        try:
            # Run gcov with branch coverage analysis
            gcda_files = []
            for root, dirs, files in os.walk(build_dir):
                for file in files:
                    if file.endswith('.gcda'):
                        gcda_files.append(os.path.join(root, file))
            
            if not gcda_files:
                print("[StateAdvancedCoverageImprovement] No .gcda files found")
                return coverage_data
            
            # Enhanced gcov with branch coverage
            gcov_cmd = [self.configReader.get_gcov_tool(), "-b", "-c", "-u"] + gcda_files
            result = subprocess.run(gcov_cmd, cwd=build_dir, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Parse enhanced gcov output
                self._parse_enhanced_gcov_output(result.stdout, coverage_data)
                
                # Find all .gcov files
                gcov_files = []
                for root, dirs, files in os.walk(build_dir):
                    for file in files:
                        if file.endswith('.gcov'):
                            gcov_files.append(os.path.join(root, file))
                
                coverage_data["gcov_files"] = gcov_files
                
                # Analyze individual .gcov files for detailed gap analysis
                self._analyze_gcov_files(gcov_files, coverage_data)
            
            # Enhanced lcov analysis
            self._run_enhanced_lcov_analysis(build_dir, coverage_data)
            
        except Exception as e:
            print(f"[StateAdvancedCoverageImprovement] Enhanced coverage measurement error: {e}")
        
        return coverage_data

    def _parse_enhanced_gcov_output(self, gcov_output, coverage_data):
        """Parse enhanced gcov output for detailed metrics"""
        
        lines = gcov_output.split('\n')
        for line in lines:
            if 'Lines executed:' in line:
                # Extract percentage
                parts = line.split()
                for part in parts:
                    if part.endswith('%'):
                        try:
                            coverage_data["coverage_percentage"] = float(part[:-1])
                        except:
                            pass
            elif 'Branches executed:' in line:
                # Extract branch coverage
                parts = line.split()
                for part in parts:
                    if part.endswith('%'):
                        try:
                            coverage_data["branch_coverage"] = float(part[:-1])
                        except:
                            pass

    def _analyze_gcov_files(self, gcov_files, coverage_data):
        """Analyze individual .gcov files for uncovered lines and functions"""
        
        uncovered_lines = []
        uncovered_functions = []
        
        for gcov_file in gcov_files:
            try:
                with open(gcov_file, 'r') as f:
                    lines = f.readlines()
                
                current_function = None
                for i, line in enumerate(lines):
                    if line.strip().startswith('function'):
                        # Extract function name
                        if 'called 0 returned' in line:
                            func_name = line.split()[1] if len(line.split()) > 1 else "unknown"
                            uncovered_functions.append({
                                "function": func_name,
                                "file": gcov_file,
                                "line": i + 1
                            })
                    elif line.strip().startswith('#####'):
                        # Uncovered line
                        parts = line.split(':', 2)
                        if len(parts) >= 3:
                            line_num = parts[1].strip()
                            code = parts[2].strip()
                            uncovered_lines.append({
                                "line_number": line_num,
                                "code": code,
                                "file": gcov_file
                            })
            except Exception as e:
                print(f"Error analyzing {gcov_file}: {e}")
        
        coverage_data["uncovered_lines"] = uncovered_lines[:20]  # Limit to first 20
        coverage_data["uncovered_functions"] = uncovered_functions[:10]  # Limit to first 10

    def _run_enhanced_lcov_analysis(self, build_dir, coverage_data):
        """Run enhanced lcov analysis with detailed reporting"""
        
        try:
            lcov_file = os.path.join(build_dir, "coverage_enhanced.info")
            
            # Enhanced lcov with branch coverage
            lcov_cmd = [
                self.configReader.get_lcov_tool(),
                "--capture",
                "--directory", build_dir,
                "--output-file", lcov_file,
                "--ignore-errors", "gcov,source",
                "--rc", "lcov_branch_coverage=1"
            ]
            
            result = subprocess.run(lcov_cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # Generate enhanced HTML report
                html_dir = os.path.join(os.path.dirname(build_dir), "lcov_html_enhanced")
                genhtml_cmd = [
                    "genhtml",
                    lcov_file,
                    "--output-directory", html_dir,
                    "--branch-coverage",
                    "--function-coverage"
                ]
                
                result = subprocess.run(genhtml_cmd, capture_output=True, text=True)
                if result.returncode == 0:
                    coverage_data["enhanced_html_dir"] = html_dir
                
                self._parse_enhanced_lcov_data(lcov_file, coverage_data)
        except Exception as e:
            print(f"[StateAdvancedCoverageImprovement] Enhanced lcov error: {e}")

    def _parse_enhanced_lcov_data(self, lcov_file, coverage_data):
        """Parse enhanced lcov data for comprehensive statistics"""
        
        try:
            with open(lcov_file, 'r') as f:
                content = f.read()
            
            lines = content.split('\n')
            for line in lines:
                if line.startswith('LH:'):
                    coverage_data["lines_covered"] += int(line[3:])
                elif line.startswith('LF:'):
                    coverage_data["lines_total"] += int(line[3:])
                elif line.startswith('FNH:'):
                    coverage_data["functions_covered"] += int(line[4:])
                elif line.startswith('FNF:'):
                    coverage_data["functions_total"] += int(line[4:])
            
            # Recalculate percentage
            if coverage_data["lines_total"] > 0:
                coverage_data["coverage_percentage"] = (
                    coverage_data["lines_covered"] / coverage_data["lines_total"] * 100
                )
        except Exception as e:
            print(f"[StateAdvancedCoverageImprovement] Error parsing enhanced lcov data: {e}")

    def _run_advanced_analysis(self, coverage_data, source_files, project_path, iteration):
        """Run advanced coverage improvement analysis"""
        
        print(f"[StateAdvancedCoverageImprovement] Running advanced gap analysis...")
        
        # Get absolute paths for source files
        absolute_source_files = []
        for source_file in source_files:
            if source_file.startswith('/'):
                source_file = source_file[1:]
            abs_path = os.path.join(project_path, source_file)
            if os.path.exists(abs_path):
                absolute_source_files.append(abs_path)
        
        # Run comprehensive improvement analysis
        analysis_results = self.improvement_engine.analyze_and_improve_coverage(
            coverage_data, absolute_source_files, project_path
        )
        
        # Save analysis results
        output_dir = os.path.join("output/UnitTestCoverage", "CoverageImprovements")
        report_file = self.improvement_engine.save_improvement_analysis(
            analysis_results, output_dir
        )
        
        print(f"[StateAdvancedCoverageImprovement] Advanced analysis completed")
        print(f"   💡 Improvement opportunities: {analysis_results.get('total_improvements', 0)}")
        print(f"   📄 Detailed report: {report_file}")
        
        return analysis_results

    def _apply_intelligent_improvements(self, input_data, improvement_analysis, iteration):
        """Apply intelligent improvements based on analysis"""
        
        print(f"[StateAdvancedCoverageImprovement] Applying intelligent improvements...")
        
        # Extract actionable improvements
        strategy_results = improvement_analysis.get("strategy_results", {})
        
        for strategy_name, results in strategy_results.items():
            if "improvements" in results:
                improvements = results["improvements"]
                print(f"   🧠 Applying {len(improvements)} improvements from {strategy_name}")
                
                # Apply each improvement
                for improvement in improvements:
                    self._apply_single_improvement(improvement, input_data, iteration)

    def _apply_single_improvement(self, improvement, input_data, iteration):
        """Apply a single improvement to the test suite"""
        
        improvement_type = improvement.get("type", "unknown")
        
        if improvement_type in ["if_statement_branch_coverage", "switch_statement_coverage"]:
            # Generate additional test file for this improvement
            test_code = improvement.get("generated_tests", "")
            if test_code:
                self._save_improvement_test(test_code, improvement_type, iteration)

    def _save_improvement_test(self, test_code, improvement_type, iteration):
        """Save generated improvement test to unit tests directory"""
        
        if not test_code.strip():
            return
        
        unit_tests_dir = "output/UnitTestCoverage/unit_tests"
        test_filename = f"improvement_{improvement_type}_iter{iteration}.cpp"
        test_path = os.path.join(unit_tests_dir, test_filename)
        
        # Ensure proper test structure
        if "#include <gtest/gtest.h>" not in test_code:
            test_code = "#include <gtest/gtest.h>\n" + test_code
        
        with open(test_path, 'w') as f:
            f.write(test_code)
        
        print(f"   💾 Saved improvement test: {test_filename}")

    def _regenerate_enhanced_tests(self, input_data, coverage_data, iteration):
        """Regenerate tests with enhanced prompts based on coverage gaps"""
        
        print(f"[StateAdvancedCoverageImprovement] Regenerating tests with enhanced coverage focus...")
        
        # Import here to avoid circular dependency
        from States_Coverage.StateGenerateUnitTests import StateGenerateUnitTests
        
        # Enhance coverage data with specific gap information
        enhanced_coverage_data = coverage_data.copy()
        enhanced_coverage_data.update({
            "iteration": iteration,
            "improvement_focus": "enhanced_gap_analysis",
            "specific_gaps": {
                "uncovered_lines": coverage_data.get("uncovered_lines", []),
                "uncovered_functions": coverage_data.get("uncovered_functions", []),
                "branch_coverage": coverage_data.get("branch_coverage", 0.0)
            }
        })
        
        input_data.set_coverage_data(enhanced_coverage_data)
        
        # Regenerate with enhanced focus
        test_generator = StateGenerateUnitTests()
        test_generator.run(input_data)
# 🧠 C++ Micro Agent - Advanced Coverage Improvement System

A powerful LLM-powered tool that automatically generates high-quality unit tests for C++ projects with intelligent coverage improvement and cross-platform support (Linux/Windows).

## 🚀 Key Features

- **🎯 Intelligent Unit Test Generation**: Automatically generates comprehensive unit tests using LLM guidance with iterative coverage improvement
- **📊 Advanced Coverage Analysis**: Detailed branch, line, and function coverage analysis with lcov/gcov integration
- **🔄 Iterative Improvement**: ML-enhanced coverage prediction with automatic test regeneration to achieve target coverage
- **🌐 Cross-Platform Support**: Works on both Linux and Windows with platform-specific compiler detection
- **📈 Comprehensive Reporting**: Generates detailed HTML and text coverage reports with improvement suggestions
- **🏗️ Multi-Project Analysis**: Batch analysis capabilities for multiple C++ projects

## 🛠️ Prerequisites

### For Linux:
```bash
# Install required tools
sudo apt update
sudo apt install -y gcc g++ cmake lcov gcov build-essential

# Install Python dependencies
pip install requests ollama
```

### For Windows:
- **Visual Studio 2022**: Community or Professional with C++ development tools
- **MinGW**: For GCC compilation (included in project)

### Ollama Setup (Optional but Recommended):
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download recommended models
ollama pull qwen2.5:0.5b        # For enhanced test generation
ollama pull llama3.2:latest     # For unit test generation
```

## 🚀 Quick Start

### Main Entry Point - Quick Start Script
The easiest way to use C++ Micro Agent is through the interactive quick start script:

```bash
./quick_start.sh
```

This interactive menu provides:
1. **Generate Unit Tests** - Quick test generation (~30 seconds)
2. **Full Coverage Analysis** - Comprehensive coverage report (~1-2 minutes)
3. **Build Sample Application** - Compile the sample C++ project
4. **View Existing Reports** - Access previously generated reports
5. **Exit**

### Your First Run
```bash
# Step 1: Run the quick start script
./quick_start.sh

# Step 2: Select Option 1 to generate unit tests
# The script will analyze your C++ code and generate tests

# Step 3: Select Option 2 to run coverage analysis
# This analyzes the generated tests and produces coverage reports

# Step 4: View the HTML coverage report
open output/UnitTestCoverage/lcov_html/index.html
```

## 📊 Option 1: Generate Unit Tests - Process Flow

This option generates comprehensive unit tests for your C++ project using AI-enhanced analysis.

```
┌─────────────────────────────────────────────────────────────────┐
│                    OPTION 1: GENERATE UNIT TESTS                │
└─────────────────────────────────────────────────────────────────┘

Script: src/state_coverage/generate_and_build_tests.py

PHASE 1: PROJECT ANALYSIS
─────────────────────────
┌──────────────────┐
│ 1. Find Headers  │ → Scan TestProjects/SampleApplication/SampleApp/
│    (.h files)    │   - Locate src/ directory
└────────┬─────────┘   - Locate inc/ directory
         │             - Find all .h header files
         ↓
┌──────────────────┐
│ 2. Parse Classes │ → Extract class information from headers:
│    & Methods     │   - Class names
└────────┬─────────┘   - Public method signatures
         │             - Return types & parameters
         │             - Constructor/destructor identification
         ↓
┌──────────────────┐
│ 3. Find Source   │ → Locate all .cpp implementation files
│    Files (.cpp)  │   - Map to corresponding headers
└────────┬─────────┘   - Extract include dependencies
         │
         ↓

PHASE 2: MOCK GENERATION
────────────────────────
┌──────────────────┐
│ 4. Generate Mock │ → Create mock headers in output/ConsolidatedTests/mocks/
│    Headers       │   - Generate default implementations
└────────┬─────────┘   - Include necessary dependencies
         │             - Add include guards
         │             - Copy common.h if exists
         ↓
         
PHASE 3: TEST GENERATION (AI-ENHANCED)
──────────────────────────────────────
┌──────────────────┐
│ 5. Ollama Check  │ → Check if Ollama is available
│    (Optional)    │   - Model: qwen2.5:0.5b (preferred)
└────────┬─────────┘   - Fallback to template-based generation
         │
         ↓
┌──────────────────┐
│ 6. Generate Unit │ → For each method in each class:
│    Tests         │   
└────────┬─────────┘   CREATE: <filename>_<method>.cpp
         │             
         │             Test Types Based on Return Type:
         │             ┌─────────────────────────────────┐
         │             │ bool    → True/False scenarios  │
         │             │ int     → Boundary value tests  │
         │             │ void    → No-throw tests        │
         │             │ Object  → Validity tests        │
         │             └─────────────────────────────────┘
         │
         │             Threading Safety:
         │             ┌─────────────────────────────────┐
         │             │ - Add sleep delays for threads  │
         │             │ - Call init() before tests      │
         │             │ - Call close() after tests      │
         │             │ - Handle multi-threaded methods │
         │             └─────────────────────────────────┘
         ↓
┌──────────────────┐
│ 7. Save Metadata │ → Create test_metadata.json
│                  │   - Test file paths
└────────┬─────────┘   - Source file associations
         │             - Test names and classes
         ↓

PHASE 4: COMPILATION & EXECUTION
────────────────────────────────
┌──────────────────┐
│ 8. Compile Tests │ → Using g++ directly (no CMake):
│    with g++      │   
└────────┬─────────┘   Command Structure:
         │             ┌─────────────────────────────────┐
         │             │ g++ -std=c++14                  │
         │             │   -o bin/test_name              │
         │             │   test_file.cpp                 │
         │             │   all_source_files.cpp          │
         │             │   -I googletest/include         │
         │             │   -I mocks/                     │
         │             │   -I inc/                       │
         │             │   -L googletest/lib             │
         │             │   -lgtest -lgtest_main          │
         │             │   -lpthread                     │
         │             └─────────────────────────────────┘
         ↓
┌──────────────────┐
│ 9. Run Tests     │ → Execute each compiled test:
│                  │   
└────────┬─────────┘   Execution Strategy:
         │             ┌─────────────────────────────────┐
         │             │ ✅ Run simple tests normally    │
         │             │ ⏭️  Skip threading-heavy tests  │
         │             │    (InterfaceA, InterfaceB)     │
         │             │ ⏱️  Timeout: 10 seconds         │
         │             └─────────────────────────────────┘
         ↓
┌──────────────────┐
│ 10. Report       │ → Print summary:
│     Results      │   - Total tests generated
└──────────────────┘   - Compiled successfully
                       - Passed / Failed / Skipped
                       - Success rate calculation

OUTPUT ARTIFACTS
────────────────
📁 output/ConsolidatedTests/
   ├── mocks/                 ← Mock headers
   │   ├── Program.h
   │   ├── InterfaceA.h
   │   └── ...
   ├── tests/                 ← Generated test files
   │   ├── Program_init.cpp
   │   ├── Program_close.cpp
   │   └── ...
   ├── bin/                   ← Compiled test executables
   │   ├── Program_init
   │   ├── Program_close
   │   └── ...
   └── test_metadata.json     ← Test catalog

TIMING: ~30 seconds for sample project
```

## 📈 Option 2: Full Coverage Analysis - Process Flow

This option runs the generated tests and produces detailed coverage reports.

```
┌─────────────────────────────────────────────────────────────────┐
│              OPTION 2: FULL COVERAGE ANALYSIS                   │
└─────────────────────────────────────────────────────────────────┘

Script: src/run_coverage_analysis.py

PREREQUISITE CHECK
──────────────────
┌──────────────────┐
│ 1. Verify Tools  │ → Check if installed:
│    Installed     │   ✓ g++     (compiler)
└────────┬─────────┘   ✓ gcov    (coverage tool)
         │             ✓ lcov    (report generator)
         │
         ↓             If missing: sudo apt-get install lcov
┌──────────────────┐
│ 2. Verify Tests  │ → Check Option 1 output:
│    Exist         │   ✓ output/ConsolidatedTests/ exists
└────────┬─────────┘   ✓ test_metadata.json exists
         │             ✓ bin/ directory has executables
         │
         ↓             If missing: Run Option 1 first!

TEST EXECUTION PHASE
────────────────────
┌──────────────────┐
│ 3. Discover Test │ → Scan output/ConsolidatedTests/bin/
│    Executables   │   - Find all executable files
└────────┬─────────┘   - Load test metadata
         │             - Count available tests
         ↓
┌──────────────────┐
│ 4. Run Each Test │ → For each test executable:
│    Binary        │   
└────────┬─────────┘   Execution:
         │             ┌─────────────────────────────────┐
         │             │ ./bin/test_name                 │
         │             │                                 │
         │             │ Capture:                        │
         │             │   - stdout (test results)       │
         │             │   - stderr (errors)             │
         │             │   - return code                 │
         │             │                                 │
         │             │ Timeout: 10 seconds             │
         │             └─────────────────────────────────┘
         ↓
┌──────────────────┐
│ 5. Track Results │ → Categorize each test:
│                  │   
└────────┬─────────┘   Categories:
         │             ┌─────────────────────────────────┐
         │             │ ✅ PASSED   (exit code 0)      │
         │             │ ❌ FAILED   (exit code non-0)  │
         │             │ ⏱️  TIMEOUT (exceeded 10s)      │
         │             │ ❌ ERROR    (exception thrown)  │
         │             └─────────────────────────────────┘
         ↓

COVERAGE DATA COLLECTION
────────────────────────
┌──────────────────┐
│ 6. Initialize    │ → Run lcov to capture baseline:
│    Coverage Data │   
└────────┬─────────┘   Command:
         │             ┌─────────────────────────────────┐
         │             │ lcov --capture                  │
         │             │   --directory output/           │
         │             │   ConsolidatedTests             │
         │             │   --output-file                 │
         │             │   coverage.info                 │
         │             └─────────────────────────────────┘
         │
         │             This collects .gcda files from test runs
         ↓

REPORT GENERATION
─────────────────
┌──────────────────┐
│ 7. Generate HTML │ → Create interactive HTML report:
│    Coverage      │   
└────────┬─────────┘   Command:
         │             ┌─────────────────────────────────┐
         │             │ genhtml coverage.info           │
         │             │   --output-directory            │
         │             │   lcov_html/                    │
         │             └─────────────────────────────────┘
         │
         │             Creates:
         │             ┌─────────────────────────────────┐
         │             │ - index.html (main report)      │
         │             │ - Per-file coverage pages       │
         │             │ - Source code highlighting      │
         │             │ - Branch coverage details       │
         │             └─────────────────────────────────┘
         ↓
┌──────────────────┐
│ 8. Generate Text │ → Create summary report:
│    Summary       │   
└────────┬─────────┘   Extract:
         │             ┌─────────────────────────────────┐
         │             │ Overall Coverage Rate:          │
         │             │   - Lines covered: XX.X%        │
         │             │   - Functions covered: XX.X%    │
         │             │   - Branches covered: XX.X%     │
         │             │                                 │
         │             │ Per-File Coverage:              │
         │             │   Program.cpp: XX.X%            │
         │             │   InterfaceA.cpp: XX.X%         │
         │             │   ...                           │
         │             └─────────────────────────────────┘
         ↓

FINAL OUTPUT
────────────
┌──────────────────┐
│ 9. Print Summary │ → Display to console:
│    & Statistics  │   - Test execution summary
└──────────────────┘   - Coverage percentages
                       - Report locations
                       - Next steps

OUTPUT ARTIFACTS
────────────────
📁 output/UnitTestCoverage/
   ├── coverage.info          ← Raw coverage data (lcov format)
   ├── coverage_report.txt    ← Text summary report
   └── lcov_html/             ← Interactive HTML report
       ├── index.html         ← Main coverage dashboard
       ├── Program.cpp.gcov.html
       ├── InterfaceA.cpp.gcov.html
       └── ...

COVERAGE METRICS EXPLAINED
──────────────────────────
Line Coverage:     % of code lines executed by tests
Function Coverage: % of functions called by tests  
Branch Coverage:   % of conditional branches taken

TIMING: ~1-2 minutes for sample project

NOTE: This option does NOT use Ollama/LLM
      It only analyzes existing tests from Option 1
```

## 📁 Project Structure

```
CppMicroAgent/
├── quick_start.sh          # 🎯 MAIN ENTRY POINT (interactive menu)
├── install.sh              # Installation script
├── CppMicroAgent.cfg       # Configuration file
├── README.md               # This file
├── src/                    # Core modules
│   ├── state_coverage/     # Test generation scripts
│   │   └── generate_and_build_tests.py  # Option 1 script
│   ├── run_coverage_analysis.py         # Option 2 script
│   ├── states_coverage/    # Coverage analysis state machine
│   ├── ConfigReader.py     # Configuration management
│   ├── OllamaClient.py     # LLM integration
│   └── ...                 # Other core modules
├── TestProjects/           # Sample and test projects
│   ├── SampleApplication/  # Example C++ project
│   │   └── SampleApp/      # Default test target
│   ├── nlohmann-json/      # JSON library example
│   └── ...                 # Other test projects
└── output/                 # Generated reports and results
    ├── ConsolidatedTests/  # Option 1 output (tests)
    └── UnitTestCoverage/   # Option 2 output (coverage)
```

## 🎯 Usage Examples

### Example 1: First Time Usage (Recommended)
```bash
# Use the interactive quick start menu
./quick_start.sh

# Select Option 1: Generate Unit Tests
# Wait ~30 seconds for completion

# Select Option 2: Full Coverage Analysis  
# Wait ~1-2 minutes for completion

# View the HTML report
open output/UnitTestCoverage/lcov_html/index.html
```

### Example 2: Advanced - Analyze Your Own Project
```bash
# Step 1: Edit the test generation script to point to your project
nano src/state_coverage/generate_and_build_tests.py
# Update project_root path (line ~1035)

# Step 2: Run through quick_start.sh
./quick_start.sh
```

### Example 3: Direct Python Script Usage
```bash
# Run Option 1 directly
python3 src/state_coverage/generate_and_build_tests.py

# Run Option 2 directly
python3 src/run_coverage_analysis.py
```

## 📊 Understanding Results

After running both options through quick_start.sh, check the output directory:

### Option 1 Output (Unit Tests):
- **📄 test_metadata.json**: Catalog of all generated tests
- **🧪 tests/**: Individual test files (Program_init.cpp, etc.)
- **📦 bin/**: Compiled test executables
- **🔧 mocks/**: Mock header files for dependencies

### Option 2 Output (Coverage Analysis):
- **📄 coverage_report.txt**: Detailed text report with coverage metrics
- **🌐 lcov_html/index.html**: Interactive HTML coverage report (RECOMMENDED)
- **📈 coverage.info**: Raw coverage data in lcov format

### Coverage Metrics Explained:
- **Line Coverage**: Percentage of source lines executed during tests
- **Function Coverage**: Percentage of functions called by at least one test
- **Branch Coverage**: Percentage of conditional branches (if/else) taken during execution

### Visual Coverage Report:
Open `output/UnitTestCoverage/lcov_html/index.html` in a browser to see:
- Color-coded source files (green = covered, red = not covered)
- Per-function coverage breakdown
- Branch coverage visualization
- Uncovered code locations highlighted

## 🔧 Configuration

### Quick Start Configuration
The quick_start.sh script uses sensible defaults and requires minimal configuration. However, you can customize:

**Project Location**: Edit `src/state_coverage/generate_and_build_tests.py` (line ~1035)
```python
project_root = Path("/workspaces/CppMicroAgent/TestProjects/SampleApplication/SampleApp")
```

**Output Location**: Edit same file (line ~1036)
```python
output_root = Path("/workspaces/CppMicroAgent/output/ConsolidatedTests")
```

**GoogleTest Location**: Edit same file (line ~840)
```python
self.gtest_root = Path("/workspaces/CppMicroAgent/googletest-1.16.0")
```

## 🚨 Troubleshooting

### Common Issues:

1. **"Prerequisites not found"**
   - Run the prerequisite check in quick_start.sh
   - Install missing tools: `sudo apt-get install g++ lcov gcov`
   - Python 3 required: `sudo apt-get install python3`

2. **"Ollama not found" (Optional Warning)**
   - Ollama enhances test generation but is not required
   - Basic test generation works without Ollama
   - To install: `curl -fsSL https://ollama.com/install.sh | sh`
   - To get models: `ollama pull qwen2.5:0.5b`

3. **"No tests found" when running Option 2**
   - You must run Option 1 first to generate tests
   - Check if `output/ConsolidatedTests/` directory exists
   - Verify test_metadata.json was created

4. **"GoogleTest not found"**
   - The project includes GoogleTest 1.16.0
   - Ensure it's built: `ls googletest-1.16.0/build/lib/`
   - If missing, rebuild GoogleTest or run install.sh

5. **Some tests fail or timeout**
   - This is expected for threading-heavy code
   - Tests like InterfaceA and InterfaceB are skipped automatically
   - Coverage analysis still works with passing tests
   - Check test output in quick_start.sh for details

6. **Permission denied on quick_start.sh**
   - Make it executable: `chmod +x quick_start.sh`
   - Then run: `./quick_start.sh`

### Getting Help:
```bash
# Check if tests were generated
ls -la output/ConsolidatedTests/

# View test metadata
cat output/ConsolidatedTests/test_metadata.json | head -20

# Check coverage output
ls -la output/UnitTestCoverage/

# Verify prerequisites
which g++ gcov lcov python3
```

## 🏆 Expected Results

A successful run through quick_start.sh will produce:

### After Option 1 (Generate Unit Tests):
- ✅ 50+ unit tests generated for the sample application
- ✅ Tests compiled successfully with GoogleTest
- ✅ Mock headers created for all dependencies
- ✅ Test metadata catalog generated
- ✅ 70-80% of tests passing (some threading tests skipped)

### After Option 2 (Full Coverage Analysis):
- ✅ All compiled tests executed
- ✅ Coverage data collected via gcov
- ✅ HTML report with visual coverage highlighting
- ✅ Text report with detailed metrics
- ✅ Typical coverage: 60-75% line coverage for complex multi-threaded code

### Performance:
- Option 1: ~30 seconds (test generation + compilation)
- Option 2: ~1-2 minutes (test execution + coverage analysis)
- Total time: ~2 minutes for complete analysis

## 🎯 Quick Reference

### Main Commands:
```bash
# Primary way to use the tool
./quick_start.sh              # Interactive menu (RECOMMENDED)

# Direct script execution (advanced)
python3 src/state_coverage/generate_and_build_tests.py   # Option 1
python3 src/run_coverage_analysis.py                     # Option 2
```

### Directory Quick Access:
```bash
# View generated tests
ls output/ConsolidatedTests/tests/

# View test executables
ls output/ConsolidatedTests/bin/

# View coverage report (text)
cat output/UnitTestCoverage/coverage_report.txt

# Open HTML coverage report
open output/UnitTestCoverage/lcov_html/index.html
```

### Workflow Summary:
1. **Start**: `./quick_start.sh`
2. **Generate Tests**: Select Option 1
3. **Analyze Coverage**: Select Option 2
4. **Review Results**: Select Option 4 or open HTML report
5. **Iterate**: Modify code and repeat

## 🤝 Contributing

This tool is designed for safety-critical C++ development with emphasis on:
- High code coverage through intelligent test generation
- Quality assurance via automated testing
- Comprehensive reporting for compliance and documentation
- Cross-platform compatibility

---

**For more detailed documentation, see:**
- `HOW_TO_RUN.md` - Detailed setup and execution guide
- `QUICK_START_IMPROVEMENTS.md` - Enhancement history
- `OLLAMA_INTEGRATION_SUMMARY.md` - AI integration details
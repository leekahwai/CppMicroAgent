# New Per-Function Coverage Flow

## Overview
The coverage generation has been completely restructured to work on a **per-function basis** with test generation, compilation validation, and coverage measurement happening for each function individually before moving to the next.

---

## Main State Machine Flow

### 1. **StateInit**
- Initializes the system
- Prepares output directory

### 2. **StateParseCMake**
- Parses CMakeLists.txt
- Extracts source files and include directories
- Stores in `input_data`

### 3. **StateIterateSourceFiles**
- Iterates through each source file
- For each source file:
  - Extracts all functions (C-style and C++ member functions)
  - Creates directory structure: `output/UnitTestCoverage/<SourceFile>/<FunctionName>/`
  - For each function:
    - **Triggers Function-Level State Machine** (see below)
    - Waits for completion before moving to next function

### 4. **StateAggregateCoverageReports** *(NEW)*
- Collects all function-level coverage summaries
- Calculates overall project statistics
- Generates comprehensive final report
- Creates `FINAL_COVERAGE_REPORT.txt` with:
  - Overall coverage percentage
  - Per-function breakdown
  - Coverage distribution
  - Recommendations
  - Directory structure visualization

### 5. **StateEnd**
- Cleanup and finish

---

## Function-Level State Machine Flow

This state machine runs **for each individual function** found in the source code.

### 1. **StatesCreateMock**
- Analyzes function's header and source dependencies
- Generates mock headers for all external dependencies
- Saves mocks to function's directory: `output/UnitTestCoverage/<Source>/<Function>/<MockHeader>.h`
- **Flow:** If mocks generated → proceed to test generation

### 2. **StateGenerateFunctionTest** *(NEW)*
- Uses LLM (Ollama) to generate Google Test unit test for the specific function
- Creates prompt including:
  - Function implementation
  - Header content
  - Source context
  - Available mock headers
- Generates: `test_<FunctionName>.cpp`
- Saves to: `output/UnitTestCoverage/<Source>/<Function>/test_<FunctionName>.cpp`
- **Flow:** If test generated → proceed to compilation

### 3. **StateCompileFunctionTest** *(NEW)*
- Attempts to compile the generated test with coverage flags
- Compilation command:
  ```bash
  g++ -std=c++17 -g -O0 --coverage -fprofile-arcs -ftest-coverage \
      -I<project_paths> -I<mock_headers_dir> \
      test_<function>.cpp <source_file>.cpp \
      -lgtest -lgtest_main -lpthread \
      -o build/test_executable
  ```
- **Retry Logic (up to 3 attempts):**
  - If compilation fails:
    1. Captures compilation error output
    2. Sends error back to LLM with correction prompt
    3. LLM generates fixed test code
    4. Saves corrected test and retries compilation
  - Repeats until successful or max retries reached
- **Flow:** If compiled successfully → proceed to coverage measurement

### 4. **StateMeasureFunctionCoverage** *(NEW)*
- Runs the compiled test executable to generate coverage data
- Executes: `./test_executable` (generates `.gcda` files)
- Runs `gcov` to analyze coverage
- Generates coverage reports:
  - `.gcov` files (line-by-line coverage)
  - HTML report using `lcov` and `genhtml`
  - Text summary: `coverage_summary.txt`
- Saves all coverage data to function's directory
- **Flow:** Coverage complete → end function state machine

### 5. **StateEnd**
- Function processing complete
- Returns to main state machine to process next function

---

## New Directory Structure

```
output/UnitTestCoverage/
├── Program.cpp/                          # Source file directory
│   ├── Program/                          # Function directory (constructor)
│   │   ├── MockHeader1.h                 # Generated mocks
│   │   ├── MockHeader2.h
│   │   ├── test_Program.cpp              # ✅ NEW: Unit test for this function
│   │   ├── coverage_summary.txt          # ✅ NEW: Coverage summary
│   │   └── build/                        # ✅ NEW: Build artifacts
│   │       ├── test_executable           # Compiled test
│   │       ├── *.gcno, *.gcda            # Coverage data files
│   │       ├── *.gcov                    # Line coverage files
│   │       └── coverage_html/            # HTML coverage report
│   │           └── index.html
│   ├── DoSomething/                      # Another function
│   │   ├── test_DoSomething.cpp
│   │   ├── coverage_summary.txt
│   │   └── build/
│   └── ...
├── AnotherFile.cpp/
│   └── ...
└── FINAL_COVERAGE_REPORT.txt            # ✅ NEW: Aggregated final report
```

---

## Key Improvements

### ✅ **Per-Function Unit Tests**
- Each function gets its own dedicated unit test file
- Tests are focused and specific to the function
- Easy to identify which test covers which function

### ✅ **Compilation Validation with Retry**
- Tests are compiled immediately after generation
- Automatic retry with error feedback to LLM
- Ensures only compilable tests are accepted
- Max 3 retry attempts per function

### ✅ **Per-Function Coverage Measurement**
- Coverage is measured immediately for each function
- Coverage data is stored locally in function's directory
- HTML reports available per function for detailed analysis

### ✅ **Aggregated Final Report**
- Combines all function-level coverage into overall statistics
- Shows coverage distribution across the project
- Identifies functions needing attention
- Provides actionable recommendations

### ✅ **Better Organization**
- Each function has its own isolated workspace
- Easy to debug specific function tests
- Clear separation of concerns
- Reproducible per-function builds

---

## Flow Summary

```
Main Flow:
1. Parse CMakeLists.txt
2. For each source file:
   └─ For each function:
      ├─ Generate mocks
      ├─ Generate unit test (LLM)
      ├─ Compile test (with retry on error)
      ├─ Run test and measure coverage
      └─ Save coverage to function directory
3. Aggregate all coverage reports
4. Generate final comprehensive report
```

---

## What Was Removed

The following states are **NO LONGER USED** in the new flow:

- ❌ `StateCompileAndMeasureCoverage` - Replaced by per-function compilation
- ❌ `StateGenerateUnitTests` - Replaced by per-function test generation
- ❌ `StateAdvancedCoverageImprovement` - Replaced by retry logic in compilation
- ❌ `StateGenerateCoverageReport` - Replaced by StateAggregateCoverageReports

These files still exist in the codebase but are not part of the state machine flow.

---

## Benefits

1. **Immediate Feedback**: Know immediately if a test compiles and what coverage it achieves
2. **Isolated Failures**: If one function's test fails, others continue
3. **Easier Debugging**: Each function has its own workspace for troubleshooting
4. **Better Coverage Tracking**: See exactly which functions have good/poor coverage
5. **Incremental Progress**: Can stop and resume, already-completed functions are preserved
6. **Realistic Testing**: Each test is compiled and run, ensuring it actually works

---

## Configuration

The system uses the same configuration file (`CppMicroAgent.cfg`):
- `gtest_model`: LLM model for test generation
- `codegen_model`: LLM model for mock generation
- `gcov_tool`: Path to gcov (default: gcov)
- `lcov_tool`: Path to lcov (default: lcov)

---

## Next Steps

To use the new flow:
1. Run: `python3 main.py`
2. Select option 1 (Complete Coverage Analysis)
3. Watch as each function is processed individually
4. Review the final report: `output/UnitTestCoverage/FINAL_COVERAGE_REPORT.txt`
5. For detailed function coverage, open: `output/UnitTestCoverage/<Source>/<Function>/build/coverage_html/index.html`

================================================================================               │ │
 │ │                     NEW PER-FUNCTION COVERAGE FLOW                                             │ │
 │ │ ================================================================================               │ │
 │ │                                                                                                │ │
 │ │ MAIN STATE MACHINE:                                                                            │ │
 │ │ ═══════════════════                                                                            │ │
 │ │                                                                                                │ │
 │ │     ┌──────────────┐                                                                           │ │
 │ │     │  StateInit   │  Initialize system, prepare output directory                              │ │
 │ │     └──────┬───────┘                                                                           │ │
 │ │            │                                                                                   │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌──────────────────┐                                                                       │ │
 │ │     │ StateParseCMake  │  Parse CMakeLists.txt, extract sources & includes                     │ │
 │ │     └──────┬───────────┘                                                                       │ │
 │ │            │                                                                                   │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌───────────────────────────┐                                                              │ │
 │ │     │ StateIterateSourceFiles   │  For each source file found...                               │ │
 │ │     └───────────┬───────────────┘                                                              │ │
 │ │                 │                                                                              │ │
 │ │                 │  FOR EACH SOURCE FILE (e.g., Program.cpp)                                    │ │
 │ │                 │                                                                              │ │
 │ │                 ▼                                                                              │ │
 │ │         ╔═══════════════════════════════════════════════════╗                                  │ │
 │ │         ║  EXTRACT ALL FUNCTIONS FROM SOURCE FILE           ║                                  │ │
 │ │         ╚═══════════════════════════════════════════════════╝                                  │ │
 │ │                 │                                                                              │ │
 │ │                 │  FOR EACH FUNCTION (e.g., Program(), DoSomething())                          │ │
 │ │                 │                                                                              │ │
 │ │                 ▼                                                                              │ │
 │ │         ┌──────────────────────────────────────────────────┐                                   │ │
 │ │         │  CREATE DIRECTORY: output/UnitTestCoverage/      │                                   │ │
 │ │         │    Program.cpp/Program/                          │                                   │ │
 │ │         └──────────────────────────────────────────────────┘                                   │ │
 │ │                 │                                                                              │ │
 │ │                 │  ╔════════════════════════════════════════╗                                  │ │
 │ │                 └─>║  FUNCTION-LEVEL STATE MACHINE          ║                                  │ │
 │ │                    ║  (Runs for THIS specific function)    ║                                   │ │
 │ │                    ╚════════════════════════════════════════╝                                  │ │
 │ │                                     │                                                          │ │
 │ │                                     │ (See detailed flow below)                                │ │
 │ │                                     │                                                          │ │
 │ │                                     ▼                                                          │ │
 │ │                    ╔════════════════════════════════════════╗                                  │ │
 │ │                    ║  Function processing complete          ║                                  │ │
 │ │                    ║  Coverage saved to function directory  ║                                  │ │
 │ │                    ╚════════════════════════════════════════╝                                  │ │
 │ │                 │                                                                              │ │
 │ │                 │  REPEAT FOR ALL FUNCTIONS IN ALL SOURCE FILES                                │ │
 │ │                 │                                                                              │ │
 │ │                 ▼                                                                              │ │
 │ │     ┌─────────────────────────────────┐                                                        │ │
 │ │     │ StateAggregateCoverageReports   │  Collect all function coverage,                        │ │
 │ │     │                                 │  generate FINAL_COVERAGE_REPORT.txt                    │ │
 │ │     └──────┬──────────────────────────┘                                                        │ │
 │ │            │                                                                                   │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌──────────────┐                                                                           │ │
 │ │     │   StateEnd   │  Cleanup and finish                                                       │ │
 │ │     └──────────────┘                                                                           │ │
 │ │                                                                                                │ │
 │ │                                                                                                │ │
 │ │ FUNCTION-LEVEL STATE MACHINE (Detailed):                                                       │ │
 │ │ ════════════════════════════════════════                                                       │ │
 │ │                                                                                                │ │
 │ │ For a specific function: Program::Program()                                                    │ │
 │ │ In directory: output/UnitTestCoverage/Program.cpp/Program/                                     │ │
 │ │                                                                                                │ │
 │ │     ┌─────────────────────┐                                                                    │ │
 │ │     │  StatesCreateMock   │  Generate mock headers for dependencies                            │ │
 │ │     │                     │  Output: MockHeader1.h, MockHeader2.h                              │ │
 │ │     └──────┬──────────────┘                                                                    │ │
 │ │            │                                                                                   │ │
 │ │            │ SUCCESS: Mocks generated                                                          │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌──────────────────────────────┐                                                           │ │
 │ │     │  StateGenerateFunctionTest   │  Use LLM to generate test                                 │ │
 │ │     │                              │  Input: Function impl, headers, mocks                     │ │
 │ │     │                              │  Output: test_Program.cpp                                 │ │
 │ │     └──────┬───────────────────────┘                                                           │ │
 │ │            │                                                                                   │ │
 │ │            │ SUCCESS: Test code generated                                                      │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌────────────────────────────────────────────────────────┐                                 │ │
 │ │     │  StateCompileFunctionTest                              │                                 │ │
 │ │     │                                                        │                                 │ │
 │ │     │  Attempt 1: Compile test with g++ --coverage           │                                 │ │
 │ │     │             test_Program.cpp + Program.cpp             │                                 │ │
 │ │     │             -lgtest -lgtest_main                       │                                 │ │
 │ │     │                                                        │                                 │ │
 │ │     │  ┌─────────────────────────────────────────┐          │                                  │ │
 │ │     │  │ Compilation FAILED?                     │          │                                  │ │
 │ │     │  │  ├─> Capture error output               │          │                                  │ │
 │ │     │  │  ├─> Send to LLM with correction prompt │          │                                  │ │
 │ │     │  │  ├─> LLM generates fixed test           │          │                                  │ │
 │ │     │  │  └─> Retry compilation (up to 3 times)  │          │                                  │ │
 │ │     │  └─────────────────────────────────────────┘          │                                  │ │
 │ │     │                                                        │                                 │ │
 │ │     │  Output: build/test_executable (if successful)        │                                  │ │
 │ │     └──────┬─────────────────────────────────────────────────┘                                 │ │
 │ │            │                                                                                   │ │
 │ │            │ SUCCESS: Test compiled                                                            │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌────────────────────────────────────────────┐                                             │ │
 │ │     │  StateMeasureFunctionCoverage              │                                             │ │
 │ │     │                                            │                                             │ │
 │ │     │  Step 1: Run test executable               │                                             │ │
 │ │     │          ./build/test_executable           │                                             │ │
 │ │     │          (Generates .gcda coverage files)  │                                             │ │
 │ │     │                                            │                                             │ │
 │ │     │  Step 2: Run gcov for analysis             │                                             │ │
 │ │     │          gcov -b -c *.gcda                 │                                             │ │
 │ │     │          (Generates .gcov files)           │                                             │ │
 │ │     │                                            │                                             │ │
 │ │     │  Step 3: Generate HTML report              │                                             │ │
 │ │     │          lcov --capture                    │                                             │ │
 │ │     │          genhtml → coverage_html/          │                                             │ │
 │ │     │                                            │                                             │ │
 │ │     │  Step 4: Save coverage summary             │                                             │ │
 │ │     │          coverage_summary.txt              │                                             │ │
 │ │     │          - Coverage: 85.5%                 │                                             │ │
 │ │     │          - Lines: 34/40                    │                                             │ │
 │ │     │                                            │                                             │ │
 │ │     └──────┬─────────────────────────────────────┘                                             │ │
 │ │            │                                                                                   │ │
 │ │            │ SUCCESS: Coverage measured and saved                                              │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌─────────────┐                                                                            │ │
 │ │     │  StateEnd   │  Function processing complete                                              │ │
 │ │     └─────────────┘                                                                            │ │
 │ │            │                                                                                   │ │
 │ │            │ Return to main state machine                                                      │ │
 │ │            ▼                                                                                   │ │
 │ │     [Process next function...]                                                                 │ │
 │ │                                                                                                │ │
 │ │                                                                                                │ │
 │ │ AGGREGATION PHASE:                                                                             │ │
 │ │ ═══════════════════                                                                            │ │
 │ │                                                                                                │ │
 │ │ StateAggregateCoverageReports walks through all function directories:                          │ │
 │ │                                                                                                │ │
 │ │     output/UnitTestCoverage/                                                                   │ │
 │ │     ├── Program.cpp/                                                                           │ │
 │ │     │   ├── Program/coverage_summary.txt          ──┐                                          │ │
 │ │     │   └── DoSomething/coverage_summary.txt      ──┤                                          │ │
 │ │     ├── Helper.cpp/                                 │                                          │ │
 │ │     │   ├── HelperFunc/coverage_summary.txt       ──┤                                          │ │
 │ │     │   └── AnotherFunc/coverage_summary.txt      ──┤                                          │ │
 │ │     └── ...                                          │                                         │ │
 │ │                                                      │                                         │ │
 │ │                                     READ ALL ────────┘                                         │ │
 │ │                                          │                                                     │ │
 │ │                                          ▼                                                     │ │
 │ │                             ┌────────────────────────────┐                                     │ │
 │ │                             │  Calculate Overall Stats:  │                                     │ │
 │ │                             │  - Total coverage: 78.2%   │                                     │ │
 │ │                             │  - Lines: 234/300          │                                     │ │
 │ │                             │  - Functions: 8            │                                     │ │
 │ │                             └────────────────────────────┘                                     │ │
 │ │                                          │                                                     │ │
 │ │                                          ▼                                                     │ │
 │ │                             ┌────────────────────────────┐                                     │ │
 │ │                             │  Generate Final Report:    │                                     │ │
 │ │                             │  FINAL_COVERAGE_REPORT.txt │                                     │ │
 │ │                             │                            │                                     │ │
 │ │                             │  - Overall summary         │                                     │ │
 │ │                             │  - Per-function breakdown  │                                     │ │
 │ │                             │  - Coverage distribution   │                                     │ │
 │ │                             │  - Recommendations         │                                     │ │
 │ │                             └────────────────────────────┘                                     │ │
 │ │                                                                                                │ │
 │ │                                                                                                │ │
 │ │ RETRY LOGIC DETAIL (Compilation):                                                              │ │
 │ │ ═══════════════════════════════════                                                            │ │
 │ │                                                                                                │ │
 │ │     ┌─────────────────────┐                                                                    │ │
 │ │     │  Generate Test      │                                                                    │ │
 │ │     └──────┬──────────────┘                                                                    │ │
 │ │            │                                                                                   │ │
 │ │            ▼                                                                                   │ │
 │ │     ┌──────────────────────┐                                                                   │ │
 │ │     │  Attempt Compile (1) │                                                                   │ │
 │ │     └──────┬───────────────┘                                                                   │ │
 │ │            │                                                                                   │ │
 │ │     ┌──────▼──────────────────────────────┐                                                    │ │
 │ │     │  Compilation Result?                │                                                    │ │
 │ │     └─┬─────────────────────────────────┬─┘                                                    │ │
 │ │       │                                 │                                                      │ │
 │ │       │ SUCCESS                         │ FAILED                                               │ │
 │ │       │                                 │                                                      │ │
 │ │       ▼                                 ▼                                                      │ │
 │ │     ┌─────────────────┐      ┌──────────────────────────────┐                                  │ │
 │ │     │  Proceed to     │      │  Send error to LLM:          │                                  │ │
 │ │     │  Coverage       │      │  "Fix these errors: ..."     │                                  │ │
 │ │     └─────────────────┘      └──────┬───────────────────────┘                                  │ │
 │ │                                     │                                                          │ │
 │ │                                     ▼                                                          │ │
 │ │                              ┌──────────────────────┐                                          │ │
 │ │                              │  LLM generates fix   │                                          │ │
 │ │                              └──────┬───────────────┘                                          │ │
 │ │                                     │                                                          │ │
 │ │                                     ▼                                                          │ │
 │ │                              ┌──────────────────────┐                                          │ │
 │ │                              │  Attempt Compile (2) │                                          │ │
 │ │                              └──────┬───────────────┘                                          │ │
 │ │                                     │                                                          │ │
 │ │                     ┌───────────────┴───────────────┐                                          │ │
 │ │                     │ FAILED                        │ SUCCESS                                  │ │
 │ │                     ▼                               ▼                                          │ │
 │ │             ┌──────────────────┐          ┌─────────────────┐                                  │ │
 │ │             │  Retry Count < 3?│          │  Proceed to     │                                  │ │
 │ │             └──────┬───────────┘          │  Coverage       │                                  │ │
 │ │                    │                      └─────────────────┘                                  │ │
 │ │          ┌─────────┴─────────┐                                                                 │ │
 │ │          │ YES               │ NO                                                              │ │
 │ │          ▼                   ▼                                                                 │ │
 │ │     [Retry again]      ┌──────────────┐                                                        │ │
 │ │                        │  Skip this   │                                                        │ │
 │ │                        │  function    │                                                        │ │
 │ │                        └──────────────┘                                                        │ │
 │ │                                                                                                │ │
 │ │                                                                                                │ │
 │ │ ================================================================================               │ │
 │ │ EOF                                                                                            │ │
 │ │ cat /workspaces/CppMicroAgent/FLOW_DIAGRAM.txt 

 
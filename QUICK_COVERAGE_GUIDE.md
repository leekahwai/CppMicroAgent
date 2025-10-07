# Quick Coverage Guide

## 🚀 Quick Start

### Generate Tests and Coverage Report
```bash
cd /workspaces/CppMicroAgent
python3 src/quick_test_generator/generate_and_build_tests.py
python3 src/run_coverage_analysis.py
```

### View Coverage Report
```bash
# Open in browser
open output/UnitTestCoverage/lcov_html/index.html

# Or use Python's HTTP server
cd output/UnitTestCoverage/lcov_html
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

## 📊 Current Coverage Stats

| Metric | Baseline | Improved | Gain |
|--------|----------|----------|------|
| **Lines** | 64.8% | 69.5% | +4.7% |
| **Functions** | 71.3% | 74.4% | +3.1% |

## 🎯 How to Improve Function Coverage

### Option 1: Generate More Targeted Tests
```bash
python3 src/generate_targeted_tests.py
```
This creates tests specifically designed to cover uncovered functions.

### Option 2: Analyze Coverage Gaps
```bash
python3 src/improve_function_coverage.py
```
This analyzes what's missing and suggests improvements.

### Option 3: Fix Source Code Issues
The biggest gains come from fixing bugs in the source code that prevent tests from running:

**Quick Fix for IntfA_Rx** (add to line 14 in `IntfA_rx.cpp`):
```cpp
bStart = true;  // Add this before starting thread
```

**Quick Fix for InterfaceA** (add to `init()` and `close()` methods):
```cpp
intfRx.init();   // Add to init()
intfRx.close();  // Add to close()
```

## 🔍 Understanding Coverage Reports

### HTML Report Structure
```
lcov_html/
├── index.html          # Main coverage summary
├── InterfaceA/         # Per-class coverage
├── InterfaceB/
├── Program/
└── ...
```

### Reading Coverage Colors
- 🟢 **Green**: Lines executed
- 🔴 **Red**: Lines NOT executed  
- 🟡 **Yellow**: Partially executed branches

### Coverage Metrics
- **Lines**: Percentage of code lines executed
- **Functions**: Percentage of functions called
- **Branches**: Percentage of conditional branches taken

## 🛠️ Troubleshooting

### Problem: Coverage report is empty
**Solution**: Make sure tests are compiled with `--coverage` flag
```bash
# Check if .gcda files exist
find output/ConsolidatedTests -name "*.gcda"
```

### Problem: Tests are crashing
**Solution**: Use targeted tests that avoid problematic code
```bash
python3 src/generate_targeted_tests.py
```

### Problem: Function coverage not improving
**Solution**: 
1. Identify which functions aren't covered:
```bash
lcov --list output/UnitTestCoverage/coverage.info | grep "0.0%"
```
2. Create specific tests for those functions

## 📝 Best Practices

### 1. Always Recompile After Code Changes
```bash
python3 src/quick_test_generator/generate_and_build_tests.py
```

### 2. Clean Old Coverage Data
```bash
find output/ConsolidatedTests -name "*.gcda" -delete
```

### 3. Run Tests Before Generating Reports
The coverage report needs `.gcda` files which are generated when tests run.

### 4. Check Test Results
```bash
# Run a specific test to see details
output/ConsolidatedTests/bin/IntfA_tx_init
```

## 🎓 Advanced Usage

### Compare Coverage Between Runs
```bash
# Save baseline
cp output/UnitTestCoverage/coverage.info baseline.info

# Make changes and regenerate
python3 src/quick_test_generator/generate_and_build_tests.py
python3 src/run_coverage_analysis.py

# Compare
lcov --diff baseline.info output/UnitTestCoverage/coverage.info
```

### Filter Coverage by Directory
```bash
lcov --extract coverage.info '*/InterfaceA/*' --output-file interfaceA.info
genhtml interfaceA.info --output-directory interfaceA_coverage
```

### Get Coverage for Specific File
```bash
lcov --list coverage.info | grep InterfaceA.cpp
```

## 📚 Related Scripts

| Script | Purpose |
|--------|---------|
| `src/quick_test_generator/generate_and_build_tests.py` | Main test generator |
| `src/run_coverage_analysis.py` | Generate coverage reports |
| `src/generate_targeted_tests.py` | Create targeted tests |
| `src/improve_function_coverage.py` | Analyze and improve coverage |

## 🎯 Goal: 80% Function Coverage

**Current**: 74.4%  
**Target**: 80%  
**Gap**: 5.6% (≈43 more functions)

To reach 80% function coverage:
1. ✅ Fix threading bugs in IntfA_Rx and IntfB_Rx (estimated +2%)
2. ✅ Fix init/close in InterfaceA and InterfaceB (estimated +2%)
3. ✅ Add tests for remaining uncovered methods (estimated +2%)

Total estimated improvement: **~6%** → **~80%** function coverage

## 🆘 Need Help?

See `COVERAGE_IMPROVEMENT_SUMMARY.md` for detailed documentation.

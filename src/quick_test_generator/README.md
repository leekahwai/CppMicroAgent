# State Coverage - Python-Only Test Generation System

## 🐍 Python-Only Interface - No CMake Required!

**Single command does everything:**
```bash
python3 src/state_coverage/generate_and_build_tests.py
```

The script will analyze, generate, compile (with g++), and run tests automatically.

## ✅ What It Does

1. Analyzes all C++ source files
2. Generates consolidated mock headers (9 mocks in one folder)
3. Generates unit tests with boundary and condition testing (25 tests)
4. Compiles tests directly using g++ (no CMake!)
5. Runs tests and reports results

## 📊 Current Results

```
Total Tests:      25
Compiled:          9 ✅
Passed:            9 ✅ (11 test cases)
```

## 🎯 Key Features

- **Python-Only**: User only interacts with Python code
- **Consolidated Mocks**: All mocks in `/output/ConsolidatedTests/mocks/`
- **Clear Naming**: `<filename>_<method>.cpp` (e.g., `Program_run.cpp`)
- **Direct g++ Compilation**: No CMake or Makefiles
- **Boundary Testing**: INT_MIN/MAX, initial values, edge cases
- **Condition Testing**: Success/failure, consistency, exceptions

## 📁 Generated Structure

```
ConsolidatedTests/
├── mocks/        # 9 mock headers (consolidated)
├── tests/        # 25 test files  
├── bin/          # 9 compiled binaries
└── test_metadata.json
```

## 🚀 Usage

```bash
cd /workspaces/CppMicroAgent
python3 src/state_coverage/generate_and_build_tests.py
```

To run individual tests:
```bash
cd output/ConsolidatedTests
./bin/Program_run
./bin/IntfA_tx_init
```

## 📝 Documentation

See `/PYTHON_ONLY_TEST_GENERATION_COMPLETE.md` for complete details.

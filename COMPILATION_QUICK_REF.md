# Compilation Strategy Quick Reference

## The Problem You Asked About

**Question:** "What was being used in the compilation? Can we make sure that it uses the test_xx.cpp, the mock header as well as the correct source files that it targets to compile?"

**Answer:** Yes! The compilation now correctly uses:
- ✅ `test_xx.cpp` (the generated test file)
- ✅ Mock headers (e.g., `InterfaceA.h`, `InterfaceB.h` from the run directory)
- ✅ Correct source file (e.g., `Program.cpp` from TestProjects/...)
- ✅ Correct header (e.g., `Program.h` from TestProjects/...)

## How It Works

### For `output/UnitTestCoverage/Program.cpp/Program/run`

```
Compiles:
  📝 test_Program.cpp         (from output/.../run/)
  📝 Program.cpp              (from TestProjects/.../src/Program/)
  📝 gtest-all.cc             (GoogleTest)
  📝 gtest_main.cc            (GoogleTest)

Includes:
  📄 Program.h                (from TestProjects/.../src/Program/) ← REAL
  📄 InterfaceA.h             (from output/.../run/)              ← MOCK
  📄 InterfaceB.h             (from output/.../run/)              ← MOCK
```

## The Secret: Include Path Order

```bash
-I output/.../run/           # 1. MOCKS FIRST (highest priority)
-I TestProjects/.../Program/ # 2. Real header directory
-I TestProjects/.../         # 3. Other project paths
```

### Why This Order Works

```
test_Program.cpp
  └─► #include "Program.h"
       └─► Found in: TestProjects/.../Program/Program.h (REAL) ✓
            └─► #include "InterfaceA.h"
                 └─► Found in: output/.../run/InterfaceA.h (MOCK) ✓
```

## Complete Command Example

```bash
g++ -std=c++17 -g -O0 --coverage \
    -I output/UnitTestCoverage/Program.cpp/Program/run \        # Mocks
    -I TestProjects/SampleApplication/SampleApp/src/Program \   # Real header
    -I googletest-1.16.0/googletest/include \
    -I googletest-1.16.0/googletest \
    output/UnitTestCoverage/Program.cpp/Program/run/test_Program.cpp \
    TestProjects/SampleApplication/SampleApp/src/Program/Program.cpp \
    googletest-1.16.0/googletest/src/gtest-all.cc \
    googletest-1.16.0/googletest/src/gtest_main.cc \
    -lpthread \
    -o test_executable
```

## What Changed

### Before (BROKEN)
```python
include_paths = [
    f"-I{project_path}",
    f"-I{os.path.dirname(source_file)}",
    f"-I{output_folder}",  # ❌ Mocks LAST
]
# Result: Real headers found instead of mocks!
```

### After (FIXED)
```python
include_paths = [
    f"-I{output_folder}",  # ✅ Mocks FIRST
    f"-I{os.path.dirname(source_file)}",
    f"-I{project_path}",
]
# Result: Mocks have priority, real headers found when needed!
```

## Key Points

1. **Mock headers must come FIRST** in include paths
2. **Source directory comes SECOND** so real header is found
3. **Only the target .cpp is compiled** (not dependencies)
4. **GoogleTest compiled from source** (no system dependencies)

## File Location

The fix is in: `src/states_coverage/States_Function/StateCompileFunctionTest.py`
Method: `_compile_test()` (lines 71-134)

## Verification

Run: `./verify_compilation_fix.sh`

Or manually:
```bash
g++ -std=c++17 -g -O0 --coverage \
    -I output/UnitTestCoverage/Program.cpp/Program/run \
    -I TestProjects/SampleApplication/SampleApp/src/Program \
    -I googletest-1.16.0/googletest/include \
    -I googletest-1.16.0/googletest \
    output/UnitTestCoverage/Program.cpp/Program/run/test_Program.cpp \
    TestProjects/SampleApplication/SampleApp/src/Program/Program.cpp \
    googletest-1.16.0/googletest/src/gtest-all.cc \
    googletest-1.16.0/googletest/src/gtest_main.cc \
    -lpthread \
    -o /tmp/test && /tmp/test
```

Should output: `[  PASSED  ] 1 test.`

## More Info

- **COMPILATION_STRATEGY.md** - Full documentation
- **COMPILATION_FLOW.txt** - Visual diagram
- **CHANGES_TO_COMPILATION.md** - Detailed changes

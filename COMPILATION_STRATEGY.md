# Code Coverage Compilation Strategy

## Overview

This document explains the compilation strategy used for code coverage unit tests in the CppMicroAgent system. The goal is to test individual source files (like `Program.cpp`) with their actual headers while using mock headers for dependencies.

## Compilation Requirements

When testing a source file like `TestProjects/SampleApplication/SampleApp/src/Program/Program.cpp`, the compilation must include:

1. **Test file**: The generated unit test (e.g., `test_Program.cpp`)
2. **Source file**: The actual implementation being tested (e.g., `Program.cpp`)
3. **Real header**: The actual header for the source file (e.g., `Program.h`)
4. **Mock headers**: Mock implementations for dependencies (e.g., `InterfaceA.h`, `InterfaceB.h`)

## Include Path Priority (CRITICAL!)

The order of include paths is **critical** for proper compilation:

```bash
-I output/UnitTestCoverage/Program.cpp/Program/run  # 1. MOCK HEADERS FIRST
-I TestProjects/.../src/Program                     # 2. Real header directory
-I TestProjects/.../SampleApp                       # 3. Project directories
# ... other project paths
```

### Why Order Matters

1. **Mock headers first** (`-I output/.../run`): When the real header `Program.h` includes `"InterfaceA.h"`, the compiler should find the **mock** version from the test directory, not the real one.

2. **Real header second** (`-I .../src/Program`): When the test file includes `"Program.h"`, it should find the **actual** header from the source directory.

3. **Project paths last**: For any other includes that aren't mocked.

## Example: Testing Program.cpp

### File Structure
```
TestProjects/SampleApplication/SampleApp/src/Program/
├── Program.cpp          # Source being tested
└── Program.h            # Real header (includes InterfaceA.h, InterfaceB.h)

output/UnitTestCoverage/Program.cpp/Program/run/
├── test_Program.cpp     # Generated test file
├── InterfaceA.h         # MOCK header
└── InterfaceB.h         # MOCK header
```

### Compilation Flow

1. **Test includes Program.h**:
   ```cpp
   #include "Program.h"  // Finds: TestProjects/.../src/Program/Program.h
   ```

2. **Program.h includes dependencies**:
   ```cpp
   #include "InterfaceA.h"  // Finds: output/.../run/InterfaceA.h (MOCK!)
   #include "InterfaceB.h"  // Finds: output/.../run/InterfaceB.h (MOCK!)
   ```

3. **Source file compiles**:
   - `Program.cpp` gets compiled with its real header
   - Dependencies are resolved using mock headers
   - No need to compile actual InterfaceA.cpp or InterfaceB.cpp

### Complete Compilation Command

```bash
g++ -std=c++17 -g -O0 --coverage \
  -I output/UnitTestCoverage/Program.cpp/Program/run \      # Mocks FIRST
  -I TestProjects/SampleApplication/SampleApp/src/Program \ # Real header
  -I googletest-1.16.0/googletest/include \                 # GTest
  -I googletest-1.16.0/googletest \                         # GTest internal
  output/UnitTestCoverage/Program.cpp/Program/run/test_Program.cpp \
  TestProjects/SampleApplication/SampleApp/src/Program/Program.cpp \
  googletest-1.16.0/googletest/src/gtest-all.cc \
  googletest-1.16.0/googletest/src/gtest_main.cc \
  -lpthread \
  -o test_executable
```

## Key Points

1. **Include order is critical**: Mock headers must come first in include paths
2. **No need to compile dependencies**: Mock headers provide minimal implementations
3. **Test only the target**: Only `Program.cpp` is compiled, not its dependencies
4. **Coverage is accurate**: Since we compile the actual source file with mocked dependencies

## Common Compilation Errors

### Error: "No such file or directory" for Program.h
**Cause**: Missing source file directory in include paths
**Fix**: Add `-I{os.path.dirname(source_file)}` to include paths

### Error: "InterfaceA does not name a type"
**Cause**: Missing mock header or mock header has wrong content
**Fix**: Ensure all dependencies have proper mock headers generated

### Error: Real dependency file included instead of mock
**Cause**: Include path order is wrong
**Fix**: Ensure output_folder with mocks comes FIRST in include paths

### Error: "redefinition of class Program"
**Cause**: Test file incorrectly defines the class being tested
**Fix**: Test should only instantiate the class, not redefine it

## Implementation Location

The compilation logic is implemented in:
- **File**: `src/states_coverage/States_Function/StateCompileFunctionTest.py`
- **Method**: `_compile_test()`
- **Lines**: 71-122 (approximately)

## Testing the Strategy

To verify the compilation strategy works:

```bash
cd /workspaces/CppMicroAgent

# Ensure mocks exist
ls output/UnitTestCoverage/Program.cpp/Program/run/*.h

# Try manual compilation
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
  -o /tmp/test_program

# Run the test
/tmp/test_program
```

## Benefits of This Strategy

1. **Isolation**: Tests only the target file, not its dependencies
2. **Speed**: Faster compilation (only one source file + test)
3. **Coverage accuracy**: Coverage metrics reflect only the tested file
4. **Maintainability**: Changes to dependencies don't break tests
5. **Flexibility**: Easy to control dependency behavior through mocks

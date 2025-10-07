# State Coverage - Consolidated Unit Test Generator

## Overview

This is the new consolidated approach for generating unit tests with comprehensive boundary and condition testing. It replaces the old `advanced_coverage_workflow` approach (now renamed to `advanced_coverage_workflow_old`).

## Key Features

### 1. Consolidated Mock Headers
All mock headers are generated in a single folder (`/output/ConsolidatedTests/mocks/`) instead of creating separate folders for each method. This approach:
- Reduces duplication
- Simplifies maintenance
- Makes mocks reusable across all tests
- Improves build times

### 2. Filename-Based Test Naming
Tests follow the pattern: `<filename>_<method>.cpp`

Examples:
- `Program_run.cpp` - Tests for `Program::run()` method
- `InterfaceA_init.cpp` - Tests for `InterfaceA::init()` method
- `InterfaceA_getTxStats.cpp` - Tests for `InterfaceA::getTxStats()` method

### 3. Real Implementation with Mock Dependencies
Each test:
- Links to the **actual source file** being tested
- Uses **mock headers** for all other dependencies
- This provides true unit testing by isolating the unit under test

### 4. Comprehensive Boundary and Condition Testing

For each method, the generator creates tests based on the method's return type and characteristics:

#### Boolean Methods
- `ReturnsTrueOnSuccess` - Tests success path
- `ReturnsFalseOnFailure` - Tests failure path
- `HandlesBoundaryConditions` - Tests edge cases

#### Numeric Methods (int, long, etc.)
- `ReturnsValidValue` - Verifies non-negative values
- `ReturnsZeroInitially` - Tests initial state
- `HandlesBoundaryValues` - Tests INT_MIN to INT_MAX range
- `ConsistentAcrossMultipleCalls` - Tests consistency

#### Void Methods
- `ExecutesWithoutThrowing` - Ensures no exceptions
- `CanBeCalledMultipleTimes` - Tests repeatability
- `HandlesInvalidConditions` - Tests edge cases

#### Constructors
- `ConstructorCreatesValidObject` - Verifies object creation
- `MultipleInstancesCanBeCreated` - Tests multiple instances

## Usage

### Generate Tests

```bash
cd /workspaces/CppMicroAgent
python3 src/state_coverage/generate_consolidated_tests.py
```

The script will:
1. Analyze all source files in `TestProjects/SampleApplication/SampleApp/src/`
2. Parse header files to extract class and method information
3. Generate consolidated mock headers in `/output/ConsolidatedTests/mocks/`
4. Generate unit tests in `/output/ConsolidatedTests/tests/`
5. Create CMakeLists.txt for building

### Build and Run Tests

```bash
cd /workspaces/CppMicroAgent/output/ConsolidatedTests
mkdir build && cd build
cmake ..
make -j4
ctest --verbose
```

### Run Individual Test

```bash
cd /workspaces/CppMicroAgent/output/ConsolidatedTests/build
./Program_run
./InterfaceA_init
```

## Architecture

### Python Script Structure

**File**: `generate_consolidated_tests.py`

#### Main Classes:

1. **HeaderAnalyzer**
   - Finds all source and header files
   - Parses C++ classes and methods
   - Handles modern C++ syntax (auto -> type)
   - Extracts non-system includes
   - Identifies constructors, destructors, and regular methods

2. **MockGenerator**
   - Creates mock headers for all classes
   - Generates default constructors and destructors
   - Creates stub implementations that return sensible defaults
   - Handles struct typedefs (structA, structB)
   - Includes necessary headers (common.h, etc.)

3. **UnitTestGenerator**
   - Generates test files with GoogleTest framework
   - Creates test fixtures for each method
   - Generates boundary condition tests
   - Creates condition tests based on return type
   - Links real source with mock dependencies

### Generated File Structure

```
/workspaces/CppMicroAgent/
├── src/
│   ├── state_coverage/              # New approach
│   │   ├── generate_consolidated_tests.py
│   │   └── README.md (this file)
│   └── advanced_coverage_workflow_old/         # Old approach (renamed)
└── output/
    └── ConsolidatedTests/
        ├── mocks/                   # Consolidated mock headers
        │   ├── InterfaceA.h
        │   ├── InterfaceB.h
        │   ├── Program.h
        │   ├── common.h
        │   └── ...
        ├── tests/                   # Unit tests
        │   ├── Program_run.cpp
        │   ├── InterfaceA_init.cpp
        │   ├── InterfaceA_getTxStats.cpp
        │   └── ...
        ├── CMakeLists.txt           # Build configuration
        ├── SUMMARY.md               # Generated files summary
        └── build/                   # Build directory
```

## CMake Build System

### Key Features

1. **Automatic Test Discovery**: Finds all `*_*.cpp` files in tests/
2. **Source File Matching**: Automatically matches tests with source files
3. **Include Path Priority**: Mocks take precedence over real headers
4. **Individual Test Executables**: Each test is a separate executable
5. **CTest Integration**: All tests registered with CTest

### Include Order (Critical)

The CMakeLists.txt sets includes in this specific order:
1. `mocks/` - Mock headers (highest priority)
2. `src/` - Source directories
3. `inc/` - Include directories

This ensures:
- Dependencies use mock implementations
- The tested class uses its real header
- True unit testing isolation

## Example Files

### Mock Header Example

**File**: `mocks/InterfaceA.h`

```cpp
#ifndef MOCK_INTERFACEA_H
#define MOCK_INTERFACEA_H

#include <cstdint>
#include <string>
#include "common.h"

class InterfaceA {
public:
    InterfaceA() {}
    ~InterfaceA() {}
    
    void addToTx(structA& data) {}
    void addToRx(structA& data) {}
    
    bool init() { return true; }
    void close() {}
    
    int getTxStats() { return 0; }
    int getRxStats() { return 0; }
};

#endif
```

### Test File Example

**File**: `tests/InterfaceA_getTxStats.cpp`

```cpp
#include <gtest/gtest.h>
#include "InterfaceA.h"

class InterfaceA_getTxStats_Test : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}
};

// Test: getTxStats returns valid value
TEST_F(InterfaceA_getTxStats_Test, ReturnsValidValue) {
    InterfaceA obj;
    auto result = obj.getTxStats();
    EXPECT_GE(result, 0);
}

// Test: getTxStats returns zero initially
TEST_F(InterfaceA_getTxStats_Test, ReturnsZeroInitially) {
    InterfaceA obj;
    auto result = obj.getTxStats();
    EXPECT_EQ(result, 0);
}

// Test: getTxStats handles boundary values
TEST_F(InterfaceA_getTxStats_Test, HandlesBoundaryValues) {
    InterfaceA obj;
    auto result = obj.getTxStats();
    EXPECT_GE(result, INT_MIN);
    EXPECT_LE(result, INT_MAX);
}

// Test: getTxStats consistent across multiple calls
TEST_F(InterfaceA_getTxStats_Test, ConsistentAcrossMultipleCalls) {
    InterfaceA obj;
    auto result1 = obj.getTxStats();
    auto result2 = obj.getTxStats();
    SUCCEED();
}
```

## Customization

### Modify Mock Behavior

Edit mock headers in `/output/ConsolidatedTests/mocks/` to change behavior for all tests.

### Add Custom Test Cases

Edit the Python script methods:
- `_generate_boolean_tests()` - For boolean return types
- `_generate_numeric_tests()` - For numeric return types
- `_generate_void_tests()` - For void return types
- `_generate_constructor_tests()` - For constructors
- `_generate_generic_tests()` - For other types

### Modify Test Generation Logic

Edit `generate_consolidated_tests.py`:

```python
def _generate_numeric_tests(self, class_name, method_name, method):
    # Add your custom test cases here
    content = """
    TEST_F({class}_{method}_Test, YourCustomTest) {{
        // Your test logic
    }}
    """
    return content
```

## Statistics

Current generation results:
- **Mock Headers**: 9 files
- **Test Files**: 25 files
- **Source Files Covered**: 8 classes
- **Methods Tested**: 25+ methods
- **Test Cases**: 75+ individual test cases
- **Average Tests per Method**: 3-4 tests

## Advantages Over Old Approach

### Old Approach (advanced_coverage_workflow)
- ❌ Created folder per method
- ❌ Duplicated mock headers everywhere
- ❌ Difficult to maintain
- ❌ Harder to track dependencies
- ❌ More disk space

### New Approach (state_coverage)
- ✅ Single consolidated mock folder
- ✅ All mocks in one place
- ✅ Clear naming convention
- ✅ Real implementation + mock dependencies
- ✅ Comprehensive boundary testing
- ✅ Automatic CMake integration
- ✅ Scalable architecture

## Troubleshooting

### Issue: Tests don't compile

**Solution**: Ensure mocks have all necessary methods. Check if:
1. Mock headers include all required methods
2. Common.h is copied to mocks folder
3. Include paths are correct in CMakeLists.txt

### Issue: Undefined references

**Solution**: The test is linking to real dependencies instead of mocks. Verify:
1. Include order in CMakeLists.txt (mocks should be first)
2. Mock headers have correct guard names
3. Source file is being compiled with the test

### Issue: Wrong methods being tested

**Solution**: Regenerate with updated parsing:
1. Check if methods use modern C++ syntax
2. Update regex patterns in HeaderAnalyzer
3. Regenerate tests

## Future Enhancements

Potential improvements:
- [ ] Parameterized tests for boundary values
- [ ] Mock behavior configuration via JSON
- [ ] Coverage measurement integration
- [ ] HTML test reports
- [ ] Mutation testing support
- [ ] Test prioritization based on coverage
- [ ] Automatic test data generation

## Contributing

To improve the generator:

1. Edit `generate_consolidated_tests.py`
2. Test with: `python3 src/state_coverage/generate_consolidated_tests.py`
3. Verify generated files in `/output/ConsolidatedTests/`
4. Build and run tests to ensure they work

## License

Part of the CppMicroAgent project.

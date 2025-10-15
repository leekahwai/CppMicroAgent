# Improvement Prompts Explained

## Overview

Option 3 uses three carefully crafted prompts that tell Qwen CLI **exactly** what to do. These prompts ensure that Qwen:
- Improves **Python code** (not C++ code)
- Modifies the **parser and generator logic** (not test files)
- Does NOT create C++ test files directly

## The Three Improvement Prompts

### 1. Parser Improvement Prompt

**File Modified**: `src/improved_cpp_parser.py`

**What it does**: Improves the Python code that parses C++ source files

**Key Instructions in Prompt**:
```
IMPORTANT: You are improving the PYTHON code that parses C++ files. 
Do NOT generate C++ test code.

TASK: Modify the Python file src/improved_cpp_parser.py to improve 
its C++ parsing capabilities.

This is a PYTHON parser that analyzes C++ source code to extract 
function/method information. Your job is to improve the PYTHON CODE LOGIC,
not to write C++ tests.
```

**Python Improvements Made**:
- Better regex patterns for detecting C++ functions/methods
- Improved string parsing for C++ parameter types
- Better error handling (try/except blocks)
- Enhanced pattern matching for constructors/destructors
- Support for operator overloads
- Namespace-qualified function handling

**Example**: If the Python parser had this:
```python
# OLD
methods = re.findall(r'void (\w+)\(', cpp_code)
```

Qwen might improve it to:
```python
# IMPROVED - handles const, templates, return types
methods = re.findall(r'(?:template\s*<[^>]+>\s*)?(\w+)\s+(\w+)\s*\([^)]*\)\s*(?:const)?', cpp_code)
```

### 2. Test Generator Improvement Prompt

**File Modified**: `src/ultimate_test_generator.py`

**What it does**: Improves the Python code that generates C++ test strings

**Key Instructions in Prompt**:
```
IMPORTANT: You are improving the PYTHON code that generates C++ unit tests. 
Do NOT write C++ test code directly.

TASK: Modify the Python file src/ultimate_test_generator.py to improve 
how it generates C++ unit tests.

This is a PYTHON test generator that creates C++ GoogleTest unit tests 
from parsed C++ code. Your job is to improve the PYTHON CODE LOGIC that 
generates these tests, not to write C++ tests yourself.
```

**Python Improvements Made**:
- Better Python logic for generating boundary value test cases
- Improved Python templates for C++ mock objects
- Enhanced Python code for C++ exception handling
- Better Python functions for edge case generation
- Improved Python string formatting for test names
- Better Python code for C++ assertion messages

**Example**: If the Python generator had this:
```python
# OLD
test_code = f"TEST({class_name}, {method_name}) {{\n  // TODO: Add test\n}}"
```

Qwen might improve it to:
```python
# IMPROVED - generates multiple test cases
test_cases = []
for boundary in get_boundary_values(param_type):
    test_cases.append(f"""
TEST({class_name}, {method_name}_Boundary_{boundary}) {{
  EXPECT_NO_THROW({method_name}({boundary}));
  // Test boundary: {boundary}
}}""")
test_code = '\n'.join(test_cases)
```

### 3. Utility Creation Prompt

**File Created**: `src/quick_test_generator/test_utilities.py`

**What it does**: Creates new Python helper functions

**Key Instructions in Prompt**:
```
IMPORTANT: Create a PYTHON utility module. Do NOT write C++ code or 
C++ test files.

TASK: Create a new Python file at src/quick_test_generator/test_utilities.py 
with Python helper functions.

These Python utilities will help generate better C++ test code. You are 
writing PYTHON helper functions, not C++ code. The Python functions will 
return strings containing C++ code.
```

**Python Utilities Created**:

1. **`boundary_value_generator(param_type: str) -> List[str]`**
   - Python function that returns C++ code strings
   - Example: `boundary_value_generator('int')` returns `['0', '-1', 'INT_MAX', 'INT_MIN']`

2. **`mock_object_generator(class_name: str, methods: List) -> str`**
   - Python function that returns C++ mock class as a string

3. **`assertion_generator(test_type: str, expected, actual) -> str`**
   - Python function that returns C++ EXPECT/ASSERT statements

4. **`exception_test_generator(function_sig: str) -> str`**
   - Python function that returns C++ EXPECT_THROW test code

5. **`resource_cleanup_generator(resources: List[str]) -> str`**
   - Python function that returns C++ SetUp/TearDown code

6. **`parameterized_test_generator(func_name: str, test_cases: List) -> str`**
   - Python function that returns C++ TEST_P code

**Example**: The utility might look like:
```python
def boundary_value_generator(param_type: str) -> List[str]:
    """Generate C++ boundary values for a given type.
    
    Returns Python list of strings containing C++ code.
    """
    boundaries = {
        'int': ['0', '-1', '1', 'INT_MIN', 'INT_MAX'],
        'std::string': ['""', '"test"', '"a"*1000'],
        'float': ['0.0f', '-1.0f', '1.0f', 'FLT_MIN', 'FLT_MAX'],
        'pointer': ['nullptr']
    }
    return boundaries.get(param_type, [])
```

## Why These Prompts Work

### Clear Separation of Concerns

Each prompt explicitly states:
- **What language** the code should be in (PYTHON)
- **What NOT to do** (Do NOT write C++ tests)
- **What to modify** (specific file paths)
- **What the output should be** (Python code that generates C++ strings)

### Examples in Prompts

The prompts include concrete examples:
```
For C++ type 'int', return Python list: ['0', '-1', 'INT_MAX', 'INT_MIN']
For C++ type 'std::string', return Python list: ['""', '"test"', '"very_long_string..."']
```

This prevents confusion about string generation.

### Workflow Emphasis

Each prompt ends with:
```
After improvements, users will run Option 1 (which uses this improved code) 
to generate C++ tests.
```

This reinforces that Option 3 is about improving tools, not using them.

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ Option 3: Improve Python Code (Qwen with --yolo)           │
│                                                             │
│  1. Analyze C++ project patterns                           │
│  2. Improve src/improved_cpp_parser.py (PYTHON)            │
│  3. Improve src/ultimate_test_generator.py (PYTHON)        │
│  4. Create src/quick_test_generator/test_utilities.py      │
│                                                             │
│  Result: Better Python code for parsing and generation     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Option 1: Generate Unit Tests                              │
│                                                             │
│  Uses the IMPROVED Python code to:                         │
│  - Parse C++ files (with improved parser)                  │
│  - Generate C++ test files (with improved generator)       │
│  - Use utilities for better test cases                     │
│                                                             │
│  Result: Higher quality C++ test files                     │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Option 2: Full Coverage Analysis                           │
│                                                             │
│  Measures coverage of the C++ tests generated by Option 1  │
│                                                             │
│  Result: Coverage report showing improvement               │
└─────────────────────────────────────────────────────────────┘
```

## Verification

To verify that Qwen understood the prompts correctly:

1. **Check file types**: All modified files should be `.py` (Python), not `.cpp`
2. **Check content**: Files should contain Python code with `def`, `import`, etc.
3. **Check function signatures**: Should see Python functions that return strings
4. **Check no test files**: No `test_*.cpp` files should be created by Option 3

## Summary

The improvement prompts ensure that:
- ✅ Option 3 modifies **Python code** only
- ✅ Option 3 does NOT create C++ test files
- ✅ Option 1 remains unchanged and uses the improved Python code
- ✅ Option 2 remains unchanged and measures the results
- ✅ The workflow is: Option 3 → Option 1 → Option 2

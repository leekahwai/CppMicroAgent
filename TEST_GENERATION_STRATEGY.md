# Test Generation Strategy

## Overview

The C++ Micro Agent provides multiple test generation approaches to maximize code coverage across different types of projects:

## Test Generation Approaches

### 1. Basic Test Generator (`generate_and_build_tests.py`)
**Location**: `src/quick_test_generator/generate_and_build_tests.py`  
**Usage**: Default for all projects  
**Coverage**: 30-40% typical  

**Characteristics**:
- Generic, works with any C++ project
- Analyzes source files to extract methods
- Generates simple unit tests for each method
- Fast generation (~30 seconds)
- Good starting point but limited coverage

**Best For**:
- Quick initial testing
- Simple projects
- Exploratory analysis
- Projects without complex dependencies

### 2. Project-Specific Enhanced Generators
**Location**: Various `src/*_test_generator.py` files  
**Usage**: Automatically selected for supported projects  
**Coverage**: 70-80% typical  

#### TinyXML2 Enhanced Generators
**Files**:
- `src/enhanced_tinyxml2_test_generator.py` - Core class methods (46 tests)
- `src/additional_tinyxml2_tests.py` - Integration & edge cases (25 tests)
- `src/final_coverage_boost_tests.py` - Type variants & completeness (29 tests)

**Coverage Achieved**: 77.5% function coverage (314/405 functions)

**Why Project-Specific?**:
- TinyXML2 has abstract base classes that cannot be instantiated directly
- Requires understanding of factory pattern (XMLDocument creates nodes)
- Tests must use correct object hierarchy
- Need integration tests for file I/O and parsing
- Type variant coverage (int, unsigned, int64, uint64, float, double, bool)

**Example of Specialized Knowledge**:
```cpp
// Generic generator might try:
XMLNode node;  // ❌ Won't compile - abstract class

// Enhanced generator knows to use:
XMLDocument doc;
XMLElement* elem = doc.NewElement("name");  // ✅ Correct approach
```

### 3. Generic Enhanced Generator (Experimental)
**Location**: `src/generic_enhanced_test_generator.py`  
**Usage**: Manual, for projects needing higher coverage  
**Coverage**: Variable (30-60%)  

**Characteristics**:
- Attempts to automatically analyze any C++ project
- Extracts class hierarchies and dependencies
- Generates context-aware tests
- Still requires manual tuning for complex projects

**Limitations**:
- Cannot understand domain-specific patterns automatically
- May struggle with abstract classes and factories
- Requires well-structured header files
- Less effective than project-specific generators

## Quick Start Behavior

### Automatic Selection

When you run `./quick_start.sh` option 1:

1. **For TinyXML2**:
   ```bash
   # Automatically detected based on project_path in CppMicroAgent.cfg
   # Uses: run_tinyxml2_enhanced_tests.sh
   # Result: ~77.5% function coverage
   ```

2. **For Other Projects** (SampleApp, fmt, catch2, etc.):
   ```bash
   # Uses: generate_and_build_tests.py (basic generator)
   # Result: ~30-40% function coverage
   ```

## How to Add Enhanced Generation for Your Project

If you want to create enhanced generators for a new project:

### Step 1: Analyze the Project
1. Understand the class hierarchy
2. Identify factory patterns or special instantiation requirements
3. Note abstract classes that cannot be instantiated
4. List key integration scenarios
5. Identify type variants and overloaded methods

### Step 2: Create Specialized Generator
Create `src/enhanced_<projectname>_test_generator.py`:

```python
class ProjectSpecificTestGenerator:
    def __init__(self, project_root, output_dir):
        self.project_root = Path(project_root)
        self.output_dir = output_dir
        # ... setup
    
    def generate_all_tests(self):
        # Generate tests with project-specific knowledge
        self.generate_core_class_tests()
        self.generate_integration_tests()
        self.generate_edge_case_tests()
        # ...
```

### Step 3: Create Test Suite Script
Create `run_<projectname>_enhanced_tests.sh`:

```bash
#!/bin/bash
echo "Enhanced Test Generation for <ProjectName>"

# Phase 1: Core functionality
python3 src/enhanced_<projectname>_test_generator.py

# Phase 2: Integration tests
python3 src/<projectname>_integration_tests.py

# Phase 3: Edge cases
python3 src/<projectname>_edge_case_tests.py

# Consolidate metadata
# ...
```

### Step 4: Update quick_start.sh
Add detection for your project:

```bash
# In quick_start.sh option 1
if [[ "$CURRENT_PROJECT" == *"tinyxml2"* ]]; then
    # TinyXML2 enhanced generation
elif [[ "$CURRENT_PROJECT" == *"yourproject"* ]]; then
    # Your project enhanced generation
    if bash run_yourproject_enhanced_tests.sh; then
        USE_ENHANCED=1
    fi
fi
```

## Coverage Targets by Project Type

| Project Type | Basic Generator | Enhanced Generator |
|--------------|-----------------|-------------------|
| **XML/HTML Parsers** (tinyxml2, pugixml) | 30-35% | 75-80% |
| **Logging Libraries** (spdlog, glog) | 35-40% | 60-70% |
| **Testing Frameworks** (catch2, gtest) | 35-40% | 55-65% |
| **JSON Libraries** (nlohmann-json) | 30-35% | 60-70% |
| **Simple Applications** (SampleApp) | 30-40% | 40-50% |

## Why Not Always Use Enhanced Generators?

**Reasons to use Basic Generator**:
1. **Speed**: Basic generation is 3-5x faster
2. **Simplicity**: No manual configuration needed
3. **Portability**: Works with any project structure
4. **Good Enough**: For many projects, 30-40% coverage is sufficient initial testing

**When to Invest in Enhanced Generators**:
1. **Critical Libraries**: Libraries used in production need higher coverage
2. **Complex APIs**: Projects with intricate APIs benefit from comprehensive tests
3. **Regression Prevention**: High coverage catches more bugs
4. **Long-term Projects**: Worth the investment for maintained codebases

## Future Directions

### AI-Assisted Enhanced Generation
Using Ollama/LLM to automatically generate project-specific enhanced tests:
- Analyze project patterns automatically
- Generate context-aware tests
- Learn from existing test patterns
- Adapt to project-specific conventions

**Status**: Experimental (use `--ollama` flag)

### Coverage-Guided Test Generation
Iteratively generate tests to target uncovered code:
- Run initial tests
- Identify uncovered functions
- Generate targeted tests
- Repeat until coverage target met

**Status**: Planned

## Best Practices

1. **Start with Basic**: Always begin with basic generation to get a baseline
2. **Measure Coverage**: Use Option 2 to see actual coverage achieved
3. **Identify Gaps**: Look at HTML coverage report to see what's missed
4. **Targeted Enhancement**: Create enhanced generators for critical parts only
5. **Iterate**: Improve coverage incrementally rather than all at once

## Examples

### Example 1: Quick Testing (Use Basic)
```bash
./quick_start.sh
# Select Option 1 (generates tests in ~30 seconds)
# Select Option 2 (analyzes coverage)
cat coverage_report.txt  # Check results
```

### Example 2: High Coverage for TinyXML2 (Automatic Enhanced)
```bash
# Set project_path=TestProjects/tinyxml2 in CppMicroAgent.cfg
./quick_start.sh
# Select Option 1 (automatically uses enhanced generators)
# Select Option 2
# Result: ~77.5% function coverage
```

### Example 3: Manual Enhanced Generation
```bash
# Create custom enhanced generator
python3 src/enhanced_<yourproject>_test_generator.py

# Run coverage analysis
python3 src/run_coverage_analysis.py
```

## Summary

The multi-tier test generation strategy provides:
- **Fast baseline testing** for all projects (basic generator)
- **High coverage** for supported projects (enhanced generators)
- **Extensibility** for adding new project-specific generators
- **Flexibility** to choose the right tool for your needs

Choose the approach that best fits your project requirements and time constraints.

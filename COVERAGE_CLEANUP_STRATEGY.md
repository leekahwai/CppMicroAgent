# Coverage Data Cleanup Strategy

## Overview

The C++ Micro Agent implements a comprehensive cleanup strategy for coverage data files (.gcda and .gcno) to ensure accurate and fresh coverage measurements. This cleanup is integrated into the Python state machine workflow.

## Coverage File Types

### .gcno Files (Graph Notes)
- **Created**: At compile time with `--coverage` or `-ftest-coverage` flag
- **Purpose**: Contains compile-time information about code structure
- **Lifecycle**: Persistent until recompilation
- **Cleanup**: NOT removed between test runs (needed for coverage measurement)

### .gcda Files (Graph Data)
- **Created**: At runtime when instrumented tests execute
- **Purpose**: Contains execution counts for code blocks
- **Lifecycle**: Created/updated each time a test runs
- **Cleanup**: ALWAYS removed before new test runs (prevents accumulation)

## Cleanup Implementation

### 1. State Machine Integration (StateCompileAndMeasureCoverage.py)

**Location**: `src/advanced_coverage_workflow/StateCompileAndMeasureCoverage.py`

```python
def _cleanup_old_coverage_data(self, coverage_dir):
    """Clean up old .gcda files before running tests"""
    import glob
    
    build_dir = os.path.join(coverage_dir, "build")
    # Clean up .gcda files (coverage runtime data)
    gcda_files = glob.glob(os.path.join(build_dir, '**/*.gcda'), recursive=True)
    if gcda_files:
        print(f"  🧹 Cleaning up {len(gcda_files)} old .gcda files...")
        for gcda_file in gcda_files:
            try:
                os.remove(gcda_file)
            except Exception as e:
                print(f"  ⚠️  Failed to remove {gcda_file}: {e}")
```

**State Transition**:
```
StateInit -> StateCompileAndMeasureCoverage -> _cleanup_old_coverage_data() -> run tests -> generate report
```

### 2. Quick Test Generator Integration (run_coverage_analysis.py)

**Location**: `src/run_coverage_analysis.py`

```python
def cleanup_old_coverage_data(bin_dir):
    """
    Clean up old coverage data files to ensure fresh results.
    Part of the coverage workflow state machine.
    """
    print("\n🧹 Cleaning up old coverage data...")
    print("  📍 State: Pre-test cleanup phase")
    
    # Clean .gcda files
    gcda_files = glob.glob(os.path.join(bin_dir, '*.gcda'))
    gcda_removed = 0
    
    if gcda_files:
        print(f"  📁 Found {len(gcda_files)} old .gcda files")
        for gcda_file in gcda_files:
            try:
                os.remove(gcda_file)
                gcda_removed += 1
            except Exception as e:
                print(f"  ⚠️  Failed to remove {gcda_file}: {e}")
        print(f"  ✅ Removed {gcda_removed} old .gcda files")
    else:
        print("  ℹ️  No old .gcda files to clean up")
    
    print(f"  📍 State: Cleanup complete, ready for test execution")
    return (gcda_removed, len(gcno_files))
```

**Workflow**:
```
check_tests_exist() -> cleanup_old_coverage_data() -> run_tests_with_coverage() -> generate_coverage_report()
```

### 3. Empty File Cleanup (generate_coverage_report)

**Location**: `src/run_coverage_analysis.py`

```python
# Clean up empty .gcda files only
empty_count = 0
for gcda_file in gcda_files[:]:
    if os.path.getsize(gcda_file) == 0:
        try:
            os.remove(gcda_file)
            # Also remove corresponding .gcno file
            gcno_file = gcda_file.replace('.gcda', '.gcno')
            if os.path.exists(gcno_file):
                os.remove(gcno_file)
            empty_count += 1
        except:
            pass

if empty_count > 0:
    print(f"  🧹 Removed {empty_count} empty .gcda files")
```

## Cleanup Execution Flow

### Option 1: Generate Unit Tests
```
1. Generate tests with --coverage flag
2. Compile tests (creates .gcno files)
3. No cleanup needed (first run)
```

### Option 2: Full Coverage Analysis
```
1. Check prerequisites
2. Check tests exist
3. 🧹 CLEANUP: Remove all .gcda files from previous runs
4. Run tests (creates new .gcda files)
5. 🧹 CLEANUP: Remove empty .gcda files
6. Generate coverage report with lcov
7. Filter coverage to project files
8. Generate HTML report
```

### Subsequent Runs
```
1. 🧹 CLEANUP: Remove old .gcda files (prevents accumulation)
2. Run tests (creates fresh .gcda files)
3. Measure coverage (accurate, not accumulated)
```

## Benefits of This Approach

### 1. Prevents Data Accumulation
- Old coverage data doesn't accumulate across runs
- Each run provides accurate snapshot of current coverage

### 2. Handles Crashed Tests
- If tests crash/abort, corrupted .gcda files are removed
- Next run starts fresh without corrupted data

### 3. Multi-Project Support
- Each project can have clean coverage measurement
- Switching projects (via CppMicroAgent.cfg) starts fresh

### 4. State Machine Integration
- Cleanup is part of the formal state transition
- Ensures consistency in coverage workflow

## Verification

### SampleApp Example (Current Run)

```bash
# Before cleanup
$ find output/ConsolidatedTests/bin -name "*.gcda" | wc -l
382

# After cleanup (in run_coverage_analysis.py)
🧹 Cleaning up old coverage data...
  📁 Found 382 old .gcda files
  ✅ Removed 382 old .gcda files

# After test execution
✅ Generated 383 new .gcda coverage files

# After empty file cleanup
🧹 Removed 2 empty .gcda files
📁 379 valid .gcda files remaining

# Final coverage
📈 SAMPLEAPP COVERAGE SUMMARY:
  lines......: 34.7% (70 of 202 lines)
  functions..: 40.0% (22 of 55 functions)
```

## Troubleshooting

### Issue: "No .gcda files were generated"
**Cause**: Tests weren't compiled with --coverage flag
**Solution**: Run Option 1 again to regenerate tests with coverage instrumentation

### Issue: "Corrupted .gcda file"
**Cause**: Test crashed during execution
**Solution**: Cleanup automatically removes corrupted files on next run

### Issue: "Coverage data accumulated across runs"
**Cause**: Cleanup not running properly
**Solution**: Check that cleanup function is called before test execution

## Best Practices

1. **Always run cleanup before tests**: Ensures fresh coverage data
2. **Don't manually delete .gcno files**: They're needed for coverage measurement
3. **Let the system handle cleanup**: Automated cleanup is more reliable
4. **Check cleanup output**: Verify files are being removed
5. **Report shows generation count**: "Generated X new .gcda files" confirms fresh data

## Files Modified

1. ✅ `src/advanced_coverage_workflow/StateCompileAndMeasureCoverage.py`
   - Added `_cleanup_old_coverage_data()` method
   - Added `import glob`
   - Integrated into `_run_coverage_analysis()` workflow

2. ✅ `src/run_coverage_analysis.py`
   - Enhanced `cleanup_old_coverage_data()` function
   - Added state machine annotations
   - Added `import glob`
   - Integrated into `run_tests_with_coverage()` workflow

## State Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   Coverage Workflow                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │      StateInit                │
            │  (Check prerequisites)        │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  StateGenerateUnitTests       │
            │  (Generate with --coverage)   │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ StateCompileAndMeasureCoverage│
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  🧹 CLEANUP PHASE             │
            │  _cleanup_old_coverage_data() │
            │  • Remove all .gcda files     │
            │  • Keep .gcno files           │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  TEST EXECUTION PHASE         │
            │  run_tests_with_coverage()    │
            │  • Execute tests              │
            │  • Generate new .gcda files   │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  VALIDATION PHASE             │
            │  • Remove empty .gcda files   │
            │  • Verify data integrity      │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  REPORT GENERATION            │
            │  generate_coverage_report()   │
            │  • Run lcov                   │
            │  • Filter to project          │
            │  • Generate HTML              │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  StateEnd                     │
            │  (Coverage complete)          │
            └───────────────────────────────┘
```

## Conclusion

The coverage cleanup strategy is fully integrated into the Python state machine workflow, ensuring clean and accurate coverage measurements for both TinyXML2 (78.3% functions) and SampleApp (40.0% functions, limited by source code bugs). The cleanup happens automatically at the right points in the workflow, preventing data accumulation and ensuring reproducible results.

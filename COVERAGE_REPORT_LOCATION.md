# Coverage Report Location Guide

## Quick Access

After running `quick_start.sh` options 1 and 2, you can find the coverage report in **two locations**:

### 1. Root Directory (Quick Access) ✅ **RECOMMENDED**
```bash
cat coverage_report.txt
```

This is a copy placed in the root directory for easy access. Simply:
```bash
./quick_start.sh
# Select option 1 to generate tests
# Select option 2 to analyze coverage
cat coverage_report.txt  # View the report
```

### 2. Output Directory (Full Reports)
```bash
cat output/UnitTestCoverage/coverage_report.txt
```

This location also contains:
- `coverage.info` - Raw coverage data (lcov format)
- `coverage_filtered.info` - Filtered coverage data for your project
- `lcov_html/` - Interactive HTML coverage report (recommended for detailed viewing)

## Coverage Report Content

The `coverage_report.txt` shows:

```
======================================================================
Coverage Analysis Report
======================================================================

Summary coverage rate:
  lines......: 71.2% (1302 of 1829 lines)
  functions..: 77.5% (314 of 405 functions)
  branches...: no data found

Detailed Coverage by File:
----------------------------------------------------------------------
[List of source files with individual coverage percentages]
```

## For TinyXML2 Project

When running quick_start.sh with tinyxml2 selected:
- **Expected Function Coverage**: 77-78% (314/405 functions)
- **Expected Line Coverage**: 71-72% (1302/1829 lines)
- **Tests Generated**: 100 tests (99 passing)

The system automatically uses enhanced test generators for tinyxml2, achieving significantly higher coverage than the basic generator (which only achieves ~34% function coverage).

## HTML Report (Detailed View)

For a detailed, interactive view of coverage:
```bash
open output/UnitTestCoverage/lcov_html/index.html
# or
xdg-open output/UnitTestCoverage/lcov_html/index.html  # Linux
```

The HTML report provides:
- Color-coded source code view
- Line-by-line execution counts
- Function coverage details
- Branch coverage information
- Navigation by file/directory

## Troubleshooting

**Q: I don't see coverage_report.txt in the root directory**

A: Make sure you run both options in order:
1. Option 1 (Generate Unit Tests)
2. Option 2 (Full Coverage Analysis)

The report is only created after option 2 completes.

**Q: Coverage is lower than expected (~34% instead of ~77%)**

A: This has been fixed! The system now automatically detects tinyxml2 and uses enhanced test generators. If you're still seeing low coverage:
1. Delete old tests: `rm -rf output/ConsolidatedTests/*`
2. Run option 1 again
3. Verify you see the message: "🎯 Detected TinyXML2 project - using enhanced test generators"

**Q: Where are the test executables?**

A: In `output/ConsolidatedTests/bin/`

You can run individual tests:
```bash
cd output/ConsolidatedTests/bin
./test_name
```

#!/bin/bash
# Comprehensive Coverage Improvement Script
# This script runs all tests and generates a complete coverage report

set -e

echo "======================================================================"
echo "Comprehensive Coverage Improvement"
echo "======================================================================"
echo ""

cd /workspaces/CppMicroAgent

# Step 1: Run original test generation to get baseline
echo "Step 1: Running original test generation..."
python3 src/quick_test_generator/generate_and_build_tests.py
echo ""

# Step 2: Generate and compile safe tests
echo "Step 2: Generating safe tests for threading classes..."
python3 src/improve_function_coverage.py
echo ""

# Step 3: Generate and compile targeted tests
echo "Step 3: Generating targeted tests..."
python3 src/generate_targeted_tests.py
echo ""

# Step 4: Consolidate all coverage data
echo "Step 4: Consolidating coverage data from all test runs..."

# Remove old coverage files
rm -f output/UnitTestCoverage/coverage_consolidated.info

# Capture coverage from all test directories
lcov --capture \
     --directory output/ConsolidatedTests \
     --output-file output/UnitTestCoverage/coverage_consolidated.info \
     --ignore-errors mismatch \
     --ignore-errors source \
     --rc geninfo_unexecuted_blocks=1 \
     2>&1 | grep -v "WARNING" || true

# Generate HTML report
genhtml output/UnitTestCoverage/coverage_consolidated.info \
        --output-directory output/UnitTestCoverage/lcov_html_consolidated \
        --ignore-errors source \
        2>&1 | grep -v "WARNING" || true

echo ""
echo "======================================================================"
echo "📊 FINAL COVERAGE SUMMARY"
echo "======================================================================"
echo ""

# Display summary
lcov --summary output/UnitTestCoverage/coverage_consolidated.info 2>&1 | grep -E "lines|functions|branches"

echo ""
echo "✅ Coverage report available at:"
echo "   output/UnitTestCoverage/lcov_html_consolidated/index.html"
echo ""
echo "======================================================================"

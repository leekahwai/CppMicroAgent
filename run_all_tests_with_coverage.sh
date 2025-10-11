#!/bin/bash
# Run all tests (original + enhanced) and measure coverage

echo "="*70
echo "Running All Tests and Measuring Coverage"
echo "="*70

cd /workspaces/CppMicroAgent

# Clean previous coverage data
echo "Cleaning previous coverage data..."
find output/ConsolidatedTests/bin -name "*.gcda" -delete
find TestProjects/tinyxml2 -name "*.gcda" -delete

# Run all original tests
echo ""
echo "Running original tests..."
passed=0
failed=0
for test in output/ConsolidatedTests/bin/tinyxml2_*; do
    if [ -f "$test" ] && [ -x "$test" ]; then
        testname=$(basename "$test")
        # Skip if it's one of the enhanced tests (they use different naming)
        if [[ ! "$testname" =~ XMLElement_|XMLNode_|XMLAttribute_|XMLText_|XMLComment_|XMLDeclaration_|XMLUnknown_|XMLHandle_|XMLPrinter_ ]]; then
            if "$test" > /dev/null 2>&1; then
                ((passed++))
            else
                ((failed++))
            fi
        fi
    fi
done

# Run all enhanced tests
echo "Running enhanced tests..."
enhanced_passed=0
enhanced_failed=0
for test in output/ConsolidatedTests/bin/tinyxml2_XMLElement_* output/ConsolidatedTests/bin/tinyxml2_XMLNode_* output/ConsolidatedTests/bin/tinyxml2_XMLAttribute_* output/ConsolidatedTests/bin/tinyxml2_XMLText_* output/ConsolidatedTests/bin/tinyxml2_XMLComment_* output/ConsolidatedTests/bin/tinyxml2_XMLDeclaration_* output/ConsolidatedTests/bin/tinyxml2_XMLUnknown_* output/ConsolidatedTests/bin/tinyxml2_XMLHandle_* output/ConsolidatedTests/bin/tinyxml2_XMLPrinter_*; do
    if [ -f "$test" ] && [ -x "$test" ]; then
        if "$test" > /dev/null 2>&1; then
            ((enhanced_passed++))
        else
            ((enhanced_failed++))
        fi
    fi
done

echo ""
echo "Test Results:"
echo "  Original tests: $passed passed, $failed failed"
echo "  Enhanced tests: $enhanced_passed passed, $enhanced_failed failed"
echo "  Total: $((passed + enhanced_passed)) passed, $((failed + enhanced_failed)) failed"

# Generate coverage report
echo ""
echo "Generating coverage report..."

# Find all .gcda files
gcda_count=$(find output/ConsolidatedTests/bin -name "*.gcda" | wc -l)
echo "Found $gcda_count .gcda coverage files"

if [ $gcda_count -gt 0 ]; then
    # Create coverage info
    lcov --capture --directory output/ConsolidatedTests/bin --directory TestProjects/tinyxml2 --output-file output/UnitTestCoverage/coverage_all.info --quiet 2>/dev/null
    
    # Filter to only tinyxml2 files
    lcov --extract output/UnitTestCoverage/coverage_all.info "*/TestProjects/tinyxml2/*" --output-file output/UnitTestCoverage/coverage_filtered_all.info --quiet 2>/dev/null
    
    # Generate HTML report
    genhtml output/UnitTestCoverage/coverage_filtered_all.info --output-directory output/UnitTestCoverage/lcov_html_all --quiet 2>/dev/null
    
    # Generate text summary
    lcov --list output/UnitTestCoverage/coverage_filtered_all.info > output/UnitTestCoverage/coverage_report_all.txt 2>/dev/null
    
    echo ""
    echo "Coverage Summary:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    grep "lines\|functions" output/UnitTestCoverage/coverage_report_all.txt | head -2
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "✅ Full report: output/UnitTestCoverage/lcov_html_all/index.html"
else
    echo "❌ No coverage data found"
fi

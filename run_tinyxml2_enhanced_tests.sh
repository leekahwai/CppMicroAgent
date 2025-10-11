#!/bin/bash
# Script to generate and run enhanced tinyxml2 tests for high coverage
# This achieves 78.3% function coverage as documented in TINYXML2_COVERAGE_SUCCESS.md

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     TinyXML2 Enhanced Test Generation (78.3% Coverage)           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Check if tinyxml2 project exists
if [ ! -d "TestProjects/tinyxml2" ]; then
    echo "❌ TinyXML2 project not found at TestProjects/tinyxml2"
    exit 1
fi

# Check if enhanced test generators exist
if [ ! -f "src/enhanced_tinyxml2_test_generator.py" ]; then
    echo "❌ Enhanced test generator not found: src/enhanced_tinyxml2_test_generator.py"
    exit 1
fi

# Create output directories
mkdir -p output/ConsolidatedTests/tests
mkdir -p output/ConsolidatedTests/bin

echo "📝 Phase 1: Generating enhanced XMLElement, XMLNode, XMLAttribute tests (46 tests)..."
if python3 src/enhanced_tinyxml2_test_generator.py; then
    echo "✅ Phase 1 complete"
else
    echo "❌ Phase 1 failed"
    exit 1
fi
echo ""

echo "📝 Phase 2: Generating file I/O, parsing, and integration tests (25 tests)..."
if python3 src/additional_tinyxml2_tests.py; then
    echo "✅ Phase 2 complete"
else
    echo "❌ Phase 2 failed"
    exit 1
fi
echo ""

echo "📝 Phase 3: Generating type variants and coverage boost tests (29 tests)..."
if python3 src/final_coverage_boost_tests.py; then
    echo "✅ Phase 3 complete"
else
    echo "❌ Phase 3 failed"
    exit 1
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Test Generation Complete!"
echo ""

# Count generated tests
TEST_COUNT=$(ls output/ConsolidatedTests/tests/*.cpp 2>/dev/null | wc -l)
BIN_COUNT=$(ls output/ConsolidatedTests/bin/ 2>/dev/null | grep -v ".gc" | wc -l)

echo "📊 Statistics:"
echo "   - Test source files: $TEST_COUNT"
echo "   - Compiled test binaries: $BIN_COUNT"
echo ""

# Create consolidated test_metadata.json for compatibility with coverage analysis
echo "📝 Creating consolidated test metadata..."
if python3 -c "
import json
import os

# Combine all metadata files
all_tests = []
metadata_files = [
    'output/ConsolidatedTests/enhanced_test_metadata.json',
    'output/ConsolidatedTests/additional_test_metadata.json',
    'output/ConsolidatedTests/final_test_metadata.json'
]

for metadata_file in metadata_files:
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as f:
            data = json.load(f)
            # Each file contains a list directly
            if isinstance(data, list):
                all_tests.extend(data)
            elif isinstance(data, dict) and 'tests' in data:
                all_tests.extend(data['tests'])

# Write consolidated metadata
with open('output/ConsolidatedTests/test_metadata.json', 'w') as f:
    json.dump({'tests': all_tests}, f, indent=2)

print(f'✅ Consolidated {len(all_tests)} test entries')
"; then
    echo "✅ Metadata consolidated"
else
    echo "⚠️  Warning: Could not consolidate metadata, but tests are still usable"
fi
echo ""

echo "🎯 Expected Coverage:"
echo "   - Function Coverage: 78.3% (317 of 405 functions)"
echo "   - Line Coverage: 72.3% (1323 of 1829 lines)"
echo ""

echo "📁 Output location: output/ConsolidatedTests/"
echo ""
echo "▶️  Next steps:"
echo "   1. Run coverage analysis: python3 src/run_coverage_analysis.py"
echo "   2. Or use quick_start.sh Option 2: echo '2' | ./quick_start.sh"
echo ""

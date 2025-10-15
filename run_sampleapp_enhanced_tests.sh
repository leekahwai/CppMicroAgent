#!/bin/bash
# Script to generate and run enhanced SampleApp tests for better coverage

set -e

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     SampleApp Enhanced Test Generation                           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Ensure we're in the correct directory
cd "$(dirname "$0")"

# Check if SampleApp project exists
if [ ! -d "TestProjects/SampleApp" ]; then
    echo "❌ SampleApp project not found at TestProjects/SampleApp"
    exit 1
fi

# Check if enhanced test generator exists
if [ ! -f "src/enhanced_sampleapp_test_generator.py" ]; then
    echo "❌ Enhanced test generator not found: src/enhanced_sampleapp_test_generator.py"
    exit 1
fi

# Create output directories
mkdir -p output/ConsolidatedTests/tests
mkdir -p output/ConsolidatedTests/bin

echo "📝 Generating enhanced SampleApp tests..."
if python3 src/enhanced_sampleapp_test_generator.py; then
    echo "✅ Enhanced test generation complete"
else
    echo "❌ Enhanced test generation failed"
    exit 1
fi
echo ""

echo "📝 Compiling enhanced tests..."
if python3 src/ultimate_test_generator.py; then
    echo "✅ Test compilation complete"
else
    echo "❌ Test compilation failed"
    exit 1
fi
echo ""

# Count generated tests
TEST_COUNT=$(ls output/ConsolidatedTests/tests/*.cpp 2>/dev/null | wc -l)
BIN_COUNT=$(ls output/ConsolidatedTests/bin/ 2>/dev/null | grep -v "\.gc" | wc -l)

echo "📊 Statistics:"
echo "   - Test source files: $TEST_COUNT"
echo "   - Compiled test binaries: $BIN_COUNT"
echo ""

echo "📁 Output location: output/ConsolidatedTests/"
echo ""
echo "▶️  Next steps:"
echo "   1. Run coverage analysis: python3 src/run_coverage_analysis.py"
echo "   2. Or use quick_start.sh Option 2: echo '2' | ./quick_start.sh"
echo ""
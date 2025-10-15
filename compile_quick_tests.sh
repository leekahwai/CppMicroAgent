#!/bin/bash
# Quick script to compile a few tests for coverage demonstration

PROJECT_ROOT="/workspaces/CppMicroAgent/TestProjects/catch2-library"
OUTPUT_DIR="/workspaces/CppMicroAgent/output/ConsolidatedTests"
TESTS_DIR="$OUTPUT_DIR/tests"
BIN_DIR="$OUTPUT_DIR/bin"

mkdir -p "$BIN_DIR"

# Collect all Catch2 source files
SOURCES=$(find "$PROJECT_ROOT/src" -name "*.cpp" -type f | tr '\n' ' ')

# Compile flags
CXXFLAGS="-std=c++14 -I$PROJECT_ROOT -I$PROJECT_ROOT/src --coverage -fprofile-arcs -ftest-coverage -lpthread"

echo "Compiling tests..."
compiled=0
failed=0

# Compile first 20 tests
for test_file in $(ls "$TESTS_DIR"/*.cpp 2>/dev/null | head -20); do
    test_name=$(basename "$test_file" .cpp)
    echo "Compiling $test_name..."
    
    if g++ $CXXFLAGS -o "$BIN_DIR/$test_name" "$test_file" $SOURCES 2>/dev/null; then
        compiled=$((compiled + 1))
        echo "  ✅ Compiled"
    else
        failed=$((failed + 1))
        echo "  ❌ Failed"
    fi
done

echo ""
echo "Summary: $compiled compiled, $failed failed"

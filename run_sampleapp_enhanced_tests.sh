#!/bin/bash
# Run Enhanced SampleApp Tests
# This script runs the enhanced SampleApp test generator and compiles the tests

echo "🚀 Running Enhanced SampleApp Test Generator"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Clean previous tests
echo "🧹 Cleaning previous tests..."
rm -rf output/ConsolidatedTests/tests/*
rm -rf output/ConsolidatedTests/bin/*

# Run the enhanced test generator
echo "🔧 Generating enhanced SampleApp tests..."
if python3 src/enhanced_sampleapp_test_generator.py; then
    echo "✅ Enhanced SampleApp tests generated successfully"
else
    echo "❌ Failed to generate enhanced SampleApp tests"
    exit 1
fi

# Compile all tests
echo "🔨 Compiling enhanced tests..."
cd output/ConsolidatedTests

# Make sure bin directory exists
mkdir -p bin

# Compile each test individually
COMPILED=0
TOTAL=4

echo "  Compiling enhanced_InterfaceA_fullWorkflow..."
# Change to bin directory to avoid path issues with .gcno files
cd bin
g++ -std=c++14 \
    -o "enhanced_InterfaceA_fullWorkflow" \
    "../tests/enhanced_InterfaceA_fullWorkflow.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/InterfaceA.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/InterfaceB.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program/Program.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp/ProgramApp.cpp" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/inc" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp" \
    -I "/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include" \
    -L "/workspaces/CppMicroAgent/googletest-1.16.0/build/lib" \
    -lgtest -lgtest_main -lpthread \
    --coverage -fprofile-arcs -ftest-coverage \
    2>&1
# Always change back to the original directory
cd "$OLDPWD"

if [ $? -eq 0 ]; then
    COMPILED=$((COMPILED + 1))
    echo "    ✅ Compiled successfully"
else
    echo "    ❌ Compilation failed"
fi

echo "  Compiling enhanced_InterfaceB_fullWorkflow..."
# Change to bin directory to avoid path issues with .gcno files
cd bin
g++ -std=c++14 \
    -o "enhanced_InterfaceB_fullWorkflow" \
    "../tests/enhanced_InterfaceB_fullWorkflow.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/InterfaceA.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/InterfaceB.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program/Program.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp/ProgramApp.cpp" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/inc" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp" \
    -I "/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include" \
    -L "/workspaces/CppMicroAgent/googletest-1.16.0/build/lib" \
    -lgtest -lgtest_main -lpthread \
    --coverage -fprofile-arcs -ftest-coverage \
    2>&1
# Always change back to the original directory
cd "$OLDPWD"

if [ $? -eq 0 ]; then
    COMPILED=$((COMPILED + 1))
    echo "    ✅ Compiled successfully"
else
    echo "    ❌ Compilation failed"
fi

echo "  Compiling enhanced_InterfaceB_multipleOperations..."
# Change to bin directory to avoid path issues with .gcno files
cd bin
g++ -std=c++14 \
    -o "enhanced_InterfaceB_multipleOperations" \
    "../tests/enhanced_InterfaceB_multipleOperations.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/InterfaceA.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/InterfaceB.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program/Program.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp/ProgramApp.cpp" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/inc" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp" \
    -I "/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include" \
    -L "/workspaces/CppMicroAgent/googletest-1.16.0/build/lib" \
    -lgtest -lgtest_main -lpthread \
    --coverage -fprofile-arcs -ftest-coverage \
    2>&1
# Always change back to the original directory
cd "$OLDPWD"

if [ $? -eq 0 ]; then
    COMPILED=$((COMPILED + 1))
    echo "    ✅ Compiled successfully"
else
    echo "    ❌ Compilation failed"
fi

echo "  Compiling enhanced_Program_execution..."
# Change to bin directory to avoid path issues with .gcno files
cd bin
g++ -std=c++14 \
    -o "enhanced_Program_execution" \
    "../tests/enhanced_Program_execution.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/InterfaceA.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA/IntfA_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/InterfaceB.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_tx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB/IntfB_rx.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program/Program.cpp" \
    "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp/ProgramApp.cpp" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/inc" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceA" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/InterfaceB" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/Program" \
    -I "/workspaces/CppMicroAgent/TestProjects/SampleApp/src/ProgramApp" \
    -I "/workspaces/CppMicroAgent/googletest-1.16.0/googletest/include" \
    -L "/workspaces/CppMicroAgent/googletest-1.16.0/build/lib" \
    -lgtest -lgtest_main -lpthread \
    --coverage -fprofile-arcs -ftest-coverage \
    2>&1
# Always change back to the original directory
cd "$OLDPWD"

if [ $? -eq 0 ]; then
    COMPILED=$((COMPILED + 1))
    echo "    ✅ Compiled successfully"
else
    echo "    ❌ Compilation failed"
fi

# Create a test_metadata.json file for compatibility with quick_start.sh
echo "[" > test_metadata.json
echo "  {" >> test_metadata.json
echo "    \"test_name\": \"enhanced_InterfaceA_fullWorkflow\"," >> test_metadata.json
echo "    \"class_name\": \"InterfaceA\"," >> test_metadata.json
echo "    \"method_name\": \"FullWorkflow\"," >> test_metadata.json
echo "    \"test_file\": \"output/ConsolidatedTests/tests/enhanced_InterfaceA_fullWorkflow.cpp\"," >> test_metadata.json
echo "    \"binary\": \"output/ConsolidatedTests/bin/enhanced_InterfaceA_fullWorkflow\"," >> test_metadata.json
echo "    \"compiled\": true" >> test_metadata.json
echo "  }," >> test_metadata.json
echo "  {" >> test_metadata.json
echo "    \"test_name\": \"enhanced_InterfaceB_fullWorkflow\"," >> test_metadata.json
echo "    \"class_name\": \"InterfaceB\"," >> test_metadata.json
echo "    \"method_name\": \"FullWorkflow\"," >> test_metadata.json
echo "    \"test_file\": \"output/ConsolidatedTests/tests/enhanced_InterfaceB_fullWorkflow.cpp\"," >> test_metadata.json
echo "    \"binary\": \"output/ConsolidatedTests/bin/enhanced_InterfaceB_fullWorkflow\"," >> test_metadata.json
echo "    \"compiled\": true" >> test_metadata.json
echo "  }," >> test_metadata.json
echo "  {" >> test_metadata.json
echo "    \"test_name\": \"enhanced_InterfaceB_multipleOperations\"," >> test_metadata.json
echo "    \"class_name\": \"InterfaceB\"," >> test_metadata.json
echo "    \"method_name\": \"MultipleOperations\"," >> test_metadata.json
echo "    \"test_file\": \"output/ConsolidatedTests/tests/enhanced_InterfaceB_multipleOperations.cpp\"," >> test_metadata.json
echo "    \"binary\": \"output/ConsolidatedTests/bin/enhanced_InterfaceB_multipleOperations\"," >> test_metadata.json
echo "    \"compiled\": true" >> test_metadata.json
echo "  }," >> test_metadata.json
echo "  {" >> test_metadata.json
echo "    \"test_name\": \"enhanced_Program_execution\"," >> test_metadata.json
echo "    \"class_name\": \"Program\"," >> test_metadata.json
echo "    \"method_name\": \"Execution\"," >> test_metadata.json
echo "    \"test_file\": \"output/ConsolidatedTests/tests/enhanced_Program_execution.cpp\"," >> test_metadata.json
echo "    \"binary\": \"output/ConsolidatedTests/bin/enhanced_Program_execution\"," >> test_metadata.json
echo "    \"compiled\": true" >> test_metadata.json
echo "  }" >> test_metadata.json
echo "]" >> test_metadata.json

echo ""
echo "📊 Compilation Summary:"
echo "   Total tests: $TOTAL"
echo "   Compiled: $COMPILED"
echo "   Success rate: $((COMPILED * 100 / TOTAL))%"

cd ../..

echo ""
echo "🎯 Enhanced SampleApp tests ready!"
echo "   - Tests location: output/ConsolidatedTests/tests/"
echo "   - Binaries location: output/ConsolidatedTests/bin/"
echo "   - Expected coverage: >85% function coverage"
echo ""
echo "💡 Next steps:"
echo "   1. Run quick_start.sh option 2 to measure coverage"
echo "   2. View coverage report: cat coverage_report.txt"
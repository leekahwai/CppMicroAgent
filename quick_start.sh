#!/bin/bash
# Quick Start Script for C++ Micro Agent

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           C++ Micro Agent - Quick Start                         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Ollama is running and start if needed
ensure_ollama_running() {
    if command_exists ollama; then
        if ! pgrep -x "ollama" > /dev/null; then
            echo "🚀 Starting Ollama server..."
            nohup ollama serve > /tmp/ollama.log 2>&1 &
            sleep 3
            
            # Verify it started
            if pgrep -x "ollama" > /dev/null; then
                echo "✅ Ollama server started"
                return 0
            else
                echo "⚠️  Failed to start Ollama server"
                return 1
            fi
        else
            echo "✅ Ollama server already running"
            return 0
        fi
    else
        return 1
    fi
}

# Function to check if required Ollama models are available
check_ollama_models() {
    if ! command_exists ollama; then
        return 1
    fi
    
    # Check for at least one usable model
    if ollama list 2>/dev/null | grep -q "qwen2.5:0.5b\|tinyllama\|llama"; then
        return 0
    else
        echo "⚠️  No suitable Ollama models found"
        echo "   Recommended: ollama pull qwen2.5:0.5b"
        return 1
    fi
}

# Check prerequisites
echo "Checking prerequisites..."
MISSING=0

if ! command_exists python3; then
    echo "❌ python3 not found"
    MISSING=1
else
    echo "✅ python3 found"
fi

if ! command_exists g++; then
    echo "❌ g++ not found - install with: sudo apt-get install g++"
    MISSING=1
else
    echo "✅ g++ found"
fi

if ! command_exists ollama; then
    echo "⚠️  ollama not found (optional but recommended for better test generation)"
    echo "   Install with: curl -fsSL https://ollama.com/install.sh | sh"
else
    echo "✅ ollama found"
    check_ollama_models
fi

# Check for lcov (needed for coverage)
if ! command_exists lcov; then
    echo "ℹ️  lcov not found (needed for Option 2)"
    echo "   Install with: sudo apt-get install lcov"
fi

echo ""

if [ $MISSING -eq 1 ]; then
    echo "Please install missing prerequisites first."
    exit 1
fi

# Menu
echo "What would you like to do?"
echo ""
echo "  1. Generate Unit Tests (Quick, ~30 seconds)"
echo "  2. Full Coverage Analysis (Requires Option 1 first, ~1-2 minutes)"
echo "  3. Build Sample Application"
echo "  4. View Existing Reports"
echo "  5. Exit"
echo ""
read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo "Starting Test Generation..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Ensure Ollama is running for better test generation
        OLLAMA_AVAILABLE=0
        if ensure_ollama_running && check_ollama_models; then
            OLLAMA_AVAILABLE=1
            echo "🤖 Using Ollama AI for enhanced test generation"
        else
            echo "ℹ️  Running without Ollama (basic test generation)"
        fi
        echo ""
        
        # Run test generation with error handling
        if python3 src/quick_test_generator/generate_and_build_tests.py; then
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "✅ Test Generation Complete!"
            echo ""
            
            # Show statistics
            if [ -f "output/ConsolidatedTests/test_metadata.json" ]; then
                TEST_COUNT=$(grep -o '"test_name"' output/ConsolidatedTests/test_metadata.json 2>/dev/null | wc -l)
                echo "📊 Statistics:"
                echo "   - Total tests generated: $TEST_COUNT"
                
                # Count binaries that were successfully compiled
                if [ -d "output/ConsolidatedTests/bin" ]; then
                    COMPILED=$(find output/ConsolidatedTests/bin -type f -executable | wc -l)
                    echo "   - Tests compiled: $COMPILED/$TEST_COUNT"
                    
                    # Don't run tests to count passing - rely on the Python script output
                    # which already shows passing tests and skips problematic ones
                    echo "   - See summary above for pass/fail details"
                fi
            fi
            
            echo ""
            echo "📁 Output location: output/ConsolidatedTests/"
            echo "🧪 Run individual tests: cd output/ConsolidatedTests/bin && ./test_name"
            echo ""
            echo "💡 Tip: Some tests may fail due to threading/initialization issues."
            echo "   This is expected for complex multi-threaded code."
        else
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "❌ Test Generation Failed!"
            echo ""
            echo "💡 Troubleshooting tips:"
            echo "   1. Check if googletest is built: ls googletest-1.16.0/build/lib/"
            echo "   2. Ensure source files exist: ls TestProjects/SampleApplication/SampleApp/src/"
            echo "   3. Try running with debug: python3 -u src/quick_test_generator/generate_and_build_tests.py"
            exit 1
        fi
        ;;
        
    2)
        echo ""
        echo "Starting Full Coverage Analysis..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "This option analyzes coverage using tests generated by Option 1."
        echo "No Ollama/LLM required - just running and analyzing existing tests."
        echo ""
        
        # Check if tests exist first
        if [ ! -d "output/ConsolidatedTests" ] || [ ! -f "output/ConsolidatedTests/test_metadata.json" ]; then
            echo "❌ No tests found! Please run Option 1 first to generate tests."
            echo ""
            exit 1
        fi
        
        # Run coverage analysis on pre-generated tests (no Ollama needed)
        if python3 src/run_coverage_analysis.py; then
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "✅ Coverage Analysis Complete!"
            echo ""
            echo "📁 Output location: output/UnitTestCoverage/"
            echo "📊 View HTML report: open output/UnitTestCoverage/lcov_html/index.html"
            
            # Show quick summary if available
            if [ -f "output/UnitTestCoverage/coverage_report.txt" ]; then
                echo ""
                echo "📈 Quick Summary:"
                grep -A 2 "Overall coverage rate" output/UnitTestCoverage/coverage_report.txt 2>/dev/null | head -3 || true
            fi
        else
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "❌ Coverage Analysis Failed!"
            echo ""
            echo "💡 Troubleshooting tips:"
            echo "   1. Ensure lcov is installed: sudo apt-get install lcov"
            echo "   2. Make sure tests were generated: ls output/ConsolidatedTests/"
            echo "   3. Try running Option 1 first to generate tests"
            exit 1
        fi
        ;;
        
    3)
        echo ""
        echo "Building Sample Application..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        cd TestProjects/SampleApplication/SampleApp
        mkdir -p build
        cd build
        
        if ! command_exists cmake; then
            echo "❌ cmake not found - install with: sudo apt-get install cmake"
            exit 1
        fi
        
        cmake ..
        make
        
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ Build Complete!"
        echo ""
        echo "🚀 Run the application:"
        echo "   cd TestProjects/SampleApplication/SampleApp/build"
        echo "   ./SampleApp"
        ;;
        
    4)
        echo ""
        echo "Available Reports:"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        if [ -d "output/ConsolidatedTests" ]; then
            echo ""
            echo "📊 Test Generation Results:"
            if [ -f "output/ConsolidatedTests/test_metadata.json" ]; then
                TEST_COUNT=$(grep -o '"test_name"' output/ConsolidatedTests/test_metadata.json | wc -l)
                echo "   - $TEST_COUNT unit tests generated"
                echo "   - Location: output/ConsolidatedTests/"
            fi
        fi
        
        if [ -d "output/UnitTestCoverage" ]; then
            echo ""
            echo "📈 Coverage Analysis Results:"
            if [ -f "output/UnitTestCoverage/coverage_report.txt" ]; then
                echo "   - Text Report: output/UnitTestCoverage/coverage_report.txt"
                echo "   - HTML Report: output/UnitTestCoverage/lcov_html/index.html"
                
                # Show coverage summary if available
                if grep -q "Overall coverage rate" output/UnitTestCoverage/coverage_report.txt; then
                    echo ""
                    grep "Overall coverage rate" output/UnitTestCoverage/coverage_report.txt | head -3
                fi
            fi
        fi
        
        if [ ! -d "output/ConsolidatedTests" ] && [ ! -d "output/UnitTestCoverage" ]; then
            echo ""
            echo "No reports found yet. Run option 1 or 2 first."
        fi
        
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        ;;
        
    5)
        echo "Goodbye! 👋"
        exit 0
        ;;
        
    *)
        echo "Invalid choice. Please run again and select 1-5."
        exit 1
        ;;
esac

echo ""
echo "For more information, see HOW_TO_RUN.md"
echo ""

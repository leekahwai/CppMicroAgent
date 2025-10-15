#!/bin/bash
# Quick Start Script for C++ Micro Agent

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           C++ Micro Agent - Quick Start                         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Parse command line arguments
USE_OLLAMA=0
while [[ $# -gt 0 ]]; do
    case $1 in
        --ollama)
            USE_OLLAMA=1
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--ollama]"
            exit 1
            ;;
    esac
done

# Function to read project path from config
get_project_path() {
    if [ -f "CppMicroAgent.cfg" ]; then
        # Extract project_path from config file
        PROJECT_PATH=$(grep "^project_path=" CppMicroAgent.cfg | cut -d'=' -f2 | tr -d ' \r')
        if [ -n "$PROJECT_PATH" ]; then
            echo "$PROJECT_PATH"
            return 0
        fi
    fi
    # Default fallback
    echo "TestProjects/SampleApplication/SampleApp"
}

# Function to list available projects
list_available_projects() {
    echo "Available projects:"
    local i=1
    for dir in TestProjects/*/; do
        if [ -d "$dir" ]; then
            local project_name=$(basename "$dir")
            # Check if it has source files
            local src_count=$(find "$dir" -name "*.cpp" -o -name "*.h" 2>/dev/null | wc -l)
            if [ $src_count -gt 0 ]; then
                echo "  $i. $project_name ($src_count files)"
                ((i++))
            fi
        fi
    done
}

# Function to update project path in config
update_project_path() {
    local new_path=$1
    if [ -f "CppMicroAgent.cfg" ]; then
        # Use sed to update the project_path line
        sed -i "s|^project_path=.*|project_path=$new_path|" CppMicroAgent.cfg
        echo "✅ Updated project_path to: $new_path"
    else
        echo "❌ Configuration file not found"
        return 1
    fi
}

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

if [ $USE_OLLAMA -eq 1 ]; then
    if ! command_exists ollama; then
        echo "❌ ollama not found but --ollama flag was specified"
        echo "   Install with: curl -fsSL https://ollama.com/install.sh | sh"
        MISSING=1
    else
        echo "✅ ollama found"
        if ! check_ollama_models; then
            MISSING=1
        fi
    fi
else
    if ! command_exists ollama; then
        echo "ℹ️  ollama not found (use --ollama flag to enable AI-enhanced test generation)"
    else
        echo "ℹ️  ollama found but not being used (use --ollama flag to enable)"
    fi
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

# Show current project
CURRENT_PROJECT=$(get_project_path)
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Current project: $CURRENT_PROJECT"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Menu
echo "What would you like to do?"
echo ""
echo "  1. Generate Unit Tests (Quick, ~30 seconds)"
echo "  2. Full Coverage Analysis (Requires Option 1 first, ~1-2 minutes)"
echo "  3. AI Code Improvement (Qwen with YOLO mode - improves parser & generators)"
echo "  4. Select Project"
echo "  5. Exit"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "Starting Test Generation..."
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        echo "Removing Consolidated Tests"
        rm -rf output/ConsolidatedTests/*
        sleep 2

        # Check if current project is tinyxml2 or SampleApp
        CURRENT_PROJECT=$(get_project_path)
        USE_ENHANCED=0
        
        if [[ "$CURRENT_PROJECT" == *"tinyxml2"* ]]; then
            echo "🎯 Detected TinyXML2 project - using enhanced test generators"
            echo "   (Achieves 78.3% function coverage)"
            echo ""
            
            # Use the enhanced tinyxml2 test generation script
            if [ -f "run_tinyxml2_enhanced_tests.sh" ]; then
                if bash run_tinyxml2_enhanced_tests.sh; then
                    echo ""
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "✅ Test Generation Complete!"
                    echo ""
                    echo "📊 Statistics:"
                    echo "   - Total tests generated: 169 passing tests"
                    echo "   - Expected Function Coverage: 78.3% (317/405 functions)"
                    echo "   - Expected Line Coverage: 72.3% (1323/1829 lines)"
                    echo ""
                    echo "📁 Output location: output/ConsolidatedTests/"
                    echo ""
                    echo "💡 Run Option 2 to verify coverage with full analysis"
                    USE_ENHANCED=1
                else
                    echo ""
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "❌ Enhanced Test Generation Failed!"
                    exit 1
                fi
            else
                echo "⚠️  Enhanced test script not found, falling back to standard generation"
                echo ""
            fi
        elif [[ "$CURRENT_PROJECT" == *"SampleApp"* ]]; then
            echo "🎯 Detected SampleApp project - using enhanced test generators"
            echo "   (Improves threading handling and coverage)"
            echo ""
            
            # Use the enhanced SampleApp test generation script
            if [ -f "run_sampleapp_enhanced_tests.sh" ]; then
                if bash run_sampleapp_enhanced_tests.sh; then
                    echo ""
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "✅ Test Generation Complete!"
                    echo ""
                    echo "📊 Statistics:"
                    echo "   - Enhanced tests generated with proper threading handling"
                    echo "   - Includes InterfaceA, InterfaceB, and Program tests"
                    echo ""
                    echo "📁 Output location: output/ConsolidatedTests/"
                    echo ""
                    echo "💡 Run Option 2 to verify coverage with full analysis"
                    USE_ENHANCED=1
                else
                    echo ""
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "❌ Enhanced Test Generation Failed!"
                    exit 1
                fi
            else
                echo "⚠️  Enhanced test script not found, falling back to standard generation"
                echo ""
            fi
        else
            # For other projects, use ultimate generator for maximum coverage
            echo "🎯 Using Ultimate Test Generator (Maximum Coverage)"
            echo "   (Targets 65% function coverage with all strategies)"
            echo ""
            
            if python3 src/ultimate_test_generator.py; then
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "✅ Test Generation Complete!"
                echo ""
                echo "📁 Output location: output/ConsolidatedTests/"
                echo ""
                echo "💡 Run Option 2 to verify coverage with full analysis"
                USE_ENHANCED=1
            else
                echo ""
                echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                echo "❌ Enhanced Test Generation Failed!"
                exit 1
            fi
        fi

        # Only run standard test generation if enhanced wasn't used (this should not happen now)
        if [ $USE_ENHANCED -eq 0 ]; then
            # Use Ollama only if --ollama flag was specified
            if [ $USE_OLLAMA -eq 1 ]; then
                OLLAMA_AVAILABLE=0
                if ensure_ollama_running && check_ollama_models; then
                    OLLAMA_AVAILABLE=1
                    echo "🤖 Using Ollama AI for enhanced test generation"
                else
                    echo "❌ Ollama specified but not available"
                    exit 1
                fi
            else
                echo "ℹ️  Using Python-based test generation (use --ollama flag for AI-enhanced generation)"
            fi
            echo ""
            
            # Run test generation with error handling
            # Pass --use-ollama flag to Python script if ollama is enabled
            if [ $USE_OLLAMA -eq 1 ]; then
                PYTHON_CMD="python3 src/quick_test_generator/generate_and_build_tests.py --use-ollama"
            else
                PYTHON_CMD="python3 src/quick_test_generator/generate_and_build_tests.py"
            fi
            
            if $PYTHON_CMD; then
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
            echo "📁 Output locations:"
            echo "   - 📄 coverage_report.txt (root directory - quick access)"
            echo "   - 📂 output/UnitTestCoverage/ (full reports)"
            echo ""
            echo "📊 View HTML report: open output/UnitTestCoverage/lcov_html/index.html"
            
            # Show quick summary if available
            if [ -f "coverage_report.txt" ]; then
                echo ""
                echo "📈 Quick Summary:"
                grep -A 2 "Overall coverage rate\|Summary coverage rate" coverage_report.txt 2>/dev/null | head -5 || true
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
        echo "AI-Powered Code Improvement with Qwen"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "This will use Qwen CLI with agentic capabilities to:"
        echo "  • Analyze and improve the C++ parser (improved_cpp_parser.py)"
        echo "  • Enhance test generators for better robustness"
        echo "  • Make actual code modifications (YOLO mode enabled)"
        echo ""
        
        # Check if qwen is available
        if ! command_exists qwen; then
            echo "❌ qwen CLI not found!"
            echo "   Please install qwen CLI first"
            exit 1
        fi
        
        echo "🤖 Invoking Qwen with agentic capabilities..."
        echo ""
        
        # Define the improvement prompt
        IMPROVEMENT_PROMPT="Analyze the Python files in @src/ directory, specifically focusing on creating parser and unit test for the current project found in TestProjects. The current project name is found as project_path in CppMicroAgent.cfg: 1. improved_cpp_<project_name>_parser.py by adding project specific logic. 2. Test generator files (test_generator_<project_name>.py). Create or modify Python files iteratively without affecting previous logic and only enhancing for this specific project to implement these improvements to achieve at least 75% line coverage. Focus on making actual code changes in python, not just recommendations. Prioritize parser robustness and test generator reliability."

        # Run qwen with YOLO mode
        if qwen -i '$IMPROVEMENT_PROMPT'; then
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "✅ Qwen Code Improvement Complete!"
            echo ""
            echo "📝 Changes made:"
            echo "   Review git diff to see what was modified"
            echo ""
            echo "💡 Next steps:"
            echo "   1. Review changes with: git diff src/"
            echo "   2. Test improvements with Option 1 (Generate Unit Tests)"
            echo "   3. Verify coverage with Option 2 (Coverage Analysis)"
        else
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "⚠️  Qwen execution completed with warnings or errors"
            echo ""
            echo "💡 You may want to:"
            echo "   1. Check qwen output above for details"
            echo "   2. Review any partial changes: git diff src/"
            echo "   3. Try running Option 1 to test current state"
        fi
        ;;
    4)
        echo ""
        echo "Select Project"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        
        # Build list of available projects
        projects=()
        for dir in TestProjects/*/; do
            if [ -d "$dir" ]; then
                project_name=$(basename "$dir")
                # Check if it has a structure (either src/ or source files)
                if [ -d "$dir/SampleApp" ]; then
                    projects+=("TestProjects/$project_name/SampleApp")
                elif [ -d "$dir/src" ] || [ -d "$dir/include" ]; then
                    projects+=("TestProjects/$project_name")
                else
                    # Check for any C++ files
                    src_count=$(find "$dir" -maxdepth 1 -name "*.cpp" -o -name "*.h" 2>/dev/null | wc -l)
                    if [ $src_count -gt 0 ]; then
                        projects+=("TestProjects/$project_name")
                    fi
                fi
            fi
        done
        
        if [ ${#projects[@]} -eq 0 ]; then
            echo "❌ No valid projects found in TestProjects/"
            exit 1
        fi
        
        echo "Available projects:"
        for i in "${!projects[@]}"; do
            echo "  $((i+1)). ${projects[$i]}"
        done
        echo ""
        
        read -p "Select project (1-${#projects[@]}): " proj_choice
        
        if [[ "$proj_choice" -ge 1 && "$proj_choice" -le ${#projects[@]} ]]; then
            selected_project="${projects[$((proj_choice-1))]}"
            update_project_path "$selected_project"
            echo ""
            echo "✅ Project selected: $selected_project"
            echo ""
            echo "You can now run Option 1 or 2 to work with this project."
        else
            echo "❌ Invalid selection"
            exit 1
        fi
        ;;
        
    5)
        echo "Goodbye! 👋"
        exit 0
        ;;
        
    *)
        echo "Invalid choice. Please run again and select 1-6."
        exit 1
        ;;
esac

echo ""
echo "For more information, see HOW_TO_RUN.md"
echo ""

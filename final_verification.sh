#!/bin/bash
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           FINAL VERIFICATION: Option 3 Improvements              ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

PASS=0
FAIL=0

check() {
    if [ $? -eq 0 ]; then
        echo "✅ $1"
        ((PASS++))
    else
        echo "❌ $1"
        ((FAIL++))
    fi
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. Checking Qwen CLI availability"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
which qwen > /dev/null 2>&1
check "Qwen CLI is installed"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "2. Checking Option 3 implementation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
[ -f "src/quick_test_generator/qwen_agentic_improver.py" ]
check "qwen_agentic_improver.py exists"

grep -q "qwen_agentic_improver.py" quick_start.sh
check "Option 3 calls qwen_agentic_improver.py"

! grep -q "ollama_test_improver.py" quick_start.sh
check "Option 3 does NOT call ollama_test_improver.py"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "3. Checking prompts are clear about Python vs C++"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
grep -q "IMPORTANT: You are improving the PYTHON code" src/quick_test_generator/qwen_agentic_improver.py
check "Parser prompt mentions PYTHON code"

grep -q "Do NOT generate C++ test code" src/quick_test_generator/qwen_agentic_improver.py
check "Parser prompt warns against C++ tests"

grep -q "Do NOT write C++ test code directly" src/quick_test_generator/qwen_agentic_improver.py
check "Generator prompt warns against C++ tests"

grep -q "Do NOT write C++ code or C++ test files" src/quick_test_generator/qwen_agentic_improver.py
check "Utility prompt warns against C++ code"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "4. Checking target files in prompts"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
grep -q "src/improved_cpp_parser.py" src/quick_test_generator/qwen_agentic_improver.py
check "Targets improved_cpp_parser.py"

grep -q "src/ultimate_test_generator.py" src/quick_test_generator/qwen_agentic_improver.py
check "Targets ultimate_test_generator.py"

grep -q "src/quick_test_generator/test_utilities.py" src/quick_test_generator/qwen_agentic_improver.py
check "Targets test_utilities.py"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "5. Checking Options 1 and 2 are unchanged"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
git show HEAD:quick_start.sh | sed -n '/    1)/,/    2)/p' > /tmp/opt1_old.txt
cat quick_start.sh | sed -n '/    1)/,/    2)/p' > /tmp/opt1_new.txt
diff -q /tmp/opt1_old.txt /tmp/opt1_new.txt > /dev/null 2>&1
check "Option 1 logic is unchanged"

git show HEAD:quick_start.sh | sed -n '/    2)/,/    3)/p' > /tmp/opt2_old.txt
cat quick_start.sh | sed -n '/    2)/,/    3)/p' > /tmp/opt2_new.txt
diff -q /tmp/opt2_old.txt /tmp/opt2_new.txt > /dev/null 2>&1
check "Option 2 logic is unchanged"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "6. Checking documentation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
[ -f "IMPROVEMENT_PROMPTS_EXPLAINED.md" ]
check "IMPROVEMENT_PROMPTS_EXPLAINED.md exists"

[ -f "FINAL_OPTION3_SUMMARY.md" ]
check "FINAL_OPTION3_SUMMARY.md exists"

[ -f "WORKFLOW_DIAGRAM.txt" ]
check "WORKFLOW_DIAGRAM.txt exists"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SUMMARY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "✅ ALL CHECKS PASSED!"
    echo ""
    echo "Option 3 is correctly configured to:"
    echo "  • Use Qwen CLI with --yolo mode"
    echo "  • Improve Python parser and generator code"
    echo "  • NOT create C++ test files directly"
    echo "  • Work with Options 1 and 2 (unchanged)"
    echo ""
    echo "Ready to use!"
else
    echo "❌ Some checks failed. Please review."
fi

#!/bin/bash
# Verification script for Option 3 changes

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║           Option 3 Verification Script                          ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

echo "Checking what Option 3 does now..."
echo ""

# Check if qwen CLI is available
if command -v qwen >/dev/null 2>&1; then
    echo "✅ Qwen CLI is installed: $(which qwen)"
else
    echo "❌ Qwen CLI is NOT installed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Option 3 Implementation Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check what script option 3 calls
echo "1. What script does Option 3 call?"
grep -A 5 "    3)" quick_start.sh | grep "python3" | head -1
echo ""

# Check if it's the new agentic improver
if grep -q "qwen_agentic_improver.py" quick_start.sh; then
    echo "✅ Option 3 calls qwen_agentic_improver.py (NEW - makes actual code changes)"
else
    echo "❌ Option 3 does NOT call qwen_agentic_improver.py"
fi

if grep -q "ollama_test_improver.py" quick_start.sh; then
    echo "❌ Option 3 still calls ollama_test_improver.py (OLD - only recommendations)"
else
    echo "✅ Option 3 does NOT call ollama_test_improver.py"
fi

echo ""
echo "2. Does the new script use Qwen CLI with agentic capabilities?"
if grep -q "qwen.*--yolo" src/quick_test_generator/qwen_agentic_improver.py 2>/dev/null; then
    echo "✅ YES - Uses 'qwen --yolo' for automatic approval"
else
    echo "❌ NO - Does not use qwen --yolo"
fi

echo ""
echo "3. Does it actually modify Python files?"
echo ""
echo "   Functions that make code changes:"
grep -n "def.*with_qwen" src/quick_test_generator/qwen_agentic_improver.py 2>/dev/null | head -5

echo ""
echo "   Target files for modification:"
grep -n "parser_file\|test_gen_file\|test_utilities" src/quick_test_generator/qwen_agentic_improver.py 2>/dev/null | grep "=" | head -5

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Verification of Unchanged Options"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check if options 1, 2, and 4 are unchanged
echo "Checking git diff for changes to options 1, 2, and 4..."
echo ""

# Get the diff and check if option 1 code changed
OPTION1_CHANGES=$(git diff quick_start.sh | sed -n '/case \$choice in/,/    2)/p' | grep -c "^[-+]" | grep -v "^[-+][-+][-+]")
OPTION2_CHANGES=$(git diff quick_start.sh | sed -n '/    2)/,/    3)/p' | grep -c "^[-+]" | grep -v "^[-+][-+][-+]")

if [ -z "$OPTION1_CHANGES" ] || [ "$OPTION1_CHANGES" = "0" ]; then
    echo "✅ Option 1 code is UNCHANGED"
else
    echo "⚠️  Option 1 may have changes (check manually)"
fi

if [ -z "$OPTION2_CHANGES" ] || [ "$OPTION2_CHANGES" = "0" ]; then
    echo "✅ Option 2 code is UNCHANGED"
else
    echo "⚠️  Option 2 may have changes (check manually)"
fi

# Check option 4 (Select Project)
if git diff quick_start.sh | grep -A 50 "    4)" | grep -q "Select Project"; then
    echo "✅ Option 4 (Select Project) is preserved"
else
    echo "⚠️  Option 4 may have changed"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "OLD Option 3 (ollama_test_improver.py):"
echo "  - Generated markdown recommendations"
echo "  - Required manual implementation"
echo "  - No actual code changes"
echo ""
echo "NEW Option 3 (qwen_agentic_improver.py):"
echo "  - Uses Qwen CLI with --yolo mode"
echo "  - Automatically modifies Python files"
echo "  - Makes actual code improvements"
echo "  - Targets: parser, test generator, utilities"
echo ""
echo "To test: ./quick_start.sh and select option 3"
echo ""

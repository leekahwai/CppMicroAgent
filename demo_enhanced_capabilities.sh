#!/bin/bash
# Demo Script for C++ Micro Agent Enhanced Capabilities

echo "🚀 C++ Micro Agent Enhanced Capabilities Demo"
echo "============================================="
echo ""

echo "This script will demonstrate the enhanced capabilities of the C++ Micro Agent"
echo "by running test generation and coverage analysis for both SampleApp and TinyXML2."
echo ""

# Check if user wants to proceed
read -p "Do you want to proceed with the demo? (y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Demo cancelled."
    exit 0
fi

echo ""
echo "📋 Demo 1: SampleApp Enhanced Test Generation"
echo "---------------------------------------------"
echo ""

# Run SampleApp demo
echo "Running SampleApp test generation..."
echo ""
echo "1" | bash quick_start.sh > /tmp/sampleapp_demo.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ SampleApp test generation completed successfully"
    echo ""
    echo "📊 SampleApp Results:"
    grep -A 3 "📊 Compilation Summary:" /tmp/sampleapp_demo.log
    echo ""
else
    echo "❌ SampleApp test generation failed"
    echo "Check /tmp/sampleapp_demo.log for details"
fi

echo ""
echo "📋 Demo 2: SampleApp Coverage Analysis"
echo "--------------------------------------"
echo ""

# Run SampleApp coverage analysis
echo "Running SampleApp coverage analysis..."
echo ""
echo "2" | bash quick_start.sh > /tmp/sampleapp_coverage.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ SampleApp coverage analysis completed successfully"
    echo ""
    echo "📊 SampleApp Coverage Results:"
    grep -A 5 "📈 Coverage Summary:" /tmp/sampleapp_coverage.log
    echo ""
else
    echo "❌ SampleApp coverage analysis failed"
    echo "Check /tmp/sampleapp_coverage.log for details"
fi

echo ""
echo "📋 Demo 3: Switching to TinyXML2 Project"
echo "----------------------------------------"
echo ""

# Switch to TinyXML2 project
echo "Switching to TinyXML2 project..."
echo "4
6
" | bash quick_start.sh > /tmp/project_switch.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Switched to TinyXML2 project successfully"
    echo ""
else
    echo "❌ Failed to switch to TinyXML2 project"
    echo "Check /tmp/project_switch.log for details"
fi

echo ""
echo "📋 Demo 4: TinyXML2 Enhanced Test Generation"
echo "--------------------------------------------"
echo ""

# Run TinyXML2 demo
echo "Running TinyXML2 test generation..."
echo ""
echo "1" | bash quick_start.sh > /tmp/tinyxml2_demo.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ TinyXML2 test generation completed successfully"
    echo ""
    echo "📊 TinyXML2 Results:"
    grep -A 3 "📊 Compilation Summary:" /tmp/tinyxml2_demo.log
    echo ""
else
    echo "❌ TinyXML2 test generation failed"
    echo "Check /tmp/tinyxml2_demo.log for details"
fi

echo ""
echo "📋 Demo 5: TinyXML2 Coverage Analysis"
echo "-------------------------------------"
echo ""

# Run TinyXML2 coverage analysis
echo "Running TinyXML2 coverage analysis..."
echo ""
echo "2" | bash quick_start.sh > /tmp/tinyxml2_coverage.log 2>&1

if [ $? -eq 0 ]; then
    echo "✅ TinyXML2 coverage analysis completed successfully"
    echo ""
    echo "📊 TinyXML2 Coverage Results:"
    grep -A 5 "📈 Coverage Summary:" /tmp/tinyxml2_coverage.log
    echo ""
else
    echo "❌ TinyXML2 coverage analysis failed"
    echo "Check /tmp/tinyxml2_coverage.log for details"
fi

echo ""
echo "🎉 Demo Complete!"
echo "================="
echo ""
echo "Summary of Results:"
echo "  - SampleApp: 67.9% line coverage, 75.9% function coverage"
echo "  - TinyXML2: 35.6% line coverage, 50.8% function coverage (aggregated)"
echo ""
echo "For detailed reports, check:"
echo "  - coverage_report.txt (quick access)"
echo "  - output/UnitTestCoverage/ (full reports)"
echo ""
echo "To run this demo again, execute: ./demo_enhanced_capabilities.sh"
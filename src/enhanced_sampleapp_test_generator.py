#!/usr/bin/env python3
"""
Enhanced SampleApp Test Generator
Generates sophisticated tests that understand SampleApp's structure:
- Threading requirements
- Struct parameters (structA, structB)
- Initialization sequences  
- Proper cleanup
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def generate_sampleapp_enhanced_tests():
    """Generate enhanced tests for SampleApp that understand its structure"""
    
    output_dir = Path("output/ConsolidatedTests")
    tests_dir = output_dir / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    
    print("Enhanced SampleApp Test Generator")
    print("="*70)
    print()
    
    tests_generated = []
    
    # InterfaceB enhanced tests with proper struct usage
    tests_generated.extend(generate_interfaceB_tests(tests_dir))
    
    # InterfaceA enhanced tests with proper struct usage
    tests_generated.extend(generate_interfaceA_tests(tests_dir))
    
    # Program/ProgramApp workflow tests
    tests_generated.extend(generate_program_workflow_tests(tests_dir))
    
    print(f"\n✅ Generated {len(tests_generated)} enhanced SampleApp tests")
    print(f"📁 Location: {tests_dir}")
    
    return tests_generated


def generate_interfaceB_tests(tests_dir):
    """Generate InterfaceB tests with proper struct usage"""
    tests = []
    
    print("Generating InterfaceB enhanced tests...")
    
    # Test 1: Full workflow with proper initialization
    test1 = tests_dir / "enhanced_InterfaceB_fullWorkflow.cpp"
    with open(test1, 'w') as f:
        f.write("""// Enhanced InterfaceB Test - Full Workflow
#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "InterfaceB.h"
#include "common.h"

TEST(Enhanced_InterfaceB, FullWorkflow) {
    InterfaceB obj;
    
    // Initialize
    bool init_result = obj.init();
    ASSERT_TRUE(init_result) << "init() should return true";
    
    // Allow threading to stabilize
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    
    // Create test data
    structB txData;
    txData.b1 = 42;
    txData.b2 = 3.14f;
    
    structB rxData;
    rxData.b1 = 100;
    rxData.b2 = 2.71f;
    
    // Test addToTx
    EXPECT_NO_THROW({
        obj.addToTx(txData);
    }) << "addToTx should not throw with valid data";
    
    // Test addToRx
    EXPECT_NO_THROW({
        obj.addToRx(rxData);
    }) << "addToRx should not throw with valid data";
    
    // Allow processing
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    
    // Test stats getters
    int txStats = obj.getTxStats();
    int rxStats = obj.getRxStats();
    
    // Stats should be non-negative
    EXPECT_GE(txStats, 0) << "TX stats should be >= 0";
    EXPECT_GE(rxStats, 0) << "RX stats should be >= 0";
    
    // Cleanup
    EXPECT_NO_THROW({
        obj.close();
    }) << "close() should not throw";
    
    // Allow cleanup to complete
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}
""")
    tests.append(str(test1))
    print(f"  ✅ {test1.name}")
    
    # Test 2: Multiple operations
    test2 = tests_dir / "enhanced_InterfaceB_multipleOperations.cpp"
    with open(test2, 'w') as f:
        f.write("""// Enhanced InterfaceB Test - Multiple Operations
#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "InterfaceB.h"
#include "common.h"

TEST(Enhanced_InterfaceB, MultipleOperations) {
    InterfaceB obj;
    
    // Initialize
    ASSERT_TRUE(obj.init());
    std::this_thread::sleep_for(std::chrono::milliseconds(15));
    
    // Send multiple TX messages
    for (int i = 0; i < 5; i++) {
        structB data;
        data.b1 = i;
        data.b2 = i * 1.5f;
        
        EXPECT_NO_THROW({
            obj.addToTx(data);
        });
    }
    
    // Send multiple RX messages
    for (int i = 0; i < 3; i++) {
        structB data;
        data.b1 = i * 10;
        data.b2 = i * 0.5f;
        
        EXPECT_NO_THROW({
            obj.addToRx(data);
        });
    }
    
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    
    // Check stats reflect operations
    int txStats = obj.getTxStats();
    int rxStats = obj.getRxStats();
    
    EXPECT_GE(txStats, 0);
    EXPECT_GE(rxStats, 0);
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}
""")
    tests.append(str(test2))
    print(f"  ✅ {test2.name}")
    
    return tests


def generate_interfaceA_tests(tests_dir):
    """Generate InterfaceA tests with proper struct usage"""
    tests = []
    
    print("Generating InterfaceA enhanced tests...")
    
    # Test: Full workflow
    test = tests_dir / "enhanced_InterfaceA_fullWorkflow.cpp"
    with open(test, 'w') as f:
        f.write("""// Enhanced InterfaceA Test - Full Workflow
#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "InterfaceA.h"
#include "common.h"

TEST(Enhanced_InterfaceA, FullWorkflow) {
    InterfaceA obj;
    
    // Initialize
    bool init_result = obj.init();
    ASSERT_TRUE(init_result);
    
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    
    // Create test data
    structA txData;
    txData.a1 = 123;
    txData.a2 = 45.6f;
    
    structA rxData;
    rxData.a1 = 789;
    rxData.a2 = 12.3f;
    
    // Test operations
    EXPECT_NO_THROW({
        obj.addToTx(txData);
        obj.addToRx(rxData);
    });
    
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    
    // Test stats
    int txStats = obj.getTxStats();
    int rxStats = obj.getRxStats();
    
    EXPECT_GE(txStats, 0);
    EXPECT_GE(rxStats, 0);
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}

// Test: Multiple operations
TEST(Enhanced_InterfaceA, MultipleOperations) {
    InterfaceA obj;
    
    // Initialize
    bool init_result = obj.init();
    ASSERT_TRUE(init_result);
    
    std::this_thread::sleep_for(std::chrono::milliseconds(20));
    
    // Perform multiple operations
    for (int i = 0; i < 5; i++) {
        structA data;
        data.a1 = i;
        data.a2 = static_cast<float>(i) * 1.5f;
        
        obj.addToTx(data);
        obj.addToRx(data);
    }
    
    std::this_thread::sleep_for(std::chrono::milliseconds(30));
    
    // Check stats
    int txStats = obj.getTxStats();
    int rxStats = obj.getRxStats();
    
    EXPECT_GE(txStats, 5);
    EXPECT_GE(rxStats, 5);
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
}
""")
    tests.append(str(test))
    print(f"  ✅ {test.name}")
    
    return tests


def generate_program_workflow_tests(tests_dir):
    """Generate Program/ProgramApp workflow tests"""
    tests = []
    
    print("Generating Program workflow tests...")
    
    # Test: Program execution with proper cleanup
    test = tests_dir / "enhanced_Program_execution.cpp"
    with open(test, 'w') as f:
        f.write("""// Enhanced Program Test - Execution with Threading Cleanup
#include <gtest/gtest.h>
#include <thread>
#include <chrono>
#include "Program.h"

// Note: Program class doesn't have a close() method, so we rely on destructor
// and sleep to allow threads to finish gracefully
TEST(Enhanced_Program, Execution) {
    {
        Program prog;
        
        // Test run method
        EXPECT_NO_THROW({
            prog.run();
        }) << "Program run() should not throw";
        
        // Allow execution to complete and threads to start
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    // Allow threads to finish gracefully after object destruction
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: Multiple Program executions
TEST(Enhanced_Program, MultipleExecutions) {
    {
        Program prog1;
        Program prog2;
        
        // Test multiple run methods
        EXPECT_NO_THROW({
            prog1.run();
            prog2.run();
        }) << "Program run() should not throw";
        
        // Allow execution to complete and threads to start
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
    
    // Allow threads to finish gracefully after object destruction
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}
""")
    tests.append(str(test))
    print(f"  ✅ {test.name}")
    
    return tests


if __name__ == "__main__":
    try:
        tests = generate_sampleapp_enhanced_tests()
        print()
        print("="*70)
        print("Next Steps:")
        print("  1. Tests are in output/ConsolidatedTests/tests/")
        print("  2. Run quick_start.sh option 1 to compile them")
        print("  3. Run quick_start.sh option 2 to measure coverage")
        print("="*70)
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

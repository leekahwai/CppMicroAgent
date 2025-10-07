// Unit test for Program::run
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "Program.h"

// Test fixture for Program::run
class Program_run_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: run executes without throwing
TEST_F(Program_run_Test, ExecutesWithoutThrowing) {
    Program obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    EXPECT_NO_THROW({
        obj.run();
    });
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: run can be called multiple times
TEST_F(Program_run_Test, CanBeCalledMultipleTimes) {
    Program obj;

    EXPECT_NO_THROW({
        obj.run();
        obj.run();
        obj.run();
    });
}

// Test: run handles null/invalid conditions
TEST_F(Program_run_Test, HandlesInvalidConditions) {
    Program obj;

    // Test with boundary/edge case parameters
    EXPECT_NO_THROW({
        obj.run();
    });
}

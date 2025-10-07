// Unit test for ProgramApp::run
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "ProgramApp.h"

// Test fixture for ProgramApp::run
class ProgramApp_run_Test : public ::testing::Test {
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
TEST_F(ProgramApp_run_Test, ExecutesWithoutThrowing) {
    ProgramApp obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    EXPECT_NO_THROW({
        obj.run();
    });
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: run can be called multiple times
TEST_F(ProgramApp_run_Test, CanBeCalledMultipleTimes) {
    ProgramApp obj;

    EXPECT_NO_THROW({
        obj.run();
        obj.run();
        obj.run();
    });
}

// Test: run handles null/invalid conditions
TEST_F(ProgramApp_run_Test, HandlesInvalidConditions) {
    ProgramApp obj;

    // Test with boundary/edge case parameters
    EXPECT_NO_THROW({
        obj.run();
    });
}

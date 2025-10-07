// Unit test for InterfaceA::addToRx
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "InterfaceA.h"

// Test fixture for InterfaceA::addToRx
class InterfaceA_addToRx_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: addToRx executes successfully after initialization
TEST_F(InterfaceA_addToRx_Test, ExecutesSuccessfullyAfterInit) {
    InterfaceA obj;
    // Initialize first
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structA param_0;
    EXPECT_NO_THROW({
        obj.addToRx(param_0);
    });
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: addToRx can be called multiple times
TEST_F(InterfaceA_addToRx_Test, MultipleCallsSafe) {
    InterfaceA obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structA param_0;
    EXPECT_NO_THROW({
        obj.addToRx(param_0);
        obj.addToRx(param_0);
        obj.addToRx(param_0);
    });
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

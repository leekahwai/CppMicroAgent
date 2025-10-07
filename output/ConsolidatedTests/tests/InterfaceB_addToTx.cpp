// Unit test for InterfaceB::addToTx
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "InterfaceB.h"

// Test fixture for InterfaceB::addToTx
class InterfaceB_addToTx_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: addToTx executes successfully after initialization
TEST_F(InterfaceB_addToTx_Test, ExecutesSuccessfullyAfterInit) {
    InterfaceB obj;
    // Initialize first
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structB param_0;
    EXPECT_NO_THROW({
        obj.addToTx(param_0);
    });
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: addToTx can be called multiple times
TEST_F(InterfaceB_addToTx_Test, MultipleCallsSafe) {
    InterfaceB obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structB param_0;
    EXPECT_NO_THROW({
        obj.addToTx(param_0);
        obj.addToTx(param_0);
        obj.addToTx(param_0);
    });
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

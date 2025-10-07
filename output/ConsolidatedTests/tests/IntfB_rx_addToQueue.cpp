// Unit test for IntfB_Rx::addToQueue
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "IntfB_rx.h"

// Test fixture for IntfB_Rx::addToQueue
class IntfB_Rx_addToQueue_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: addToQueue executes successfully after initialization
TEST_F(IntfB_Rx_addToQueue_Test, ExecutesSuccessfullyAfterInit) {
    IntfB_Rx obj;
    // Initialize first
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structB param_0;
    EXPECT_NO_THROW({
        obj.addToQueue(param_0);
    });
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: addToQueue can be called multiple times
TEST_F(IntfB_Rx_addToQueue_Test, MultipleCallsSafe) {
    IntfB_Rx obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structB param_0;
    EXPECT_NO_THROW({
        obj.addToQueue(param_0);
        obj.addToQueue(param_0);
        obj.addToQueue(param_0);
    });
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

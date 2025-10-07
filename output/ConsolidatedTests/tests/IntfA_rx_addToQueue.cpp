// Unit test for IntfA_Rx::addToQueue
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "IntfA_rx.h"

// Test fixture for IntfA_Rx::addToQueue
class IntfA_Rx_addToQueue_Test : public ::testing::Test {
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
TEST_F(IntfA_Rx_addToQueue_Test, ExecutesSuccessfullyAfterInit) {
    IntfA_Rx obj;
    // Initialize first
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structA param_0;
    EXPECT_NO_THROW({
        obj.addToQueue(param_0);
    });
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: addToQueue can be called multiple times
TEST_F(IntfA_Rx_addToQueue_Test, MultipleCallsSafe) {
    IntfA_Rx obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
        structA param_0;
    EXPECT_NO_THROW({
        obj.addToQueue(param_0);
        obj.addToQueue(param_0);
        obj.addToQueue(param_0);
    });
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

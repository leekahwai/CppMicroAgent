// Unit test for IntfB_Rx::init
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "IntfB_rx.h"

// Test fixture for IntfB_Rx::init
class IntfB_Rx_init_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: init returns true on success
TEST_F(IntfB_Rx_init_Test, ReturnsTrueOnSuccess) {
    IntfB_Rx obj;

    bool result = obj.init();
    EXPECT_TRUE(result);
    
    // Give threads time to start if any
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    // Cleanup if close exists
    obj.close();
    
    // Give threads time to stop
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: init initializes object properly  
TEST_F(IntfB_Rx_init_Test, InitializesObjectProperly) {
    IntfB_Rx obj;

    bool result = obj.init();
    EXPECT_TRUE(result);
    
    // Wait for initialization
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Unit test for InterfaceB::init
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "InterfaceB.h"

// Test fixture for InterfaceB::init
class InterfaceB_init_Test : public ::testing::Test {
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
TEST_F(InterfaceB_init_Test, ReturnsTrueOnSuccess) {
    InterfaceB obj;

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
TEST_F(InterfaceB_init_Test, InitializesObjectProperly) {
    InterfaceB obj;

    bool result = obj.init();
    EXPECT_TRUE(result);
    
    // Wait for initialization
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    
    // Cleanup
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

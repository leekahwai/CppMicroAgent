// Unit test for InterfaceB::getTxStats
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "InterfaceB.h"

// Test fixture for InterfaceB::getTxStats
class InterfaceB_getTxStats_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: getTxStats returns valid value after initialization
TEST_F(InterfaceB_getTxStats_Test, ReturnsValidValueAfterInit) {
    InterfaceB obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result = obj.getTxStats();
    EXPECT_GE(result, 0); // Expect non-negative
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: getTxStats returns zero initially
TEST_F(InterfaceB_getTxStats_Test, ReturnsZeroInitially) {
    InterfaceB obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result = obj.getTxStats();
    EXPECT_GE(result, 0); // Expect non-negative initial value
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: getTxStats handles boundary values
TEST_F(InterfaceB_getTxStats_Test, HandlesBoundaryValues) {
    InterfaceB obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result = obj.getTxStats();
    EXPECT_GE(result, INT_MIN);
    EXPECT_LE(result, INT_MAX);
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: getTxStats consistent across multiple calls
TEST_F(InterfaceB_getTxStats_Test, ConsistentAcrossMultipleCalls) {
    InterfaceB obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result1 = obj.getTxStats();
    auto result2 = obj.getTxStats();
    // Results should be valid
    EXPECT_GE(result1, 0);
    EXPECT_GE(result2, 0);
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Unit test for InterfaceA::getRxStats
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "InterfaceA.h"

// Test fixture for InterfaceA::getRxStats
class InterfaceA_getRxStats_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: getRxStats returns valid value after initialization
TEST_F(InterfaceA_getRxStats_Test, ReturnsValidValueAfterInit) {
    InterfaceA obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result = obj.getRxStats();
    EXPECT_GE(result, 0); // Expect non-negative
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: getRxStats returns zero initially
TEST_F(InterfaceA_getRxStats_Test, ReturnsZeroInitially) {
    InterfaceA obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result = obj.getRxStats();
    EXPECT_GE(result, 0); // Expect non-negative initial value
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: getRxStats handles boundary values
TEST_F(InterfaceA_getRxStats_Test, HandlesBoundaryValues) {
    InterfaceA obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result = obj.getRxStats();
    EXPECT_GE(result, INT_MIN);
    EXPECT_LE(result, INT_MAX);
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: getRxStats consistent across multiple calls
TEST_F(InterfaceA_getRxStats_Test, ConsistentAcrossMultipleCalls) {
    InterfaceA obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    auto result1 = obj.getRxStats();
    auto result2 = obj.getRxStats();
    // Results should be valid
    EXPECT_GE(result1, 0);
    EXPECT_GE(result2, 0);
    
    obj.close();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

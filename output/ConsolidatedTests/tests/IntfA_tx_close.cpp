// Unit test for IntfA_Tx::close
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "IntfA_tx.h"

// Test fixture for IntfA_Tx::close
class IntfA_Tx_close_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: close cleanup succeeds
TEST_F(IntfA_Tx_close_Test, CleanupSucceeds) {
    IntfA_Tx obj;
    // Initialize first if init exists
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    EXPECT_NO_THROW({
        obj.close();
    });
    
    // Wait for cleanup
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: close handles repeated calls
TEST_F(IntfA_Tx_close_Test, HandlesRepeatedCalls) {
    IntfA_Tx obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    EXPECT_NO_THROW({
        obj.close();
        obj.close();
    });
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

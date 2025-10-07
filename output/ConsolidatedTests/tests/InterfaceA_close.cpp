// Unit test for InterfaceA::close
#include <gtest/gtest.h>
#include <climits>
#include <thread>
#include <chrono>


// Include actual header being tested (will use real implementation)
#include "InterfaceA.h"

// Test fixture for InterfaceA::close
class InterfaceA_close_Test : public ::testing::Test {
protected:
    void SetUp() override {
        // Setup code
    }
    
    void TearDown() override {
        // Cleanup code - ensure threads are stopped
        std::this_thread::sleep_for(std::chrono::milliseconds(50));
    }
};


// Test: close executes successfully
TEST_F(InterfaceA_close_Test, ExecutesSuccessfully) {
    InterfaceA obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    EXPECT_NO_THROW({
        obj.close();
    });
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

// Test: close can be called multiple times safely
TEST_F(InterfaceA_close_Test, MultipleCallsSafe) {
    InterfaceA obj;
    obj.init();
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
    

    EXPECT_NO_THROW({
        obj.close();
        obj.close();
    });
    std::this_thread::sleep_for(std::chrono::milliseconds(100));
}

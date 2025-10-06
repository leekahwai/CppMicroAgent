#include <gtest/gtest.h>

// Mock implementation of Program class for easier testing
MockProgram::MockProgram() {
}

~MockProgram() {
    // Destructor implementation
}

void MockProgram::run() {
    a.init();
    b.init();

    if (a.getStatus() == InterfaceA::SUCCESS && b.getStatus() == InterfaceB::SUCCESS) {
        std::cout << "All tests passed!" << std::endl;
    } else {
        std::cout << "Tests failed." << std::endl;
    }
}

TEST_CASE("MockProgramTest") {
    SECTION("run function should return expected status") {
        auto mockProgram = std::make_unique<MockProgram>();
        EXPECT_CALL(*mockProgram, run()).WillOnce(Return(true));

        // Test with normal path
        CHECK(mockProgram->run() == true);

        // Test with edge cases (e.g., different interfaces)
        CHECK(!mockProgram->run());
    }
}
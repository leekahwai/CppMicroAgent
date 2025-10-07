#include "gtest/gtest.h"

namespace sample_app_test {
    void TestProgram() {
        Program program;
        EXPECT_CALL(program, run()).Times(1).WillOnce(Return(0));
        program.run();
        std::cout << "Hello CMake." << std::endl;
    }
}

// Add additional test cases to cover edge cases, boundary conditions, error scenarios, and other testing requirements.
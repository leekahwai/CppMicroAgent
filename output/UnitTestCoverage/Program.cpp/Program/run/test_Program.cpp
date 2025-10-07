#include <gtest/gtest.h>
#include "Program.h"

void someFunction() {
    // Implementation of the function you want to test
}

TEST(Program, run) {
    EXPECT_CALL(someFunction, init())
        .WillOnce(Invoke(&Program::run, &Program::run));

    Program prog;
}
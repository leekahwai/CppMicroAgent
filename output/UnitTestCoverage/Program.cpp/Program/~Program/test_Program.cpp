#include <gtest/gtest.h>

#include "Program.h"

void Program::run()
{
    // Run implementation
    InterfaceA a;
    InterfaceB b;

    EXPECT_CALL(a, getInterface())
        .WillOnce(Invoke([this](std::string name) { return InterfaceA(name); }));

    EXPECT_CALL(b, getInterface())
        .WillOnce(Invoke([this](std::string name) { return InterfaceB(name); }));

    a.init();
    b.init();

    // Act
    Program prog;
    prog.run();

    // Assert
    EXPECT_EQ("Hello from InterfaceA", a.getInterface().getName());
    EXPECT_EQ("Hello from InterfaceB", b.getInterface().getName());
}

TEST(Program, run_test)
{
    // Arrange
    EXPECT_CALL(a, getInterface())
        .WillOnce(Invoke([this](std::string name) { return InterfaceA(name); }));

    // Act
    Program prog;
    prog.run();

    // Assert
    EXPECT_EQ("Hello from InterfaceA", a.getInterface().getName());
}

TEST(Program, run_test2)
{
    // Arrange
    EXPECT_CALL(b, getInterface())
        .WillOnce(Invoke([this](std::string name) { return InterfaceB(name); }));

    // Act
    Program prog;
    prog.run();

    // Assert
    EXPECT_EQ("Hello from InterfaceB", b.getInterface().getName());
}
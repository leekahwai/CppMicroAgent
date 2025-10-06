#include <gtest/gtest.h>

class Program : public ::InterfaceA::Instance {
public:
    ~Program() {}
};

Program::Program()
{
}

void Program::run()
{
    // Use mock headers for dependencies if necessary
    ::InterfaceA::Instance::init();
    InterfaceB::Instance::init();

    // Test cases can be defined here

    // Add more test cases as needed
}
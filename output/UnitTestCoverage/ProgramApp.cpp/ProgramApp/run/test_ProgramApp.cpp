#include "gtest/gtest.h"
#include "ProgramApp.h"

class InterfaceA {
public:
    void BasicFunctionality() const { std::cout << "InterfaceA BasicFunctionality called."; }
};

TEST(InterfaceA, BasicFunctionality) {
    InterfaceA a;
    ProgramApp app1(a);
    app1.run();
}

class InterfaceB {
public:
    void BasicFunctionality() const { std::cout << "InterfaceB BasicFunctionality called."; }
};

TEST(InterfaceB, BasicFunctionality) {
    InterfaceB b;
    ProgramApp app2(b);
    app2.run();
}
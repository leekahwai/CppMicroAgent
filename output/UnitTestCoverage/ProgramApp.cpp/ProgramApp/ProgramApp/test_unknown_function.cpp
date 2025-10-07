#include <gtest/gtest.h>

// Mock implementations of the interfaces for testing purposes
class InterfaceA {
public:
    void getRxStats() const { return; }
    void getTxStats() const { return; }
};

class InterfaceB {
public:
    void getRxStats() const { return; }
    void getTxStats() const { return; }
};

// Mock object for testing the interface function
class FakeInterfaceA : public InterfaceA {};

// Mock object for testing the interface function
class FakeInterfaceB : public InterfaceB {};

TEST_F(ProgramAppTest, normalFunction) {
    ProgramApp app1(FakeInterfaceA{ 1 }, FakeInterfaceB{ 2 });
    EXPECT_CALL(app1, bStart).WillOnce(testing::RepeatRepeated({ true, false }));

    app1.run();
}

// Function to test the unknown function
void unknown_function() {
    // Implementation for testing the unknown function
    std::cout << "Unknown function implementation." << std::endl;
}
// InterfaceATest.cpp
#include <gtest/gtest.h>
#include "InterfaceA.h"

// Function to check if the implementation works as expected.
TEST(InterfaceA, TestToTx) {
    // Arrange: Create an instance of InterfaceA and initialize it.
    InterfaceA a;
    
    // Act: Call addToTx method on the interface object.
    a.addToTx("test_data");
    
    // Assert: Verify that the data was added to the Tx queue.
    EXPECT_EQ(a.getTxStats(), 1);
}

// Function to check if the implementation works as expected, with an edge case.
TEST(InterfaceA, TestToRx) {
    // Arrange: Create an instance of InterfaceA and initialize it.
    InterfaceA a;
    
    // Act: Call addToRx method on the interface object.
    a.addToRx("test_data");
    
    // Assert: Verify that the data was added to the Rx queue.
    EXPECT_EQ(a.getRxStats(), 1);
}

// Function to check if the implementation works as expected, with a boundary condition.
TEST(InterfaceA, TestInit) {
    // Arrange: Create an instance of InterfaceA and initialize it with some initial values.
    InterfaceA a;
    
    // Act: Call init method on the interface object. It should be called in its default constructor.
    a.init();
    
    // Assert: Verify that the initialization is correct.
    EXPECT_EQ(a.getTxStats(), 0);
}

// Function to check if the implementation works as expected, with an error condition.
TEST(InterfaceA, TestClose) {
    // Arrange: Create an instance of InterfaceA and initialize it.
    InterfaceA a;
    
    // Act: Call close method on the interface object. It should be called in its destructor.
    a.close();
    
    // Assert: Verify that the closing is not possible without destroying the instance.
    EXPECT_THROW(a.close(), std::exception);
}

// Function to check if the implementation works as expected, with boundary conditions.
TEST(InterfaceA, TestToTxBoundary) {
    // Arrange: Create an instance of InterfaceA and initialize it.
    InterfaceA a;
    
    // Act: Call addToTx method on the interface object. It should be called in its default constructor.
    a.addToTx("test_data");
}

// Function to check if the implementation works as expected, with boundary conditions.
TEST(InterfaceA, TestToRxBoundary) {
    // Arrange: Create an instance of InterfaceA and initialize it.
    InterfaceA a;
    
    // Act: Call addToRx method on the interface object. It should be called in its default constructor.
    a.addToRx("test_data");
}

// Function to check if the implementation works as expected, with boundary conditions.
TEST(InterfaceA, TestInitBoundary) {
    // Arrange: Create an instance of InterfaceA and initialize it.
    InterfaceA a;
    
    // Act: Call init method on the interface object. It should be called in its default constructor.
    a.init();
}

// Function to check if the implementation works as expected, with boundary conditions.
TEST(InterfaceA, TestCloseBoundary) {
    // Arrange: Create an instance of InterfaceA and initialize it.
    InterfaceA a;
    
    // Act: Call close method on the interface object. It should be called in its destructor.
    a.close();
}

// Main function to run tests
int main(int argc, char *argv[]) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
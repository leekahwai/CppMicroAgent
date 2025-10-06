WORKSPACE/CppMicroAgent/output/UnitTestCoverage/InterfaceA.cpp

#include <gtest/gtest.h>
#include "InterfaceA.h"

// Test case to verify the implementation of InterfaceA::init()
TEST(InterfaceATest, BasicInitialization) {
    // Arrange
    InterfaceA a;
    
    // Act
    intfTx.init();
    intfRx.init();

    // Assert
    EXPECT_EQ(a.getTxStats(), 0);
    EXPECT_EQ(a.getRxStats(), 0);

    // Act
    a.addToTx(IntfA_Tx());
    a.addToRx(IntfA_Rx());

    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 2);
}

// Test case to verify the implementation of InterfaceA::close()
TEST(InterfaceATest, BasicClosing) {
    // Arrange
    InterfaceA a;
    
    // Act
    intfTx.close();
    intfRx.close();

    // Assert
    EXPECT_EQ(a.getTxStats(), 0);
    EXPECT_EQ(a.getRxStats(), 2);

    // Act
    a.addToTx(IntfA_Tx());
    a.addToRx(IntfA_Rx());

    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 2);
}

// Test case to verify the implementation of InterfaceA::addToTx()
TEST(InterfaceATest, BasicAddToTx) {
    // Arrange
    InterfaceA a;
    struct A a1(A::init());
    
    // Act
    a.addToTx(IntfA_Tx(a1));
    
    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 2);

    // Act
    a.addToTx(IntfA_Rx(a1));
    a.addToRx(IntfA_Rx());

    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 3);
}

// Test case to verify the implementation of InterfaceA::addToRx()
TEST(InterfaceATest, BasicAddToRx) {
    // Arrange
    InterfaceA a;
    struct A a2(A::init());
    
    // Act
    a.addToRx(IntfA_Rx(a2));
    
    // Assert
    EXPECT_EQ(a.getTxStats(), 0);
    EXPECT_EQ(a.getRxStats(), 3);

    // Act
    a.addToTx(IntfA_Tx());
    a.addToRx(IntfA_Rx());

    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 4);
}

// Test case to verify the implementation of InterfaceA::init() method
TEST(InterfaceATest, BasicInit) {
    // Arrange
    intfTx.init();
    intfRx.init();

    // Act
    a = InterfaceA();
    
    // Assert
    EXPECT_EQ(a.getTxStats(), 0);
    EXPECT_EQ(a.getRxStats(), 3);

    // Act
    a.addToTx(IntfA_Tx());
    a.addToRx(IntfA_Rx());

    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 4);
}

// Test case to verify the implementation of InterfaceA::addToRx()
TEST(InterfaceATest, BasicAddToRx) {
    // Arrange
    InterfaceA a;
    struct A a2(A::init());
    
    // Act
    a.addToRx(IntfA_Rx(a2));
    
    // Assert
    EXPECT_EQ(a.getTxStats(), 0);
    EXPECT_EQ(a.getRxStats(), 4);

    // Act
    a.addToTx(IntfA_Tx());
    a.addToRx(IntfA_Rx());

    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 5);
}

// Test case to verify the implementation of InterfaceA::init() method
TEST(InterfaceATest, BasicInit) {
    // Arrange
    intfTx.init();
    intfRx.init();

    // Act
    a = InterfaceA();
    
    // Assert
    EXPECT_EQ(a.getTxStats(), 0);
    EXPECT_EQ(a.getRxStats(), 5);

    // Act
    a.addToTx(IntfA_Tx());
    a.addToRx(IntfA_Rx());

    // Assert
    EXPECT_EQ(a.getTxStats(), 1);
    EXPECT_EQ(a.getRxStats(), 6);
}
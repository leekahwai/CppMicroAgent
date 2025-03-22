/**
 * @file DivisionTest.h
 * @brief This header file defines a class for unit testing mathematical division.
 */

#ifndef DIVISION_TEST_H
#define DIVISION_TEST_H

#include <gtest/gtest.h>
#include <iostream>
#include <stexcept> // For exception handling
#include "Division.h" // Include the Division class definition

/**
 * @class DivisionTest
 * @brief A test suite for the Division class.
 */
class DivisionTest : public ::testing::Test {
protected:
    void SetUp() override {}
    void TearDown() override {}

    Division division_;
};

TEST_F(DivisionTest, DivisionSuccess) {
   // Test successful division
   double result = division_.divide(10.0, 2.0);
   EXPECT_DOUBLE_EQ(result, 5.0);
}

TEST_F(DivisionTest, DivisionZeroDenominator) {
   // Test division by zero with an expected exception
   std::invalid_arg expectedException;
   EXPECT_THROW(division_.divide(1.0, 0.0), std::invalid_argument);

   // Test division by zero without throwing an exception (optional)
   double result = division_.divide(10.0, 0.0);
   EXPECT_ANY_THROW(result); // Use EXPECT_ANY_THROW instead of EXPECT_THROW
}

TEST_F(DivisionTest, DivisionNegativeDenominator) {
   // Test division with a negative denominator
   double result = division_.divide(-10.0, -2.0);
   EXPECT_DOUBLE_EQ(result, 5.0);
}

TEST_F(DivisionTest, DivisionVeryLargeValues) {
   // Test division with very large values
   double result = division_.divide(1000000001.0, 123456789.0);
   EXPECT_DOUBLE_EQ(result, 8.13647037); // Approximate result
}

int main(int argc, char **argv) {
   ::testing::InitGoogleTest(&argc, argv);
   return RUN_ALL_TESTS();
}

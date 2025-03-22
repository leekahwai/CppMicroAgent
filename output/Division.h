/**
 * @file Division.h
 * @brief This header file defines a class for performing mathematical division.
 */

#ifndef DIVISION_H
#define DIVISION_H

#include <iostream>
#include <stdexcept> // For exception handling

/**
 * @class Division
 * @brief A class to perform mathematical division.
 */
class Division {
public:
    /**
     * @brief Performs mathematical division of two numbers.
     * 
     * @param numerator The numerator of the division.
     * @param denominator The denominator of the division.
     * @return The result of the division.
     * @throws std::invalid_argument If the denominator is zero.
     */
    double divide(double numerator, double denominator) {
        if (denominator == 0.0) {
            throw std::invalid_argument("Division by zero is not allowed.");
        }
        return numerator / denominator;
    }
};

#endif // DIVISION_H

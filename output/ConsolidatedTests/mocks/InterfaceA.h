#ifndef MOCK_INTERFACEA_H
#define MOCK_INTERFACEA_H

// Mock header for InterfaceA
// This is a simplified mock for testing purposes

#include <cstdint>
#include <string>
#include "common.h"

class InterfaceA {
public:
    InterfaceA() {}
    ~InterfaceA() {}
    void addToTx(structA& data) {
    }
    void addToRx(structA& data) {
    }
    bool init() {
        return true;
    }
    void close() {
    }
    int getTxStats() {
        return 0;
    }
    int getRxStats() {
        return 0;
    }
};

#endif // MOCK_INTERFACEA_H

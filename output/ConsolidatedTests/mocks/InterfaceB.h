#ifndef MOCK_INTERFACEB_H
#define MOCK_INTERFACEB_H

// Mock header for InterfaceB
// This is a simplified mock for testing purposes

#include <cstdint>
#include <string>
#include "common.h"

class InterfaceB {
public:
    InterfaceB() {}
    ~InterfaceB() {}
    void addToTx(structB& data) {
    }
    void addToRx(structB& data) {
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

#endif // MOCK_INTERFACEB_H

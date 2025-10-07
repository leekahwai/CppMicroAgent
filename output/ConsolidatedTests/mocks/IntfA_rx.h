#ifndef MOCK_INTFA_RX_H
#define MOCK_INTFA_RX_H

// Mock header for IntfA_Rx
// This is a simplified mock for testing purposes

#include <cstdint>
#include <string>
#include "common.h"

class IntfA_Rx {
public:
    IntfA_Rx() {}
    ~IntfA_Rx() {}
    void addToQueue(structA& data) {
    }
    bool init() {
        return true;
    }
    bool close() {
        return true;
    }
};

#endif // MOCK_INTFA_RX_H

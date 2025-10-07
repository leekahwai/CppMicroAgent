#ifndef MOCK_INTFB_RX_H
#define MOCK_INTFB_RX_H

// Mock header for IntfB_Rx
// This is a simplified mock for testing purposes

#include <cstdint>
#include <string>
#include "common.h"

class IntfB_Rx {
public:
    IntfB_Rx() {}
    ~IntfB_Rx() {}
    void addToQueue(structB& data) {
    }
    bool init() {
        return true;
    }
    bool close() {
        return true;
    }
};

#endif // MOCK_INTFB_RX_H

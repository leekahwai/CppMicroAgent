#ifndef MOCK_INTFB_TX_H
#define MOCK_INTFB_TX_H

// Mock header for IntfB_Tx
// This is a simplified mock for testing purposes

#include <cstdint>
#include <string>
#include "common.h"

class IntfB_Tx {
public:
    IntfB_Tx() {}
    ~IntfB_Tx() {}
    bool init() {
        return true;
    }
    bool close() {
        return true;
    }
};

#endif // MOCK_INTFB_TX_H

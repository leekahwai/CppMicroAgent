#ifndef MOCK_INTFA_TX_H
#define MOCK_INTFA_TX_H

// Mock header for IntfA_Tx
// This is a simplified mock for testing purposes

#include <cstdint>
#include <string>

class IntfA_Tx {
public:
    IntfA_Tx() {}
    ~IntfA_Tx() {}
    bool init() {
        return true;
    }
    bool close() {
        return true;
    }
};

#endif // MOCK_INTFA_TX_H

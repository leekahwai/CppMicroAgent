#include <gtest/gtest.h>

// InterfaceA class header file
#ifndef INTERFACE_A
#define INTERFACE_A

#include <thread>
#include "IntfA_tx.h"
#include "IntfA_rx.h"

class InterfaceA {
public:
	InterfaceA();
	~InterfaceA();

	void addToTx(structA& data);
	void addToRx(structA& data);

	bool init();
	void close();

private:
	IntfA_Tx intfTx;
	IntfA_Rx intfRx;

}; // class InterfaceA

#endif  // INTERFACE_A
#ifndef INTERFACE_A
#define INTERFACE_A

#include <thread>
#include "IntfA_tx.h"
#include "IntfA_rx.h"

class InterfaceA {
public:
	InterfaceA();
	~InterfaceA();
	InterfaceA(const InterfaceA&);
	InterfaceA operator=(const InterfaceA&);

	void addToTx(structA& data);
	void addToRx(structA& data);

	bool init();
	void close();
	int getTxStats();
	int getRxStats();

private:
	IntfA_Tx intfTx;
	IntfA_Rx intfRx;

public:
	// Constructor and destructor
	InterfaceA() : intfTx(), intfRx(), intfTx(0), intfRx(0) {}
	~InterfaceA() {}

	// Constructor for InterfaceA
	InterfaceA(const InterfaceA& other);
	InterfaceA& operator=(const InterfaceA& other);

	// Function to add data to the Tx queue
	void addToTx(structA& data);
};

#endif

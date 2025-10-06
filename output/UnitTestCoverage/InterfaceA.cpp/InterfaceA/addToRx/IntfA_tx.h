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
	InterfaceA() : intfTx(IntfA_tx::getDevice()), intfRx(IntfA_rx::getDevice()) {}
};

#endif

#ifndef INTERFACE_B
#define INTERFACE_B

#include <thread>
#include "IntfB_tx.h"
#include "IntfB_rx.h"

class InterfaceB {
public:
	InterfaceB();
	~InterfaceB();
	InterfaceB(const InterfaceB&);
	InterfaceB operator=(const InterfaceB&);

	void addToTx(structB& data);
	void addToRx(structB& data);

	bool init();
	void close();

	int getTxStats();
	int getRxStats();

private:
	IntfB_Tx intfTx;
	IntfB_Rx intfRx;
};

#endif

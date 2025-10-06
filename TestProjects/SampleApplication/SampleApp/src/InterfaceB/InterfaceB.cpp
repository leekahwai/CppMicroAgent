#include "InterfaceB.h"

InterfaceB::InterfaceB() {}

InterfaceB::~InterfaceB() {}

InterfaceB::InterfaceB(const InterfaceB&) {}

InterfaceB InterfaceB::operator=(const InterfaceB&) { return *this; }

bool InterfaceB::init() {
	// Initialization code for InterfaceA
	intfTx.init();
	return true;
}

void InterfaceB::close() {
	// Cleanup code for InterfaceA
	intfTx.close();
}

void InterfaceB::addToTx(structB& data) {
	// Add data to Tx queue
	intfTx.addToQueue(data);
}

void InterfaceB::addToRx(structB& data) {
	// Add data to Rx queue
	intfRx.addToQueue(data);
}

int InterfaceB::getTxStats() {
	// Return Tx statistics
	return intfTx.getStats();
}

int InterfaceB::getRxStats() {
	// Return Rx statistics
	return intfRx.getStats();
}
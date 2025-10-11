#include "InterfaceA.h"

InterfaceA::InterfaceA() { }

InterfaceA::~InterfaceA() {}

InterfaceA::InterfaceA(const InterfaceA&) {}	

InterfaceA InterfaceA::operator=(const InterfaceA&) { return *this; }

bool InterfaceA::init() {
	// Initialization code for InterfaceA
	intfTx.init();
	return true;
}

void InterfaceA::close() {
	// Cleanup code for InterfaceA
	intfTx.close();
}

void InterfaceA::addToTx(structA& data) {
	// Add data to Tx queue
	intfTx.addToQueue(data);
}

void InterfaceA::addToRx(structA& data) {
	// Add data to Rx queue
	intfRx.addToQueue(data);
}

int InterfaceA::getTxStats() {
	// Return Tx statistics
	return intfTx.getStats();
}

int InterfaceA::getRxStats() {
	// Return Rx statistics
	return intfRx.getStats();
}
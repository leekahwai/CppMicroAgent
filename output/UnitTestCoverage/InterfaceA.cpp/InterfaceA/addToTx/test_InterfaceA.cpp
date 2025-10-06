#include <gtest/gtest.h>

using namespace std;
#include "InterfaceA.h"
#include "MockHeaderName.h"

namespace InterfaceATest {
    TEST(InterfaceA, TestInit) {
        // Normal initialization
        InterfaceA a;

        EXPECT_TRUE(a.init());
    }

    TEST(InterfaceA, TestClose) {
        // Cleanup
        intfTx.close();
        intfRx.close();

        // Edge cases:
        // 1. Clean up the Tx queue before closing
        // 2. Close after finishing data transfer

        a.close();
    }
}

Compilation Errors (fix all):
/workspaces/CppMicroAgent/output/UnitTestCoverage/InterfaceA.cpp/InterfaceA/addToTx/test_InterfaceA.cpp: error: cannot open output/UnitTestCoverage/InterfaceA.cpp/InterfaceA/addToTx/build/test_executable-test_InterfaceA.gcno
/workspaces/CppMicroAgent/googletest-1.16.0/googletest/src/gtest-all.cc: error: cannot open output/UnitTestCoverage/InterfaceA.cpp/InterfaceA/addToTx/build/test_executable-gtest-all.gcno
/workspaces/CppMicroAgent/googletest-1.16.0/googletest/src/gtest_main.cc: error: cannot open output/UnitTestCoverage/InterfaceA.cpp/InterfaceA/addToTx/build/test_executable-gtest_main.gcno


Function Being Tested:
#include "InterfaceA.h"

InterfaceA::InterfaceA() { }

InterfaceA::~InterfaceA() {}

InterfaceA::InterfaceA(const InterfaceA&) {}	

InterfaceA InterfaceA::operator=(const InterfaceA&) { return *this; }

bool InterfaceA::init() {
	
	intfTx.init();
	return true;
}

void InterfaceA::close() {
	
	intfTx.close();
}

void InterfaceA::addToTx(structA& data) {
	
	intfTx.addToQueue(data);
}

HEADER FILE:
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
};

#endif


AVAILABLE MOCK HEADERS IN THE SAME DIRECTORY:
IntfA_tx.h
#ifndef INTERFACE_A
#define INTERFACE_A

#include <thread>
#include "IntfA_tx.h"

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
};

#endif
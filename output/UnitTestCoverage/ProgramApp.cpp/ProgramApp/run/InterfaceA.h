
#ifndef PROGRAMAPP_H
#define PROGRAMAPP_H

#include "InterfaceA.h"
#include "InterfaceB.h"

class ProgramApp {
public:
	explicit ProgramApp(InterfaceA a1, InterfaceB b1);
	~ProgramApp();
	void run();

private:
	ProgramApp() = delete;
	InterfaceA a;
	InterfaceB b;

	bool bStart;
};

#endif

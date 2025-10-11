#ifndef PROGRAM_H
#define PROGRAM_H
#include "InterfaceA.h"
#include "InterfaceB.h"


class Program {
public:
	Program();
	~Program();
	void run();
private:
	InterfaceA a;
	InterfaceB b;

};

#endif
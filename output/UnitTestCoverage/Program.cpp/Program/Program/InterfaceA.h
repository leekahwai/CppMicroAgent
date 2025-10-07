#ifndef PROGRAM_H
#define PROGRAM_H

#include <iostream>
using namespace std;

namespace InterfaceA {
    class A {
    public:
        void init() {}
    };
}

namespace InterfaceB {
    class B {
    public:
        void init() {}
    };
}

class Program {
public:
	Program();
	~Program();
	void run();
private:
	InterfaceA::A a;
	InterfaceB::B b;

};

#endif

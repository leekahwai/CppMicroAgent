
#ifndef PROGRAM_H
#define PROGRAM_H

#include <iostream>

namespace InterfaceA {
    class InterfaceA {
        public:
            void init() const { std::cout << "InterfaceA: Init\n"; }
            void run() const { std::cout << "InterfaceA: Run\n"; }
    };
}

namespace InterfaceB {
    class InterfaceB {
        public:
            void init() const { std::cout << "InterfaceB: Init\n"; }
            void run() const { std::cout << "InterfaceB: Run\n"; }
    };
}

class Program {
private:
    InterfaceA a;
    InterfaceB b;

public:
    Program();
    ~Program();
    void run();

};

#endif

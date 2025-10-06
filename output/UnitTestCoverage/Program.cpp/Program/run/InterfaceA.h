#ifndef PROGRAM_H
#define PROGRAM_H

// Include InterfaceA and InterfaceB
#pragma once

#include <InterfaceA.h>
#include <InterfaceB.h>

class Program {
public:
    Program();
    ~Program();

    void run();
private:
    InterfaceA a;
    InterfaceB b;

};

#endif // PROGRAM_H

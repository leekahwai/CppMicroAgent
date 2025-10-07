#include <gtest/gtest.h>

// Program.h
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

#endif // PROGRAM_H

// Program.cpp
#include "Program.h"

Program::Program()
{
}

void Program::run()
{
    InterfaceA a;
    InterfaceB b;
    EXPECT_EQ(a.getValue(), 0); // Should be 0 if the program works correctly
}
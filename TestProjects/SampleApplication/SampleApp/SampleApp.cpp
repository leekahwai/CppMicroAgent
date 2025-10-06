// SampleApp.cpp : Defines the entry point for the application.
//

#include "SampleApp.h"
#include "Program.h"

using namespace std;

int main()
{
	Program program;
	program.run();
	cout << "Hello CMake." << endl;
	return 0;
}

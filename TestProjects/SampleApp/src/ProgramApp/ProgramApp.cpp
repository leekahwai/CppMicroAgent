#include "ProgramApp.h"


ProgramApp::ProgramApp(InterfaceA a1, InterfaceB b1) : 
	a{ a1 }, b{ b1 }, bStart{ false } 
{
}




ProgramApp::~ProgramApp() {
	// Destructor implementation
}

void ProgramApp::run() {
	// Run implementation
	bStart = true;
	while (bStart) {
		a.getRxStats();
		a.getTxStats();
		b.getRxStats();
		b.getTxStats();
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));
	}
}
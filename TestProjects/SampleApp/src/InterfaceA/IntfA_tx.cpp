#include "IntfA_tx.h"
#include <thread>
#include <chrono>

IntfA_Tx::IntfA_Tx() :bStart{ false },vec {} {
}

IntfA_Tx::~IntfA_Tx() {
	vec.clear();
}

auto IntfA_Tx::init() -> bool {
	vec.clear();
	bStart = true;  // FIX: Set flag before starting thread
	std::thread t(&IntfA_Tx::process, this);
	t.detach();
	return true;
}

auto IntfA_Tx::close()->bool {
	bStart = false;
	return true;
}

void IntfA_Tx::process() {
	while (bStart) {
		_mutex.lock(); 
		if (!vec.empty()) {
			auto firstElement = vec.front();
			vec.erase(vec.begin());
		}
		_mutex.unlock();
		std::this_thread::sleep_for(std::chrono::milliseconds(500));
	}
}
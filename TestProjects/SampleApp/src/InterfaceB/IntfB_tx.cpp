#include "IntfB_tx.h"
#include <thread>
#include <chrono>

IntfB_Tx::IntfB_Tx() :bStart{ false },vec {} {
}

IntfB_Tx::~IntfB_Tx() {
	vec.clear();
}

auto IntfB_Tx::init() -> bool {
	vec.clear();
	bStart = true;  // FIX: Set flag before starting thread
	std::thread t(&IntfB_Tx::process, this);
	t.detach();
	return true;
}

auto IntfB_Tx::close()->bool {
	bStart = false;
	return true;
}

void IntfB_Tx::process() {
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
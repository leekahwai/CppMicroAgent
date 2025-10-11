#include "IntfB_rx.h"
#include <thread>
#include <chrono>

IntfB_Rx::IntfB_Rx() :bStart{ false }, vec{} {
}

IntfB_Rx::~IntfB_Rx() {
	vec.clear();
}

auto IntfB_Rx::init() -> bool {
	vec.clear();
	bStart = true;  // FIX: Set flag before starting thread
	std::thread t(&IntfB_Rx::process, this);
	t.detach();

	return true;
}

auto IntfB_Rx::close()->bool {
	bStart = false;
	return true;
}

void IntfB_Rx::process() {
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

void IntfB_Rx::addToQueue(structB& data) {
	std::lock_guard<std::mutex> lock(_mutex);
	vec.push_back(data);
}
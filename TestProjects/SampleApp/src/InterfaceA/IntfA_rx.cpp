#include "IntfA_rx.h"
#include <thread>
#include <chrono>

IntfA_Rx::IntfA_Rx() :bStart{ false }, vec{} {
}

IntfA_Rx::~IntfA_Rx() {
	vec.clear();
}

auto IntfA_Rx::init() -> bool {
	vec.clear();
	bStart = true;  // FIX: Set flag before starting thread
	std::thread t(&IntfA_Rx::process, this);
	t.detach();

	return true;
}

auto IntfA_Rx::close()->bool {
	bStart = false;
	return true;
}

void IntfA_Rx::process() {
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

void IntfA_Rx::addToQueue(structA& data) {
	std::lock_guard<std::mutex> lock(_mutex);

	if (data.a2 < 0) {
		// Process negative numbers
		data.a1 += 1.0f;
	}
	else {
		// Process non-negative numbers
		data.a1 -= 1.0f;
	}
	vec.push_back(data);
}
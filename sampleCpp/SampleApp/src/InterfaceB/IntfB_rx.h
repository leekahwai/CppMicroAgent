#ifndef INTFB_RX_H
#define INTFB_RX_H

#include <vector>
#include <thread>
#include <mutex>
#include "common.h"

class IntfB_Rx {
public:
	IntfB_Rx();
	~IntfB_Rx();
	auto init() -> bool;
	auto close() -> bool;

	void addToQueue(structB& data);

	int getStats() {
		std::lock_guard<std::mutex> lock(_mutex);
		return vec.size();
	}

private:
	void process();

	bool bStart;
	std::mutex _mutex;
	std::vector<structB> vec;
};

#endif

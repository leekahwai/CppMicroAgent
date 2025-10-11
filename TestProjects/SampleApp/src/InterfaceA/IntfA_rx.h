#ifndef INTFA_RX_H
#define INTFA_RX_H

#include <vector>
#include <thread>
#include <mutex>
#include "common.h"

class IntfA_Rx {
public:
	IntfA_Rx();
	~IntfA_Rx();
	auto init() -> bool;
	auto close() -> bool;

	void addToQueue(structA& data);

	int getStats() {
		std::lock_guard<std::mutex> lock(_mutex);
		return static_cast<int>(vec.size());
	}

private:
	void process();

	bool bStart;
	std::mutex _mutex;
	std::vector<structA> vec;
};

#endif

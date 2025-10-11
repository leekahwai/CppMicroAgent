#ifndef INTFB_TX_H
#define INTFB_TX_H

#include <vector>
#include <thread>
#include <mutex>
#include "common.h"

class IntfB_Tx {
public:
	IntfB_Tx();
	~IntfB_Tx();
	auto init() -> bool;
	auto close() -> bool;

	void addToQueue(structB& data) {
		std::lock_guard<std::mutex> lock(_mutex);
		vec.push_back(data);
	}

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

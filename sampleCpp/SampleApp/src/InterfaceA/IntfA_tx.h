#ifndef INTFA_TX_H
#define INTFA_TX_H

#include <vector>
#include <thread>
#include <mutex>
#include "common.h"

class IntfA_Tx {
public:
	IntfA_Tx();
	~IntfA_Tx();
	auto init() -> bool;
	auto close() -> bool;

	void addToQueue(structA& data) {
		std::lock_guard<std::mutex> lock(_mutex);

		if (data.a1 % 2 == 0) {
			// Process even numbers
			data.a2 += 1.0f;
		}
		else {
			// Process odd numbers
			data.a2 -= 1.0f;
		}
		vec.push_back(data);
	}

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

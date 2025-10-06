#include <gtest/gtest.h>

// SampleApp class definition
class SampleApp {
public:
    void run() const;
};

// Program class definition
class Program {
private:
    SampleApp sampleApp;

public:
    void run() const override;
};

void Program::run() const {
    std::cout << "Hello CMake." << std::endl;
}

TEST_F(SampleApp, main) {
    Program program;
    program.run();
}

int main() {
    Program program;
    program.run();
    cout << "Hello CMake." << endl;
    return 0;
}
#include "gtest/gtest.h"

#include "Program.h"
#include "InterfaceA.h"
#include "InterfaceB.h"

class Program : public Program {
public:
    ~Program() override { std::cout << "Program destroyed." << std::endl; }

protected:
    void run() override {
        EXPECT_CALL(*this, a).Times(1);
        return;
    }
};

TEST(ProgramTest, ProgramRun) {
    EXPECT_CALL(*this, a).Times(1);
    auto test = std::make_unique<Program>();
    test->run();
}
// ProgramAppTest.cpp
#include <gtest/gtest.h>
#include <string>

class ProgramApp {
 public:
  explicit ProgramApp(InterfaceA a1, InterfaceB b1);
  ~ProgramApp();

 private:
  ProgramApp() = delete;
  InterfaceA a;
  InterfaceB b;

  bool bStart;
};

TEST(ProgramAppTest, TestRun) {
  // Arrange: Create an instance of the program app and its interfaces
  ProgramApp programApp(InterfaceA("value1"), InterfaceB("value2"));
  
  // Act:
  programApp.run();
  
  // Assert:
  EXPECT_TRUE(programApp.bStart);  // Expected start condition
}
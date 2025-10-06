#include <gtest/gtest.h>
#include "InterfaceA.h"

TEST(InterfaceATests, TestNormal) {
  InterfaceA inta;
  inta.init();
  EXPECT_TRUE(inta.init());
}

// Other tests can be added similarly by creating identical functions and adjusting test code accordingly.

Explanation:
- The `#include` statements are already included in the code snippet provided for you to start with.
- Test cases have been implemented using a `TEST()` macro (`TestNormal`) that calls the corresponding function `init()`.
- Since we're only testing the normal functionality, no external dependencies or mock headers are required.

To generate this test file, you can use the following command:

gtest -v --gtest_output=xml:test/gtest.xml

This will compile and run all the C++ tests in the `InterfaceATests` namespace. If there are no errors, it will create a `.xml` output file named `test/gtest.xml`, which you can open with a text editor for your testing framework of choice (e.g., Visual Studio, Eclipse, or PyTest).
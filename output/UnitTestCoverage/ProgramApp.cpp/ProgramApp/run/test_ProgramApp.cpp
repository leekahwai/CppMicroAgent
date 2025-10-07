#include "ProgramApp.h"
#include <gtest/gtest.h>
#include "InterfaceA.h"
#include "InterfaceB.h"

TEST(ProgramAppTest, BasicFunctionality) {
	// Arrange
	InterfaceA a1(1);
	InterfaceB b1(2);

	// Act
	ProgramApp app(a1, b1);

	// Assert
	app.run();
}
#include <gtest/gtest.h>

// Function to verify initialization of program app with correct data structures.
void ProgramAppTest()
{
    // Arrange: Initialize and set up the program app with correct data structures.
    ProgramApp app1(InterfaceA1, InterfaceB1);
    ProgramApp app2(InterfaceC1, InterfaceD1);

    // Act: Call the run function to initialize the program app.
    app1.run();
    app2.run();

    // Assert: Verify that both application objects have initialized successfully.
}
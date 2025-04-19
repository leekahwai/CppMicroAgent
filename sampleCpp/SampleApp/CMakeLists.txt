cmake_minimum_required(VERSION 3.8)

# Enable Hot Reload for MSVC compilers if supported.
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

project("SampleApp")

option(USE_INTERFACE_A "Use of Interface A" ON)
option(USE_INTERFACE_B "Use of Interface B" ON)

set(SOURCES 
    SampleApp.cpp
    src/Program/Program.cpp
    src/ProgramApp/ProgramApp.cpp
)

include_directories(SampleApp
    inc
    src/Program
    src/ProgramApp
)

if (USE_INTERFACE_A)
  include(${CMAKE_SOURCE_DIR}/src/InterfaceA/__interfaceA.cmake)
endif()

if (USE_INTERFACE_B)
  include(${CMAKE_SOURCE_DIR}/src/InterfaceB/__interfaceB.cmake)
endif()

# Add source to this project's executable by expanding SOURCES properly.
add_executable(SampleApp ${SOURCES})

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET SampleApp PROPERTY CXX_STANDARD 20)
endif()

# TODO: Add tests and install targets if needed.

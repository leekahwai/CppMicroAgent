include_directories(SampleApp
	src/InterfaceB
)

list(APPEND SOURCES
    ${CMAKE_SOURCE_DIR}/src/InterfaceB/InterfaceB.cpp
	${CMAKE_SOURCE_DIR}/src/InterfaceB/IntfB_rx.cpp
	${CMAKE_SOURCE_DIR}/src/InterfaceB/IntfB_tx.cpp
)
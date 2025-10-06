include_directories(SampleApp
	src/InterfaceA
)

list(APPEND SOURCES
    ${CMAKE_SOURCE_DIR}/src/InterfaceA/InterfaceA.cpp
	${CMAKE_SOURCE_DIR}/src/InterfaceA/IntfA_rx.cpp
	${CMAKE_SOURCE_DIR}/src/InterfaceA/IntfA_tx.cpp
)
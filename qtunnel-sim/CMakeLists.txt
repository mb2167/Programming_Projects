cmake_minimum_required(VERSION 3.14)
project(QuantumTunnelling2D LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include_directories(${PROJECT_SOURCE_DIR}/include)

file(GLOB SRC_FILES src/*.cpp)

add_executable(quantum_tunnelling ${SRC_FILES})
if(MSVC)
    target_compile_options(quantum_tunnelling PRIVATE /W4 /O2)
else()
    target_compile_options(quantum_tunnelling PRIVATE -Wall -Wextra -O2)
endif()


cmake_minimum_required(VERSION 3.15)
project(nbody-sim)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Tell the compiler where to find headers
include_directories(${CMAKE_SOURCE_DIR}/include)

add_executable(nbody-sim
    src/main.cpp
    src/physics.cpp
    src/simulation.cpp
)

add_compile_definitions(PROJECT_ROOT_DIR="${CMAKE_SOURCE_DIR}")

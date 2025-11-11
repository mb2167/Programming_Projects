cmake_minimum_required(VERSION 3.14)
project(QuantumTunnelling2D LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include main headers
include_directories(${PROJECT_SOURCE_DIR}/include)

# Include additional headers (recursive search if needed)
include_directories(${PROJECT_SOURCE_DIR}/additional_libraries)

# Gather source files
file(GLOB SRC_FILES src/*.cpp)

# Add executable
add_executable(quantum_tunnelling ${SRC_FILES})

# Compiler options
if(MSVC)
    target_compile_options(quantum_tunnelling PRIVATE /W4 /O2)
else()
    target_compile_options(quantum_tunnelling PRIVATE -Wall -Wextra -O2)
endif()

# Link additional libraries if you have any
# Example:
# link_directories(${PROJECT_SOURCE_DIR}/additional_libraries/lib)
# target_link_libraries(quantum_tunnelling PRIVATE library_name)

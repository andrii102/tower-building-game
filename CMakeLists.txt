cmake_minimum_required(VERSION 3.5)
project(tower-building-game)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)

set(SOURCES src/python/bindings.cpp src/physics/physics.cpp)
include_directories(src/physics)

pybind11_add_module(physics ${SOURCES})

target_include_directories(physics PRIVATE ${CMAKE_SOURCE_DIR}/pybind11/include)


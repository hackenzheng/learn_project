cmake_minimum_required(VERSION 3.13)
project(key_value_server)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(key_value_server
        client.cpp
        convert.cpp
        convert.h
        hashtb.cpp
        hashtb.h
        makefile
        node.h
        README.md
        server.cpp hash_table_list.cpp)

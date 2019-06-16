cmake_minimum_required(VERSION 3.13)
project(libevent_sample)

set(CMAKE_CXX_STANDARD 11)

add_executable(libevent_sample libevent_use.cpp "server_by_select.c" client.c)
add_executable(server_libevent server_libevent.c)
# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.13

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /home/zhg/Downloads/clion-2018.3.4/bin/cmake/linux/bin/cmake

# The command to remove a file.
RM = /home/zhg/Downloads/clion-2018.3.4/bin/cmake/linux/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/zhg/CLionProjects/libevent_sample

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/zhg/CLionProjects/libevent_sample/cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/libevent_sample.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/libevent_sample.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/libevent_sample.dir/flags.make

CMakeFiles/libevent_sample.dir/test.cpp.o: CMakeFiles/libevent_sample.dir/flags.make
CMakeFiles/libevent_sample.dir/test.cpp.o: ../test.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/zhg/CLionProjects/libevent_sample/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/libevent_sample.dir/test.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/libevent_sample.dir/test.cpp.o -c /home/zhg/CLionProjects/libevent_sample/test.cpp

CMakeFiles/libevent_sample.dir/test.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/libevent_sample.dir/test.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/zhg/CLionProjects/libevent_sample/test.cpp > CMakeFiles/libevent_sample.dir/test.cpp.i

CMakeFiles/libevent_sample.dir/test.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/libevent_sample.dir/test.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/zhg/CLionProjects/libevent_sample/test.cpp -o CMakeFiles/libevent_sample.dir/test.cpp.s

CMakeFiles/libevent_sample.dir/server_by_select.c.o: CMakeFiles/libevent_sample.dir/flags.make
CMakeFiles/libevent_sample.dir/server_by_select.c.o: ../server_by_select.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/zhg/CLionProjects/libevent_sample/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object CMakeFiles/libevent_sample.dir/server_by_select.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libevent_sample.dir/server_by_select.c.o   -c /home/zhg/CLionProjects/libevent_sample/server_by_select.c

CMakeFiles/libevent_sample.dir/server_by_select.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libevent_sample.dir/server_by_select.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/zhg/CLionProjects/libevent_sample/server_by_select.c > CMakeFiles/libevent_sample.dir/server_by_select.c.i

CMakeFiles/libevent_sample.dir/server_by_select.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libevent_sample.dir/server_by_select.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/zhg/CLionProjects/libevent_sample/server_by_select.c -o CMakeFiles/libevent_sample.dir/server_by_select.c.s

CMakeFiles/libevent_sample.dir/client.c.o: CMakeFiles/libevent_sample.dir/flags.make
CMakeFiles/libevent_sample.dir/client.c.o: ../client.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/zhg/CLionProjects/libevent_sample/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building C object CMakeFiles/libevent_sample.dir/client.c.o"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/libevent_sample.dir/client.c.o   -c /home/zhg/CLionProjects/libevent_sample/client.c

CMakeFiles/libevent_sample.dir/client.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/libevent_sample.dir/client.c.i"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/zhg/CLionProjects/libevent_sample/client.c > CMakeFiles/libevent_sample.dir/client.c.i

CMakeFiles/libevent_sample.dir/client.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/libevent_sample.dir/client.c.s"
	/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/zhg/CLionProjects/libevent_sample/client.c -o CMakeFiles/libevent_sample.dir/client.c.s

# Object files for target libevent_sample
libevent_sample_OBJECTS = \
"CMakeFiles/libevent_sample.dir/test.cpp.o" \
"CMakeFiles/libevent_sample.dir/server_by_select.c.o" \
"CMakeFiles/libevent_sample.dir/client.c.o"

# External object files for target libevent_sample
libevent_sample_EXTERNAL_OBJECTS =

libevent_sample: CMakeFiles/libevent_sample.dir/test.cpp.o
libevent_sample: CMakeFiles/libevent_sample.dir/server_by_select.c.o
libevent_sample: CMakeFiles/libevent_sample.dir/client.c.o
libevent_sample: CMakeFiles/libevent_sample.dir/build.make
libevent_sample: CMakeFiles/libevent_sample.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/zhg/CLionProjects/libevent_sample/cmake-build-debug/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking CXX executable libevent_sample"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/libevent_sample.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/libevent_sample.dir/build: libevent_sample

.PHONY : CMakeFiles/libevent_sample.dir/build

CMakeFiles/libevent_sample.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/libevent_sample.dir/cmake_clean.cmake
.PHONY : CMakeFiles/libevent_sample.dir/clean

CMakeFiles/libevent_sample.dir/depend:
	cd /home/zhg/CLionProjects/libevent_sample/cmake-build-debug && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/zhg/CLionProjects/libevent_sample /home/zhg/CLionProjects/libevent_sample /home/zhg/CLionProjects/libevent_sample/cmake-build-debug /home/zhg/CLionProjects/libevent_sample/cmake-build-debug /home/zhg/CLionProjects/libevent_sample/cmake-build-debug/CMakeFiles/libevent_sample.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/libevent_sample.dir/depend

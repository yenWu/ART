cmake_minimum_required(VERSION 2.4.6)
include($ENV{ROS_ROOT}/core/rosbuild/rosbuild.cmake)

# Set the build type.  Options are:
#  Coverage       : w/ debug symbols, w/o optimization, w/ code-coverage
#  Debug          : w/ debug symbols, w/o optimization
#  Release        : w/o debug symbols, w/ optimization
#  RelWithDebInfo : w/ debug symbols, w/ optimization
#  MinSizeRel     : w/o debug symbols, w/ optimization, stripped binaries
#set(ROS_BUILD_TYPE RelWithDebInfo)

rosbuild_init()

#set the default path for built executables to the "bin" directory
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/bin)
#set the default path for built libraries to the "lib" directory
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

#uncomment if you have defined messages
rosbuild_genmsg()
#uncomment if you have defined services
#rosbuild_gensrv()

#common commands for building c++ executables and libraries
#rosbuild_add_library(${PROJECT_NAME} src/example.cpp)
#target_link_libraries(${PROJECT_NAME} another_library)
#rosbuild_add_boost_directories()
#rosbuild_link_boost(${PROJECT_NAME} thread)
#rosbuild_add_executable(example examples/example.cpp)
#target_link_libraries(example ${PROJECT_NAME})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
rosbuild_add_executable( firstdemo src/demo_navigation.cpp)
target_link_libraries(firstdemo opencv_core opencv_highgui opencv_imgproc opencv_videostab)

rosbuild_add_executable(manual_arduino src/manual_arduino.cpp)


#ROS challenge1
include_directories( include ..)

rosbuild_add_library(motor_ctl src/motor_ctl.cpp)

rosbuild_add_executable(center_node src/main.cpp)
target_link_libraries(center_node motor_ctl)

rosbuild_add_executable( detectTraffic src/traffic_light_test.cpp)
target_link_libraries(detectTraffic opencv_core opencv_highgui opencv_imgproc opencv_videostab)

rosbuild_add_executable( detectRoad src/line_follower1.cpp)
target_link_libraries( detectRoad opencv_core opencv_highgui opencv_imgproc opencv_videostab)

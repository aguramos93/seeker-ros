# %Tag(FULLTEXT)%
cmake_minimum_required(VERSION 2.8.3)
project(seeker_ros)

## Find catkin and any catkin packages
find_package(catkin REQUIRED COMPONENTS 
  roscpp 
  rospy 
  std_msgs  
  sensor_msgs 
  cv_bridge 
  image_transport
  message_generation
)

## Declare ROS messages and services
add_message_files(
  FILES 
  seekerCamera.msg
)

add_service_files(
  FILES 
  GoToWaypoint.srv
)

## Generate added messages and services
generate_messages(
  DEPENDENCIES 
  std_msgs
)

## Declare a catkin package
catkin_package(
  CATKIN_DEPENDS 
  message_runtime
)

## Build talker and listener
include_directories(include ${catkin_INCLUDE_DIRS})

catkin_install_python(PROGRAMS 
  scripts/talker.py 
  scripts/listener.py 
  scripts/test_video_resource.py 
  scripts/waypoints_server.py
  scripts/track_waypoints.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
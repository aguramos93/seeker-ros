# seeker-ros
A repository to send hexadecimal data to control the gimbal and camera Seeker 10 v2 using ROS.

## Dependencies 
This software has been tested on Ubuntu 16/18.04 with ROS Kinetic/Melodic and Python 3.

Guide to install and configure [ROS](http://wiki.ros.org/melodic/Installation/Ubuntu).

Guide to install [Python3](https://phoenixnap.com/kb/how-to-install-python-3-ubuntu) on Ubuntu 18.04.

To see the streaming of the camera we also need to install opencv:

```
$ sudo apt update
$ sudo apt install python3-opencv
```

## How to install and use
Download from:

```
    $ cd ~/catkin_ws/src
    $ git clone https://github.com/aguramos93/seeker-ros.git
    $ cd ..
```

and then compile using `catkin_make` or `catkin build`.

The detailed instructions to know how to use the camera and gimbal Seeker with ROS are in the [Wiki](https://github.com/aguramos93/seeker-ros/wiki).

## Acknowledgments
Thanks to [grvc-ual](https://github.com/grvcTeam/grvc-ual.git) for the implementation of the GoToWaypoint service and the save and track waypoints scripts.
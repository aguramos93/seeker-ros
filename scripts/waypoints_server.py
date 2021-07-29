#!/usr/bin/env python3

from __future__ import print_function

from seeker_ros.srv import GoToWaypoint, GoToWaypointResponse
import rospy, seeker

def handle_waypoints(path):

    mode_command = path.waypoint.data[0]
    roll_command = path.waypoint.data[1]
    pitch_command = path.waypoint.data[2]
    yaw_command = path.waypoint.data[3]

    my_seeker = seeker.Seeker()

    try:
        my_seeker.open_serial()

        if mode_command == 5:
            Ral, Rah = my_seeker.calculate_angle(roll_command)
            Pal, Pah = my_seeker.calculate_angle(pitch_command)
            Yal, Yah = my_seeker.calculate_angle(yaw_command)
            Rsl, Rsh, Psl, Psh, Ysl, Ysh = 0, 0, 0, 0, 0, 0

        elif mode_command == 1:
            Rsl, Rsh = my_seeker.calculate_speed(roll_command)
            Psl, Psh = my_seeker.calculate_speed(pitch_command)
            Ysl, Ysh = my_seeker.calculate_speed(yaw_command)
            Ral, Rah, Pal, Pah, Yal, Yah = 0, 0, 0, 0, 0, 0

        command = my_seeker.calculate_gimbal_cmd(mode_command, Rsl, Rsh, Ral, Rah, Psl, Psh, Pal, Pah, Ysl, Ysh, Yal, Yah)
        my_seeker.send_command(command)

    except KeyboardInterrupt:
        pass 

    return GoToWaypointResponse()

def waypoints_server():
    rospy.init_node('waypoints_server')
    rospy.Service('seeker/go_to_waypoint', GoToWaypoint, handle_waypoints)
    print("Ready to track waypoints.")
    rospy.spin()

if __name__ == "__main__":
    waypoints_server()
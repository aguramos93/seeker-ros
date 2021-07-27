#!/usr/bin/env python3
import rospy, seeker, time
from std_msgs.msg import Int16MultiArray
from seeker_ros.msg import seekerCamera
import numpy as np

def cbGimbal(data):
    
    mode_command = data.data[0]
    roll_command = data.data[1]
    pitch_command = data.data[2]
    yaw_command = data.data[3]

    my_seeker = seeker.Seeker()

    try:
        my_seeker.open_serial()
        start_time = time.time()

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

def cbCamera(data):
    camera_command = data.cmr_cmd
    camera_time = data.time

    my_seeker = seeker.Seeker()
    my_seeker.open_serial()
    
    command = my_seeker.calculate_camera_cmd(camera_command)
    my_seeker.send_command(command)

def listener():
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('seeker_gimbal', Int16MultiArray, cbGimbal)
    rospy.Subscriber('seeker_camera', seekerCamera, cbCamera)
    
    rospy.spin()

if __name__ == '__main__':
    listener()

#!/usr/bin/env python3
import rospy, seeker, time
from std_msgs.msg import Int16MultiArray
import numpy as np

def callback(data):
    
    mode_command = data.data[0]
    roll_command = data.data[1]
    pitch_command = data.data[2]
    yaw_command = data.data[3]

    print(mode_command, roll_command, pitch_command, yaw_command)

    my_seeker = seeker.Seeker()

    try:
        my_seeker.open_serial()
        start_time = time.time()
        roll_l, roll_h = my_seeker.calculate_angle(roll_command)
        pitch_l, pitch_h = my_seeker.calculate_angle(pitch_command)
        yaw_l, yaw_h = my_seeker.calculate_angle(yaw_command)
        command = my_seeker.calculate_command(mode_command, roll_l, roll_h, pitch_l, pitch_h, yaw_l, yaw_h)
        my_seeker.send_command(command)

    except KeyboardInterrupt:
        pass 

def listener():
    
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('seeker_angle', Int16MultiArray, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()

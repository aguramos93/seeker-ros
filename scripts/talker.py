#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16MultiArray
import numpy as np

def talker():

    pub = rospy.Publisher('seeker_angle', Int16MultiArray, queue_size=1)
    rospy.init_node('talker', anonymous=True)

    angle = Int16MultiArray()

    mode = rospy.get_param('/mode')
    roll = rospy.get_param('/roll')
    pitch = rospy.get_param('/pitch')
    yaw = rospy.get_param('/yaw')

    angle.data = [mode, roll, pitch, yaw]

    rospy.loginfo(angle)
    pub.publish(angle)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

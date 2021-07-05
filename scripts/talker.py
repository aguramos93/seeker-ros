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
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        rospy.loginfo(angle)
        pub.publish(angle)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

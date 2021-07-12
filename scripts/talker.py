#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import String
import numpy as np

def talker():

    pubG = rospy.Publisher('seeker_gimbal', Int16MultiArray, queue_size=1)
    pubC = rospy.Publisher('seeker_camera', String, queue_size=1)
    rospy.init_node('talker', anonymous=True)

    gimbal = Int16MultiArray()
    camera = String()

    mode = rospy.get_param('/mode')
    roll = rospy.get_param('/roll')
    pitch = rospy.get_param('/pitch')
    yaw = rospy.get_param('/yaw')

    cmr_cmd = rospy.get_param('/cmr_cmd')

    gimbal.data = [mode, roll, pitch, yaw]
    camera.data = cmr_cmd
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        # rospy.loginfo(seeker)
        pubG.publish(gimbal)
        pubC.publish(camera)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

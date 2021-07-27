#!/usr/bin/env python3
import rospy
from std_msgs.msg import Int16MultiArray
from seeker_ros.msg import seekerCamera
import numpy as np

def talker():

    pubG = rospy.Publisher('seeker_gimbal', Int16MultiArray, queue_size=1)
    pubC = rospy.Publisher('seeker_camera', seekerCamera, queue_size=1)
    rospy.init_node('talker', anonymous=True)

    gimbal = Int16MultiArray()
    camera = seekerCamera()

    mode = rospy.get_param('/mode')
    roll = rospy.get_param('/roll')
    pitch = rospy.get_param('/pitch')
    yaw = rospy.get_param('/yaw')

    cmr_cmd = rospy.get_param('/camera')
    time = rospy.get_param('/time')

    gimbal.data = [mode, roll, pitch, yaw]
    camera.cmr_cmd = cmr_cmd
    camera.time = time
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        if camera.cmr_cmd == "zoom_in" or camera.cmr_cmd == "zoom_out":
            rospy.sleep(camera.time)
            pubG.publish(gimbal)
            pubC.publish(camera)
            rospy.sleep(camera.time)

            camera.cmr_cmd = "stop_zoom"
            pubC.publish(camera)
            rate.sleep()
        else:
            pubG.publish(gimbal)
            pubC.publish(camera)
            rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

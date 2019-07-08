#!/usr/bin/env python
import time, math, rospy, numpy as np, tf2_ros, geometry_msgs.msg, nav_msgs.msg
import pdb

class Node:
    def __init__(self):
        self.robot_name = rospy.get_param('~robot_name', "pierrette")
        self.odom_sub = rospy.Subscriber('/{}/base_link_truth'.format(self.robot_name), nav_msgs.msg.Odometry, self.odom_cbk, queue_size=1)
        self.odom_pub =  rospy.Publisher('/{}/base_link_truth1'.format(self.robot_name), nav_msgs.msg.Odometry, queue_size=1)
        
    def odom_cbk(self, msg):
        msg.child_frame_id = '{}/base_link'.format(self.robot_name)
        self.odom_pub.publish(msg)
        
    def run(self):
        rospy.spin()
        
if __name__ == '__main__':
    try:
        rospy.init_node('fix_gazebo_thruth', anonymous=True)
        Node().run()
    except rospy.ROSInterruptException: pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import rospy, rospkg
import numpy as np
from nav_msgs.msg import Odometry
import geometry_msgs.msg
from std_srvs.srv import Empty
from gazebo_msgs.srv import SpawnModel, DeleteModel

import pdb
                       
class Agent:
    def __init__(self, x=-1.65, y=1.25):
        model_dir_path = os.path.join(rospkg.RosPack().get_path('common_simulations'), 'models/trr/')
        self.calib_pattern_model = open(model_dir_path+'/cam_calib_pattern/model.sdf','r').read()
        self.pose = geometry_msgs.msg.Pose()
        self.pose.position.x = x; self.pose.position.y = y;
        #self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
        #self.rate = rospy.Rate(1)

    def run(self, what):     
        if what == 'del':
            del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
            del_model_prox('calib_pattern')
        else:
            rospy.wait_for_service('gazebo/spawn_sdf_model')
            spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
            spawn_model_prox('calib_pattern', self.calib_pattern_model, "foo_name_space", self.pose, "world")
            
        rospy.signal_shutdown('done')
        
def main():
    rospy.init_node('load_calib_pattern')
    try:
        agent = Agent()
        agent.run(sys.argv[1])
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()

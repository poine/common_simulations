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

class TrafficLight:
    red, yellow, green, color_nb = range(4)
    color_str = ['red', 'yellow', 'green']
    
    def __init__(self, x=0, y=0):
        model_dir_path = os.path.join(rospkg.RosPack().get_path('common_simulations'), 'models/trr/')
        self.light_models = [open(model_dir_path+'/traffic_light_{}/model.sdf'.format(c),'r').read() for c in TrafficLight.color_str] 
        self.pose = geometry_msgs.msg.Pose()
        self.pose.position.x = x; self.pose.position.y = y; 
        
    def switch_on(self, color):
        rospy.wait_for_service('gazebo/spawn_sdf_model')
        spawn_model_prox = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
        spawn_model_prox(self.model_name(color),
                         self.light_models[color], "foo_name_space", self.pose, "world")
    
    def switch_off(self, color):
        del_model_prox = rospy.ServiceProxy('gazebo/delete_model', DeleteModel)
        del_model_prox(self.model_name(color))


    def model_name(self, color): return 'traffic_light_{}'.format(TrafficLight.color_str[color])
                       
class Agent:
    def __init__(self):
        self.tl1 = TrafficLight(0.75, 2.75)
        #self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)
        #self.rate = rospy.Rate(1)

    def run(self, what):     
        if what == 'on':
            for c in range(TrafficLight.color_nb):
                self.tl1.switch_on(c)
        elif what == 'off':
            for c in range(TrafficLight.color_nb):
                self.tl1.switch_off(c)
        else:
            try:
                c = TrafficLight.color_str.index(what)
                for c1 in range(TrafficLight.color_nb):
                    if c1==c: self.tl1.switch_on(c1)
                    else:  self.tl1.switch_off(c1)
            except ValueError:
                print("argument {} not understood".format(what))
        rospy.signal_shutdown('done')
        
def main():
    rospy.init_node('traffic_light_controller')
    try:
        agent = Agent()
        agent.run(sys.argv[1])
    except rospy.ROSInterruptException:
        pass

if __name__ == '__main__':
    main()

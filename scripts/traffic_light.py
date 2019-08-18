#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time
import rospy, rospkg
import numpy as np
from nav_msgs.msg import Odometry
import geometry_msgs.msg
from std_srvs.srv import Empty
from gazebo_msgs.srv import SpawnModel, DeleteModel

import common_simulations.gazebo_traffic_light as gz_tlight
import pdb


class Agent:
    def __init__(self):
        self.tl1 = gz_tlight.TrafficLight(0.75, 2.25) # TODO/FIXME: adjust position for different tracks
        #self.reset_proxy = rospy.ServiceProxy('/gazebo/reset_simulation', Empty)

    def run(self, what):     
        if what == 'on':
            for c in range(gz_tlight.TrafficLight.color_nb):
                self.tl1.switch_on(c)
        elif what == 'off':
            for c in range(gz_tlight.TrafficLight.color_nb):
                self.tl1.switch_off(c)
        else:
            try:
                c = gz_tlight.TrafficLight.color_str.index(what)
                for c1 in range(gz_tlight.TrafficLight.color_nb):
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

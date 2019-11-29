#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, os, threading, math, numpy as np, time, cv2, yaml
import rospy, sensor_msgs.msg, sensor_msgs.msg, cv_bridge
import subprocess, tempfile


class ArucoSpawner:
    def __init__(self, mid, pose, show_output=True):
        args  = ['roslaunch', 'smocap_gazebo', 'marker.launch']
        args += ['marker_urdf:=fixed_chessboard.urdf.xacro']
        args += ['marker_texture:=Aruco{}'.format(mid), 'marker_name:=marker{}'.format(mid)]
        args += ['{}:={}'.format(_w, _v) for _w, _v in zip(['pos_x', 'pos_y', 'pos_z'], pose[0])]
        args += ['{}:={}'.format(_w, _v) for _w, _v in zip(['rot_R', 'rot_P', 'rot_Y'], pose[1])]
        logfile = None if show_output else tempfile.TemporaryFile()
        print('Spawning marker {}'.format(mid))
        #print(' '.join(args))
        process = subprocess.Popen(args, stdout=logfile)
        process.wait()


def main():
    markers_yaml = {'10':{'rpy': [0, -np.pi/2, 0], 't': [ 0,  3, 0.75]},
                    '11':{'rpy': [0, -np.pi/2, 0], 't': [ 3,  3, 0.75]},
                    '12':{'rpy': [0,  np.pi/2, 0], 't': [-3, -3, 0.75]},
                    '13':{'rpy': [0, -np.pi/2, -np.pi/2], 't': [ 3, -3, 0.75]},
                    '14':{'rpy': [0, -np.pi/2,  np.pi/2], 't': [-3,  3, 0.75]},
                    '15':{'rpy': [0, -np.pi/2,      0], 't': [ 5,  0, 0.75]},
                    '16':{'rpy': [0, -np.pi/2,  np.pi], 't': [-5,  0, 0.75]}}
    for mid in markers_yaml:
        ArucoSpawner(mid, (markers_yaml[mid]['t'], markers_yaml[mid]['rpy']), show_output=True)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    #rospy.init_node('make_aruco_in_room')
    main()

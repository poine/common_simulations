import os, rospy, rospkg
import geometry_msgs.msg
from gazebo_msgs.srv import SpawnModel, DeleteModel

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
                       

#!/usr/bin/env python
# -*- coding: utf-8 -*
import rospy
import dynamic_reconfigure.client
from std_msgs.msg import Bool

class ReconfigureInflationServer:
    def __init__(self):
        self.global_reconfigure_client = dynamic_reconfigure.client.Client('/move_base/global_costmap/inflation_layer')
        self.local_reconfigure_client = dynamic_reconfigure.client.Client('/move_base/local_costmap/inflation_layer')
        self.sub = rospy.Subscriber('/reconfiguration/input',Bool,self.ChangeInflationParams)
        self.origin_global_param = rospy.get_param("/move_base/global_costmap/inflation_layer/inflation_radius")
        self.origin_local_param = rospy.get_param("/move_base/local_costmap/inflation_layer/inflation_radius")

    def ChangeInflationParams(self,boolean):
        print 'start changing inflation params'
        if boolean.data == 1:
            self.global_param = 0
            self.local_param = 0
        else:
            self.global_param = self.origin_global_param
            self.local_param = self.origin_local_param
        self.global_inflation_param = {'inflation_radius' : self.global_param}
        self.local_inflation_param = {'inflation_radius' : self.local_param}
        self.global_config = self.global_reconfigure_client.update_configuration(self.global_inflation_param)
        self.local_config = self.local_reconfigure_client.update_configuration(self.local_inflation_param)
        print 'end' 
        
    
if __name__ == '__main__':
    rospy.init_node('reconfigure_inflation_server')
    reconfiguration = ReconfigureInflationServer()
    rospy.spin()

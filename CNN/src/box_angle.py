#!/usr/bin/env python
#from __builtin__ import True
import numpy as np
import rospy
import math
import torch
import rospkg
from torch import nn
import torch.backends.cudnn as cudnn
from torch.optim.lr_scheduler import CosineAnnealingLR, MultiStepLR
import torchvision
import cv2
import os
from torchvision import transforms, utils, datasets
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Joy
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64,String,Int64

# os.environ['ROS_IP'] = '10.42.0.1'
bridge = CvBridge()
weight_path = '/home/austin/trailnet-testing-Pytorch/2020_summer/src/deep_learning/src/missile_angle.pth'

class CNN_Model(nn.Module):
    def __init__(self):
        super(CNN_Model, self).__init__()
        self.conv1 = nn.Sequential(              
            nn.Conv2d(
                in_channels=3,              
                out_channels=32,            
                kernel_size=4,              
                stride=1,                   
                padding=0,                  
            ),                                                 
            nn.MaxPool2d(kernel_size=2, stride=2),    
        )
        self.conv2 = nn.Sequential(         
            nn.Conv2d(
                in_channels=32,
                out_channels=32,
                kernel_size=4,
                stride=1,
                padding=0,
            ),                           
            nn.MaxPool2d(kernel_size=2, stride=2),                
        )
        self.conv3 = nn.Sequential(         
            nn.Conv2d(
                in_channels=32,
                out_channels=32,
                kernel_size=4,
                stride=1,
                padding=0,
            ),                           
            nn.MaxPool2d(kernel_size=2, stride=2),                
        )
        self.conv4 = nn.Sequential(         
            nn.Conv2d(
                in_channels=32,
                out_channels=32,
                kernel_size=4,
                stride=1,
                padding=1,
            ),                           
            nn.MaxPool2d(kernel_size=2, stride=2),                
        )
        self.fc1 = nn.Linear(34048, 200)
        self.fc2 = nn.Linear(200, 6)
    

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.fc2(x)
        return x


class Angle_pred(object):
    def __init__(self):
        self.node_name = rospy.get_name()
        self.initial()
        self.angle = Int64()
        self.count = 0
        # motor omega output
        self.Angle = np.array([0,90,150,120,30,60])
        rospy.loginfo("[%s] Initializing " % (self.node_name))
        self.pub_angle = rospy.Publisher("/box_pred/angle", Int64, queue_size=1)
        self.image_sub = rospy.Subscriber("/box_pred/img_roi", Image, self.img_cb, queue_size=1)
    
    # load weight
    def initial(self):
        self.model = CNN_Model()
        self.model.load_state_dict(torch.load(weight_path))

       
    # load image to define omega for motor controlling
    def img_cb(self, data):
        #self.dim = (101, 101)  # (width, height)
        self.count += 1
        if self.count == 6:
            self.count = 0
            try:
                # convert image_msg to cv format
                img = bridge.imgmsg_to_cv2(data, desired_encoding = "passthrough")
                #img = cv2.resize(img, self.dim)

                data_transform = transforms.Compose([
                    transforms.ToTensor()])
                img = data_transform(img)
                images = torch.unsqueeze(img,0)
                
                
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                images = images.to(device)
                self.model = self.model.to(device)
                output = self.model(images)
                top1 = output.argmax()
                self.angle = self.Angle[top1]
                self.pub_angle.publish(self.angle)
                
                
                rospy.loginfo('\n'+str(self.angle)+'\n')

            except CvBridgeError as e:
                print(e)



if __name__ == "__main__":
    rospy.init_node("angle_pred", anonymous=False)
    angle_pred = Angle_pred()
    rospy.spin()

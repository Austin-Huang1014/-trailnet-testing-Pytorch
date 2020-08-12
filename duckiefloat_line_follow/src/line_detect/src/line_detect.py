#! /usr/bin/env python

import rospy
import cv2
import numpy as np
import matplotlib.pyplot as plt

#img = cv2.imread('/home/austin/trailnet-testing-Pytorch/2020_summer/src/deep_learning/data/Lane_data/train_data/S/S_degree_30_0236.jpg',1)
#img = cv2.imread('/home/austin/trailnet-testing-Pytorch/2020_summer/src/deep_learning/data/Lane_data/train_data/L/L_degree_300016.jpg',1)
img = cv2.imread('/home/austin/trailnet-testing-Pytorch/2020_summer/src/deep_learning/data/Lane_data/train_data/R/R_degree_30_0275.jpg',1)
while True:
    #----------hsv_trans----------------------#
    Img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #----------detect blue line------------#
    low_red = np.array([50, 150, 100])
    up_red = np.array([220, 255, 255])
    Img = cv2.inRange(Img, low_red, up_red)
    
    #----------optimi----------------#
    kernel = np.ones((3,3), np.uint8)
    Img = cv2.erode(Img, kernel)
    Img = cv2.dilate(Img,kernel)

    #----------find_contour-------------#
    contours, hierarchy = cv2.findContours(Img.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea,reverse=True)


    #----------place box----------------------------#
    blackbox = cv2.minAreaRect(contours[0])
    (x_min, y_min), (w_min, h_min), angle = blackbox #x,y:center local w,h:weight height
    box = cv2.boxPoints(blackbox)
    box = np.int0(box)
    cv2.drawContours(Img,[box],0,(125, 0, 0),3)
    print(angle)

    #----------show--------#
    cv2.imshow('Image',Img)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cv2.destroyAllWindows()
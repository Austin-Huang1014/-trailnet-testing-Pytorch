#! /usr/bin/env python
import rospy
import tkinter as tk
from std_msgs.msg import String
from std_msgs.msg import UInt16, Int16MultiArray

pub = rospy.Publisher('/rgb', Int16MultiArray, queue_size=10)

def set_R(v):
    global k
    k = int(v)

def set_G(v):
    global j
    j = int(v)

def set_B(v):
    global i
    i = int(v)

def PUB():
    global k,j,i
    a = Int16MultiArray()
    a.data = [k,j,i]
    pub.publish(a)

def talker():
  rospy.init_node('pump_controller', anonymous=True)
  rate = rospy.Rate(10)



root = tk.Tk()

s1 = tk.Scale(root,label='R', from_=0, to=255, orient="horizontal",length=600, showvalue=1,tickinterval=15, resolution=1, command=set_R)
s1.pack()

s2 = tk.Scale(root,label='G', from_=0, to=255, orient="horizontal",length=600, showvalue=1,tickinterval=15, resolution=1, command=set_G)
s2.pack()

s3 = tk.Scale(root,label='B', from_=0, to=255, orient="horizontal",length=600, showvalue=1,tickinterval=15, resolution=1, command=set_B)
s3.pack()

btnPumpStart = tk.Button(root, text="RGB PUB", command=PUB)
btnPumpStart.pack()

if __name__ == '__main__':
    k = 0
    j = 0
    i = 0
    try:
        talker()
        root.mainloop()
    except rospy.ROSInterruptException:
        pass

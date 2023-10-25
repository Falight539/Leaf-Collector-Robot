# This Script is the main script of the robot

# Import all important libraries
import numpy as np
import cv2
import math
import time
# Import robot controller class
from controller.robot import Robot

# Import funciton for interacting with AI server
from api.Client import fetch_dir

# Setup. . . (IP, sensor pins, motor, etc..)

# I2C address was setted to 0x0b by defalut
# Servo Driver type was setted to 16 pins by default
# You can change it according to your setup
leaf_collector = Robot()

# IP = 'localhost'
# Port = '1234'

# Test API
# res = fetch_dir(IP, Port, cv2.imread(r'./BuildModel/lil_left.png'))
# print(res)
const =[0.02,0.001,0.0015]
for_angle = 0
one = True
last_ag = 0
count = 0
start = time.time()
left_turncount = 0
right_turncount = 0
# Loop overtime
while True:
    

    if one:
        leaf_collector.set_servo_angle(leaf_collector.for_angle)
        
        one = False

    if action[0]:
        leaf_collector.forward(360-yaw.get_yaw(),0,const)
        if time.time() - start > 5 :
            action[0] = False
            action[1] = True

            start = time.time()

    
    if action[1]:
        #turn to the right
        l_angle, r_angle, l_ratio, r_ratio = turning(-30)
        print(l_angle, r_angle)
        leaf_collector.set_servo_angle(l_angle, r_angle, -1*l_angle, -1*r_angle)
        left_speed = 200*l_ratio if 200*l_ratio >= 80 else 80
        right_speed = 200*r_ratio if 200*r_ratio >= 80 else 80
        leaf_collector.set_speeds(left_speed, right_speed)
        if yaw.get_yaw() == -30:
            l_angle, r_angle, l_ratio, r_ratio = turning(0)
            leaf_collector.set_servo_angle(l_angle, r_angle, -1*l_angle, -1*r_angle)
            leaf_collector.set_speeds(0,0)
            left_turncount += 1

    if action[2]:
        #turn to the right
        l_angle, r_angle, l_ratio, r_ratio = turning(30)
        print(l_angle, r_angle)
        leaf_collector.set_servo_angle(l_angle, r_angle, -1*l_angle, -1*r_angle)
        left_speed = 200*l_ratio if 200*l_ratio >= 80 else 80
        right_speed = 200*r_ratio if 200*r_ratio >= 80 else 80
        leaf_collector.set_speeds(left_speed, right_speed)
        if yaw.get_yaw() == 30:
            l_angle, r_angle, l_ratio, r_ratio = turning(0)
            leaf_collector.set_servo_angle(l_angle, r_angle, -1*l_angle, -1*r_angle)
            leaf_collector.set_speeds(0,0)
            right_turncount += 1
            count += 1


    if left_turncount ==1 and right_turncount == 0:
        action[1] = False 


    if count == 3:
        break



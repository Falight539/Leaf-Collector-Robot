# This Script is the main script of the robot

# Import all important libraries
import numpy as np
import cv2
import math

# Import robot controller class
from controller.robot import Robot

# Import funciton for interacting with AI server
from api.Client import fetch_dir

# Setup. . . (IP, sensor pins, motor, etc..)
leaf_collector = Robot()

IP = 'localhost'
Port = '1234'

# Test API
res = fetch_dir(IP, Port, cv2.imread(r'./BuildModel/lil_left.png'))
print(res)

# Loop overtime
while True:


    break
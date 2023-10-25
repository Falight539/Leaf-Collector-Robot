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
leaf_collector = Robot()

IP = 'localhost'
Port = '1234'

# Test API
res = fetch_dir(IP, Port, cv2.imread(r'./BuildModel/lil_left.png'))
print(res)

last_ag = 0
# Loop overtime
while True:
    



    leaf_collector.set_mxSpeed(255)

    #cp 0
    leaf_collector.forward(last_ag, 0)
    #if last_ag is not 0 then start timer
    if last_ag != 0:
        start_time = time.time()

    # move straight without turning
    #cp 1
    #if time passed 10 second then turn left
    if time.time() - start_time > 10:
        while last_ag != -90:
            leaf_collector.forward(last_ag, -90)
             #wait for 1 second before next iteration
            time.sleep(1)
            #reset timer 
            start_time = time.time()
            break

    leaf_collector.forward(last_ag, 0)
    #cp2
    #if time passed 10 second then turn left
    if time.time() - start_time > 10:
        while last_ag != -90:
            leaf_collector.forward(last_ag, -90)
            time.sleep(1)
            #reset timer
            start_time = time.time()
            break



    leaf_collector.forward(last_ag, 0)
    #cp 2
    #if time passed 10 second then turn left
    if time.time() - start_time > 10:
        while last_ag != -90:
            leaf_collector.forward(last_ag, -90)
            time.sleep(1)
            #reset timer
            start_time = time.time()
            break

    leaf_collector.forward(last_ag, 0)

    #cp 3
    if time.time() - start_time > 5:
        while last_ag != -90:
            leaf_collector.forward(last_ag, -90)
            time.sleep(1)
            #reset timer
            start_time = time.time()
            break
    leaf_collector.forward(last_ag, 0)
    #cp 4
    if time.time() - start_time > 5:
        while last_ag != -90:
            leaf_collector.forward(last_ag, -90)
            time.sleep(1)
            #reset timer
            start_time = time.time()
            break
    #cp 5 ++
    for i in range(0, 10):
        leaf_collector.forward(last_ag, 0)

        if time.time() - start_time > 10:
            while last_ag != 90:
                leaf_collector.forward(last_ag, 90)
                time.sleep(1)
                #reset timer
                start_time = time.time()
                break
        leaf_collector.forward(last_ag, 0)
        if time.time() - start_time > 3:
            while last_ag != 90:
                leaf_collector.forward(last_ag, 90)
                time.sleep(1)
                #reset timer
                start_time = time.time()
                break
        leaf_collector.forward(last_ag, 0)
        if time.time() - start_time > 10:
            while last_ag != -90:
                leaf_collector.forward(last_ag, -90)
                time.sleep(1)
                #reset timer
                start_time = time.time()
                break
        leaf_collector.forward(last_ag, 0)
        if time.time() - start_time > 3:
            while last_ag != -90:
                leaf_collector.forward(last_ag, -90)
                time.sleep(1)
                #reset timer
                start_time = time.time()
                break


    break
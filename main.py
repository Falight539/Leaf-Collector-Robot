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

last_ag = 0
# Loop overtime
while True:

    # Maximum PWM value (refer to Arduino PWM)
    leaf_collector.set_mxSpeed(255)
    # Set the servo pin from the servo driver here
    leaf_collector.set_servo_pins(0, 3, 7, 15)

    # This functino use to move forward with PID 
    # parm1 is current yaw in angle | parm2 is target yaw angle | parm2 is constant p, i, and d respectively
    # Note that all angle is in degree
    # The funciton will send PWM and direction to Arduino Mega via I2C
    # More detail you can take a look on ./controller/robot.py
    straight_yaw = 10 # Should be the value from sensor
    leaf_collector.forward(straight_yaw, 20, [1, 0, 0])

    # This function will use to turn the robot into the desired yaw angle
    # parm1 is current yaw in angle | parm2 is traget yaw angle
    turn_yaw = 10 # Should be the value from sensor
    leaf_collector.turn_by_angle(turn_yaw, 90)

    # Please note that you have to loop overtime to make it reaches to the target

    # Prevent the infinity loop from testing the function >>> remove this when we start running the robot
    break

    # Code below is just a path planning according to the new rule
    ##cp 0
    #leaf_collector.forward(last_ag, 0)
    ##if last_ag is not 0 then start timer
    #if last_ag != 0:
    #    start_time = time.time()
    #
    ## move straight without turning
    ##cp 1
    ##if time passed 10 second then turn left
    #if time.time() - start_time > 10:
    #    while last_ag != -90:
    #        leaf_collector.forward(last_ag, -90)
    #         #wait for 1 second before next iteration
    #        time.sleep(1)
    #        #reset timer 
    #        start_time = time.time()
    #        break
    #
    #leaf_collector.forward(last_ag, 0)
    ##cp2
    ##if time passed 10 second then turn left
    #if time.time() - start_time > 10:
    #    while last_ag != -90:
    #        leaf_collector.forward(last_ag, -90)
    #        time.sleep(1)
    #        #reset timer
    #        start_time = time.time()
    #        break
    #
    #leaf_collector.forward(last_ag, 0)
    ##cp 2
    ##if time passed 10 second then turn left
    #if time.time() - start_time > 10:
    #    while last_ag != -90:
    #        leaf_collector.forward(last_ag, -90)
    #        time.sleep(1)
    #        #reset timer
    #        start_time = time.time()
    #        break
    #
    #leaf_collector.forward(last_ag, 0)
    #
    ##cp 3
    #if time.time() - start_time > 5:
    #    while last_ag != -90:
    #        leaf_collector.forward(last_ag, -90)
    #        time.sleep(1)
    #        #reset timer
    #        start_time = time.time()
    #        break
    #leaf_collector.forward(last_ag, 0)
    ##cp 4
    #if time.time() - start_time > 5:
    #    while last_ag != -90:
    #        leaf_collector.forward(last_ag, -90)
    #        time.sleep(1)
    #        #reset timer
    #        start_time = time.time()
    #        break
    ##cp 5 ++
    #for i in range(0, 10):
    #    leaf_collector.forward(last_ag, 0)
    #
    #    if time.time() - start_time > 10:
    #        while last_ag != 90:
    #            leaf_collector.forward(last_ag, 90)
    #            time.sleep(1)
    #            #reset timer
    #            start_time = time.time()
    #            break
    #    leaf_collector.forward(last_ag, 0)
    #    if time.time() - start_time > 3:
    #        while last_ag != 90:
    #            leaf_collector.forward(last_ag, 90)
    #            time.sleep(1)
    #            #reset timer
    #            start_time = time.time()
    #            break
    #    leaf_collector.forward(last_ag, 0)
    #    if time.time() - start_time > 10:
    #        while last_ag != -90:
    #            leaf_collector.forward(last_ag, -90)
    #            time.sleep(1)
    #            #reset timer
    #            start_time = time.time()
    #            break
    #    leaf_collector.forward(last_ag, 0)
    #    if time.time() - start_time > 3:
    #        while last_ag != -90:
    #            leaf_collector.forward(last_ag, -90)
    #            time.sleep(1)
    #            #reset timer
    #            start_time = time.time()
    #            break
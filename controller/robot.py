import smbus2 as smbus
from adafruit_servokit import ServoKit

def StrTobytes(src: str):
    converted = []
    for b in src:
        converted.append(ord(b))
    return converted

import math
import time

from controller.pid import pid_forward

class Robot:
    def __init__(self, sDriverType=16, arduinoAdd=0x0b):
        self.L_speed = 50
        self.L_dir = 1

        self.R_speed = 50
        self.R_dir = 1
        
        self.ser_kit = ServoKit(channels=sDriverType)
        self.servo = [0, 0, 0, 0]

        self.I2Cadd = arduinoAdd
        self.I2Cbus = smbus.SMBus(1)

        self.mx_speed = 255

        self.prev_error = 0
        self.sum_error = 0
        self.prev_time = -1

    def set_mxSpeed(self, mx_speed: int):
        # Set new max speed according to the system PWM
        self.mx_speed = mx_speed

    def set_servo_pins(self, font_l: int, font_r: int, back_l: int, back_r: int):
        # Set each servo pin from Servo Driver
        self.servo[0] = font_l
        self.servo[1] = font_r
        self.servo[2] = back_l
        self.servo[3] = back_r

    def SendData(self):
        if self.L_dir < 0:
            L_dir = 'B'
        else:
            L_dir = 'F'
        if self.R_dir < 0:
            R_dir = 'B'
        else:
            R_dir = 'F'

        package = "-".join([str(self.L_speed), str(L_dir), str(self.R_speed), str(R_dir)])
        print(package)
        package = StrTobytes(package)
        print(package)
        package = smbus.i2c_msg.write(self.I2Cadd, package)
        # Sending the data via I2C to arduino Mega
        self.I2Cbus.i2c_rdwr(package)

    def set_servos_angle(self, *angles, degree = True):
        for i, angle in enumerate(angles):
            if not degree:
                angle = angle*(180/math.pi)
            self.ser_kit.servo[self.servo[i]].angle = angle

    def set_servo_angle(self, n: int, angle: int, degree = True):
        if not degree:
            angle = angle*(180/math.pi)
        self.ser_kit.servo[self.servo[n]].angle = angle

    def set_speeds(self, L: int, R: int):
        self.L_speed = L
        self.R_speed = R

    def set_dirs(self, L: int, R: int):
        # 1 is forward, -1 is backward
        self.L_dir = L
        self.R_dir = R
    
    def forward(self, pos: int, tar: int, k: list = [1, 0, 0]):

        # The robot use positive and negative of 180 degree system
        # RHS is the positive angle and LHS is the negative angle
        if tar > 180:
            tar = tar - 360
    
        if pos > 180:
            pos = pos - 360

        # Get time for each iteration
        delta_time = 1
        if self.prev_time != -1:
            delta_time = time.time() - self.prev_time
        self.prev_time = time.time()

        # PID calculation
        P = tar - pos # (+) need more left speed, (-) need to more right speed
        I = (self.sum_error + P) * delta_time if self.prev_time != -1 else 0
        D = (P - self.prev_error) / delta_time if self.prev_time != -1 else 0

        # Sum error and mem prev error
        self.sum_error += P
        self.prev_error = P

        # Call the pid function to get new speed and direction
        # k[0] = Kp | k[1] = Ki | k[2] = Kd
        ML, MR = pid_forward(
            (self.L_speed, self.L_dir),
            (self.R_speed, self.R_dir),
            self.mx_speed,
            P*k[0],
            I*k[1],
            D*k[2]
        )

        self.L_speed, self.L_dir = ML[0], ML[1]
        self.R_speed, self.R_dir = MR[0], MR[1]

        self.SendData()
    
    def turn_by_angle(self, pos, tar):

        # Index of each servo
        #
        #        Vacuumer
        #           v
        #   (0) ------ (1)
        #   |            |
        #   |            |
        #   |            |
        #   (2) ------ (3)
        #
        #

        ag_diff = tar - pos # (+) Turn right, (-) Turn left

        # Try to turn servos in the way the make the robot easy to rotate
        self.set_servos_angle(45, -45, -45, 45)

        if abs(ag_diff) > 5:
            self.set_speeds(L=150, R=150)
        else:
            self.set_speeds(50, 50)

        if ag_diff > 0:
            self.set_dirs(L=1, R=-1)
        elif ag_diff < 0:
            self.set_dirs(L=-1, R=1)
        else:
            self.set_speeds(0, 0)
            self.set_dirs(1, 1)
        
        self.SendData()
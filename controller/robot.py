import math
import time

from controller.pid import pid_forward

class Robot:
    def __init__(self):
        self.L_speed = 50
        self.L_dir = 1

        self.R_speed = 50
        self.R_dir = 1
        
        self.servo = [0, 0, 0, 0]

        self.mx_speed = 255

        self.prev_error = 0
        self.sum_error = 0
        self.prev_time = -1

    def set_mxSpeed(self, mx_speed: int):
        # Set new max speed according to the system PWM
        self.mx_speed = mx_speed

    def set_servos_angle(self, *angles, degree = True):
        for i, angle in enumerate(angles):
            if not degree:
                # Convert rad to angle
                angle = angle*(180/math.pi)
            self.servo[i] = angle

    def set_servo_angle(self, n: int, angle: int, degree = True):
        if not degree:
            angle = angle*(180/math.pi)
        self.servo[n] = angle

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
    
    def turn_by_angle(self, tar, pos):

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
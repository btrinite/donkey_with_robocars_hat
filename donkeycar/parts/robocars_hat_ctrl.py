from datetime import datetime
import donkeycar as dk
import re
import time
from donkeycar.parts.actuator import RobocarsHat

class RobocarsHatIn:
    def __init__(self, cfg):

        self.cfg = cfg
        self.inSteering = 0.0
        self.inThrottle = 0.0
        self.inAux1 = 0.0
        self.inAux2 = 0.0

        self.sensor = RobocarsHat(self.cfg)
        self.on = True

    def map_range(self, x, X_min, X_max, Y_min, Y_max):
        '''
        Linear mapping between two ranges of values
        '''
        X_range = X_max - X_min
        Y_range = Y_max - Y_min
        XY_ratio = X_range/Y_range

        return ((x-X_min) / XY_ratio + Y_min)


    def update(self):

        while self.on:
            start = datetime.now()

            l = self.sensor.readline()
            while l:

                params = l.split(',')
                if len(params) == 5 and int(params[0])==1 :
                    self.inThrottle = self.map_range(param[1],
                                                self.cfg.ROBOCARSHAT_PWM_IN_THROTTLE_MIN, self.cfg.ROBOCARSHAT_PWM_IN_THROTTLE_MAX,
                                                -1, 1)
                    self.inSteering = self.map_range(param[2],
                                                self.cfg.ROBOCARSHAT_PWM_IN_STEERING_MIN, self.cfg.ROBOCARSHAT_PWM_IN_STEERING_MAX,
                                                -1, 1)
                l = self.sensor.readline()

                stop = datetime.now()
                s = 0.01 - (stop - start).total_seconds()
                if s > 0:
                    time.sleep(s)

    def run_threaded(self):
        return self.inSteering, self.inThrottle, 'user', False

    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        print('stopping Robocars Hat Controller')
        time.sleep(.5)


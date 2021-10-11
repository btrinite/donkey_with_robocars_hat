from datetime import datetime
import donkeycar as dk
import re
import time

class RobocarsHatIn:
    def __init__(self, cfg):

        self.cfg = cfg
        self.inSteering = 0.0
        self.inThrottle = 0.0
        self.inAux1 = 0.0
        self.inAux2 = 0.0

        self.sensor = dk.parts.actuator.Robocars(self.cfg)
        self.on = True

    def update(self):

        while self.on:
            start = datetime.now()

            l = self.sensor.readline()
            while l:

                params = l.split5(',')
                if len(params == 4):
                    self.inThrottle = self.map_range(param[0],
                                                self.cfg.ROBOCARSHAT_PWM_IN_THROTTLE_MIN, self.cfg.ROBOCARSHAT_PWM_IN_THROTTLE_MAX,
                                                -1, 1)
                    self.inSteering = self.map_range(param[1],
                                                self.cfg.ROBOCARSHAT_PWM_IN_STEERING_MIN, self.cfg.ROBOCARSHAT_PWM_IN_STEERING_MAX,
                                                -1, 1)
                l = self.sensor.teensy_readline()

                stop = datetime.now()
                s = 0.01 - (stop - start).total_seconds()
                if s > 0:
                    time.sleep(s)

    def run_threaded(self):
        return self.inSteering, self.inThrottle

    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        print('stopping Robocars Hat Controller')
        time.sleep(.5)


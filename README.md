# donkeycar: a python self driving library, modified version with support for DIYRobocarsFr Hat

This is modified version of donkeycar to support DIYRobocarsFr Hat.
DIYRobocarsFr Hat is a daughter board (Hat) for Raspberry Pi or Nvidia Jeston Nano to ease the built of autonomous small scale RC-style car like the Donkey car. You can find more about DIYRobocarsFr Hat here :
- [software](https://github.com/btrinite/robocars_hat)
- [hardware](https://github.com/btrinite/robocars_hat_hw)

#### Main changes to integrate RobocarsHat :
- new part : [robocars_hat_ctrl.py](./donkeycar/parts/robocars_hat_ctrl.py) with new Class RobocarsHatIn, which is both a part to add support for receiving throttle and steering command from an RC Receiver and also act as low level driver between raspberry pi/jetson nano and the hat (to control the serial port). The controler part is enabled by setting USE_ROBOCARSHAT_AS_CONTROLLER configuation key to True.
- updated [actuator.py](./donkeycar/parts/actuator.py) with a new Class RobocarsHat that is used to send throttle and steering orders to the hat, enabled by setting DRIVE_TRAIN_TYPE configuration key to ROBOCARSHAT.
- new set of config parameters (search ROBOCARSHAT)
- update [complete.py](./donkeycar/templates/complete.py) with instantiation of RobocarsHatIn and RobocarsHat accordingly to configuration.

Warning : for Raspberry pi 3, you have to get rid of 'miniuart' and resplace it by the true UART device known as PL011.
You will most likely lose Bluetooth. You can check [here](https://www.circuits.dk/setup-raspberry-pi-3-gpio-uart/)

#### Calibration :
PWM signal is supposed to be square signal with positive pulse duration from 1ms to 2ms
This pulse width represents the 'value' carried.
For example, talking about steering, 1ms could mean to turn to the most left, and 2ms to turn to the most right
Pulse width at 1.5ms is then the theoritical idle position for the steering. This is more os less the same for the control of throttle as long as we are talking about cat (1ms means full reverse, 1.5 means idle and 2ms means full forward).
Now, a real Tx/RX signal would not stick strictly on those values. This is why qualibration is needed.

The simple way to qualibrate :
- Make sure your remote control is on idle position
- Make sure your car is on a stand, wheels being free to move in case of
- Connect the Rx Receiver to the Hat
- Connect the ESC control line to the Hat (3 Wire, neede because ESC is in charge to provide power supply to the RX Receiver)
- Power the Hat+Host
- Note the idle, minimum and maximum values reported by the Hat when actioning the remote control
- Update the following configuration items accordingly :
    - ROBOCARSHAT_PWM_IN_THROTTLE_MIN : value reported by Hat when moving remote control to the lowest throttle value
    - ROBOCARSHAT_PWM_IN_THROTTLE_IDLE : value reported by Hat when moving remote control to the default/idle throttle value
    - ROBOCARSHAT_PWM_IN_THROTTLE_MAX : value reported by Hat when moving remote control to the highest throttle value
    - ROBOCARSHAT_PWM_IN_STEERING_MIN : value reported by Hat when moving remote control to the maximum steering postion of one of the direction (the one that provides the minimum value)
    - ROBOCARSHAT_PWM_IN_STEERING_IDLE : value reported by Hat when moving remote control to the default steering postion 
    - ROBOCARSHAT_PWM_IN_STEERING_MAX : value reported by Hat when moving remote control to the maximum steering postion of the other direction (the one that provides the maximum value)

To visualize easely value reported by the Hat, 2 possibilities according to the firmware you use :
- With ROS :
    Dump incoming messages related to radio channes :  

    ``rostopic echo /radio_channels`` 

    Messages contains an array of 4 ints : 

    ``
        ...
        data: [xxxx yyyy, aaaa, bbbb]
    ``
    
- With Simple Serial Protocol (Text Protocol) :  
    Dump incoming messages : 

    `` stty -F /dev/serial0 1000000 raw `` 

    `` cat /dev/serial0 | grep "^1," `` 
 
    Messages like ``1,xxxx,yyyy,aaaa,bbbb`` are the Radio channel messages

Throttle is the first value out of four (xxxx) 
Steering is the second value out of four (yyyy)

If you see only 1500 as value, it means that Rx Receiver PWM signal has not been detected (you should see also status LED blinking either RED or BLUE).

#### DOnkeycar :

[![Build Status](https://travis-ci.org/autorope/donkeycar.svg?branch=dev)](https://travis-ci.org/autorope/donkeycar)
[![CodeCov](https://codecov.io/gh/autoropoe/donkeycar/branch/dev/graph/badge.svg)](https://codecov.io/gh/autorope/donkeycar/branch/dev)
[![PyPI version](https://badge.fury.io/py/donkeycar.svg)](https://badge.fury.io/py/donkeycar)
[![Py versions](https://img.shields.io/pypi/pyversions/donkeycar.svg)](https://img.shields.io/pypi/pyversions/donkeycar.svg)

Donkeycar is minimalist and modular self driving library for Python. It is
developed for hobbyists and students with a focus on allowing fast experimentation and easy
community contributions.

#### Quick Links
* [Donkeycar Updates & Examples](http://donkeycar.com)
* [Build instructions and Software documentation](http://docs.donkeycar.com)
* [Discord / Chat](https://discord.gg/PN6kFeA)

![donkeycar](./docs/assets/build_hardware/donkey2.png)

#### Use Donkey if you want to:
* Make an RC car drive its self.
* Compete in self driving races like [DIY Robocars](http://diyrobocars.com)
* Experiment with autopilots, mapping computer vision and neural networks.
* Log sensor data. (images, user inputs, sensor readings)
* Drive your car via a web or game controller.
* Leverage community contributed driving data.
* Use existing CAD models for design upgrades.

### Get driving.
After building a Donkey2 you can turn on your car and go to http://localhost:8887 to drive.

### Modify your cars behavior.
The donkey car is controlled by running a sequence of events

```python
#Define a vehicle to take and record pictures 10 times per second.

import time
from donkeycar import Vehicle
from donkeycar.parts.cv import CvCam
from donkeycar.parts.tub_v2 import TubWriter
V = Vehicle()

IMAGE_W = 160
IMAGE_H = 120
IMAGE_DEPTH = 3

#Add a camera part
cam = CvCam(image_w=IMAGE_W, image_h=IMAGE_H, image_d=IMAGE_DEPTH)
V.add(cam, outputs=['image'], threaded=True)

#warmup camera
while cam.run() is None:
    time.sleep(1)

#add tub part to record images
tub = TubWriter(path='./dat', inputs=['image'], types=['image_array'])
V.add(tub, inputs=['image'], outputs=['num_records'])

#start the drive loop at 10 Hz
V.start(rate_hz=10)
```

See [home page](http://donkeycar.com), [docs](http://docs.donkeycar.com)
or join the [Discord server](http://www.donkeycar.com/community.html) to learn more.

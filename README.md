# donkeycar: a python self driving library, modified version with support for RobocarsHat

This is modified version of donkeycar to support RobocarsHat.
RobocarsHat is a daughter board (Hat) for Raspberry Pi or Nvidia Jeston Nano to ease the built of a Donkey car
You can find more about RobocarsHat here :
- [software](https://github.com/btrinite/robocars_hat)
- [hardware](https://github.com/btrinite/robocars_hat_hw)

#### Main changes to integrate RobocarsHat :
- new part : [robocars_hat_ctrl.py](./donkeycar/parts/robocars_hat_ctrl.py) with new Class RobocarsHatIn, which is both a part to add support for driving the car from RC and also act as low level driver between raspberry pi/jetson nano and the hat. The controler part is enabled when USE_ROBOCARSHAT_AS_CONTROLLER is set to True.
- updated [actuator.py](./donkeycar/parts/actuator.py) with a new Class RobocarsHat that is used to send throttle qnd steering orders to the hat (when DRIVE_TRAIN_TYPE is set to ROBOCARSHAT)
- new set of config parameters (search ROBOCARSHAT)
- update [complete.py](./donkeycar/templates/complete.py) with instantiation of RobocarsHatIn and RobocarsHat accordingly to configuration


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

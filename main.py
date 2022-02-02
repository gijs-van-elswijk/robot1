#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Image

from stopwatch import *
from events import *

import time

# ---------------------------------------------------------------
# Classes that check for events
class Stopwatch_time_out(Event):
    def __init__(self, reference: Stopwatch, deadline) -> None:
        super().__init__(reference)
        self.deadline = deadline

    def check(self) -> bool:
        self.occurred = getattr(self.reference, 'elapsed')() >= self.deadline
        return self.occurred


class Touchsensor_pressed(Event):
    def __init__(self, reference: TouchSensor) -> None:
        super().__init__(reference)

    def check(self) -> bool:
        self.occurred = getattr(self.reference, 'pressed')()
        return self.occurred


class Object_nearby(Event):
    def __init__(self, reference: InfraredSensor, range) -> None:
        super().__init__(reference)
        self.range = range

    def check(self) -> bool:
        self.occurred = getattr(self.reference, 'distance')() < self.range
        return self.occurred



# Start a stopwatch
sw  = Stopwatch()


# Create a Robot that can subscribe to publisher
robot = Robot('robot', 
 modules = {'brick':     EV3Brick(),
            'touch':     TouchSensor(Port.S1), 
            'screen':    Image('_screen_'),
            'ir':        InfraredSensor(Port.S4),
            'drivebase': DriveBase(Motor(Port.B), Motor(Port.C), 45, 110)
            }
        )


# Make a publisher that can push events to subscribers
pub   = Publisher(('timeout', 'touchpress', 'objectnearby')) # the events that can be published

# Which message does Robot want to receive, and what callbacks to perform in response?
pub.register('timeout', robot, robot.kill)
pub.register('touchpress', robot, robot.beep)
pub.add('touchpress', robot, robot.kill)
pub.register('objectnearby', robot, robot.turn)

# Init messages
robot.modules['brick'].speaker.beep(1000)
robot.modules['screen'].print('Ready!')

# Create list of event detectors used to fill the event queue
evq =  Eventqueue({
    'timeout': Stopwatch_time_out(sw, 30), 
    'touchpress': Touchsensor_pressed(robot.modules['touch']),
    'objectnearby': Object_nearby(robot.modules['ir'], 50)
    })

# Continous event detection loop
ncycles = 0

#robot.modules['drivebase'].drive(100, 0)

while robot.alive:
    
    # Check for events and dispatch all that have occurred
    for ee in evq.occurred_events(): 
       pub.dispatch(ee)

    # Do other things
    robot.modules['drivebase'].straight(-100)

    # Delay in ms
    wait(1)
    
    # Next cycle
    ncycles += 1 

# Finished   
robot.modules['brick'].speaker.beep()
robot.modules['screen'].print('Ready!')

print('Number of cycles: {}'.format(ncycles))
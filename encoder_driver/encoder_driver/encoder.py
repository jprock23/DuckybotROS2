#import RPi.GPIO as GPIO # type: ignore
from math import pi
from shared_utils.constants import MotorDirection

class Encoder:
    def __init__(self, pin, name):
        self.pin = pin
        self.name = name
        self.ticks = 0
        self.direction = MotorDirection.STOPPED
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(pin, GPIO.IN)
        #GPIO.add_event_detect(pin, GPIO.RISING, self.callback)
        
    def callback(self, _):
        if self.direction == MotorDirection.FORWARD:
            self.ticks += 1
        elif self.direction == MotorDirection.BACKWARD:
            self.ticks -= 1
        
    def setDirection(self, dir):
        self.direction = dir
        
    def getDirection(self):
        return self.direction
    
    def getTicks(self):
        return self.ticks
    
    def shutdown(self):
        pass
        #GPIO.remove_event_detect(self.pin)
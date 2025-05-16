import RPi.GPIO as GPIO # type: ignore
from math import pi
from include.constants import MotorDirection

class encoder:
    def __init__(self, pin, name, motor):
        self.pin = pin
        self.name = name
        self.ticks = 0
        self.motor = motor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, self.callback)
        
    def callback(self, _):
        #resolution: 147
        if self.motor.get_direction() == MotorDirection.FORWARD:
            self.ticks += 1
        elif self.motor.get_direction() == MotorDirection.BACKWARD:
            self.ticks -=1
        print(self.name + ":: ", self.ticks * (pi * 6.6)/147)
    
    def shutdown(self):
        GPIO.remove_event_detect(self.pin)
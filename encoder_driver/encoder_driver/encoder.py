"""Module for a motor encoder"""
import RPi.GPIO as GPIO
from threading import Lock
from shared_utils.constants import MotorDirection

class Encoder:
    """Class for interfacing with a motor encoder"""
    def __init__(self, pin):
        self.pin = pin
        self.ticks = 0
        self.direction = MotorDirection.STOPPED
        self._thread_lock = Lock()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, self.callback)
        
        
    def callback(self, _):
        """Increments the tick count when an edge is detected on the pin"""
        with self._thread_lock:
            if self.direction == MotorDirection.FORWARD:
                self.ticks += 1
            elif self.direction == MotorDirection.BACKWARD:
                self.ticks -= 1
        
        
    def set_direction(self, direc):
        """Sets the direction the motor is spinning"""
        with self._thread_lock:
            self.direction = direc
        
        
    def get_direction(self):
        """Returns the direction the motor is spinning"""
        return self.direction
    
    
    def get_ticks(self):
        """Returns the cumulative tick count of the motor"""
        return self.ticks
    
    
    def shutdown(self):
        """Removes the event detector from the gpio pin"""
        GPIO.remove_event_detect(self.pin)
        
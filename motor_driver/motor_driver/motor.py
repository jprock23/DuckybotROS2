"""Driver for the motors"""
from math import floor
from shared_utils.Adafruit_PWM_Servo_Driver import PWM
from shared_utils.constants import MotorDirection, _DIRECTION_TO_SIGNALS, _PWM_VALUES

class PWMMotorDirectionController():
    """Class for handling the pwm signals sent by the pi in order to contol the motors"""
    def __init__(self, in1_pin: int, in2_pin: int, **kwargs):
        self._in1_pin = in1_pin
        self._in2_pin = in2_pin
        if not isinstance(kwargs.get("pwm", None), PWM):
            raise ValueError(
                "You cannot instantiate `PWMMotorDirectionController` without passing a `PWM` object."
            )
        self._pwm = kwargs["pwm"]

    def set(self, direction: MotorDirection):
        """Sets the pwm output signal for the pwm pins"""
        in1_signal, in2_signal = _DIRECTION_TO_SIGNALS[direction]
        in1_value, in2_value = _PWM_VALUES[in1_signal], _PWM_VALUES[in2_signal]
        self._pwm.setPWM(self._in1_pin, *in1_value)
        self._pwm.setPWM(self._in2_pin, *in2_value)

class Motor:
    """Class for an individual motor"""
    _K = 16

    def __init__(
        self, name: str, pwm: PWM, in1_pin: int, in2_pin: int, pwm_pin: int
    ):
        self._pwm = pwm
        self._name = name
        self._in1_pin = in1_pin
        self._in2_pin = in2_pin
        self._pwm_pin = pwm_pin
        self.direction = MotorDirection.STOPPED
        self._controller = PWMMotorDirectionController(in1_pin, in2_pin, pwm=self._pwm)
        
        
    def normalize_speed(self, speed: float):
        """Makes sure pwm values are within a valid range (0-255). Furthermore since duty cycles below 45 aren't enough to get the motors to drive,
        values below this point are set to 0"""
        speed = max(0, min(1, speed))
        speed = floor(abs(speed * 255))
        
        if speed < 45:
            speed = 0
        
        speed = max(0, min(255, speed))
        return speed
        
        
    def set(self, speed: float = 0):
        """Takes in a value between -1 and 1(normalizes value outside this range) and applies them to the motor"""
        if speed < 0:
            self.direction = MotorDirection.BACKWARD
        elif speed > 0:
            self.direction = MotorDirection.FORWARD
        else:
            self.direction = MotorDirection.STOPPED 
        
        self._controller.set(self.direction)       
        speed = self.normalize_speed(speed)
        self._pwm.setPWM(self._pwm_pin, 0, speed * self._K)
        
    def get_direction(self):
        """Returns the direction the motor is spinning"""
        return self.direction

    def __str__(self):
        return (
            f"Motor[name={self._name}"
        )

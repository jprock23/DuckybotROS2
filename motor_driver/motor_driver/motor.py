import RPi.GPIO as GPIO # type: ignore
from include.Adafruit_PWM_Servo_Driver import PWM
from include.constants import MotorDirection, _DIRECTION_TO_SIGNALS, _PWM_VALUES
from math import floor

class PWMMotorDirectionController():
    def __init__(self, in1_pin: int, in2_pin: int, *args, **kwargs):
        self._in1_pin = in1_pin
        self._in2_pin = in2_pin
        if not isinstance(kwargs.get("pwm", None), PWM):
            raise ValueError(
                "You cannot instantiate `PWMMotorDirectionController` " "without passing a `PWM` object."
            )
        self._pwm = kwargs["pwm"]

    def set(self, direction: MotorDirection):
        in1_signal, in2_signal = _DIRECTION_TO_SIGNALS[direction]
        in1_value, in2_value = _PWM_VALUES[in1_signal], _PWM_VALUES[in2_signal]
        self._pwm.setPWM(self._in1_pin, *in1_value)
        self._pwm.setPWM(self._in2_pin, *in2_value)

class Motor:
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
        
    def normalizeSpeed(self, speed: int):
        speed = floor(abs(speed * 255))
        
        if speed < 45:
            speed = 0
        
        speed = max(0, min(255, speed))
        return speed
        
    def set(self, speed: int = 0):
        if speed < 0:
            self.direction = MotorDirection.BACKWARD
        elif speed > 0:
            self.direction = MotorDirection.FORWARD
        else:
            self.direction = MotorDirection.STOPPED 
        
        self._controller.set(self.direction)       
        speed = self.normalizeSpeed(speed)
        self._pwm.setPWM(self._pwm_pin, 0, speed * self._K)
        
    def get_direction(self):
        return self.direction

    def __str__(self):
        return (
            f"Motor[name={self._name}"
        )
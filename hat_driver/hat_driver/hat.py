from motor_driver.motor import Motor
from include.Adafruit_PWM_Servo_Driver import PWM
from include.constants import _MOTOR_NUM_TO_PINS

class Hat():
    def __init__(self, address=0x60, frequency=1600):
        # default I2C address of the HAT
        self._i2caddr = address
        # default @1600Hz PWM frequency
        self._frequency = frequency
        # configure PWM
        self._pwm = PWM(self._i2caddr, debug=False)
        self._pwm.setPWMFreq(self._frequency)
        self._tick = 0

    def get_motor(self, num: int, name: str) -> Motor:
        if num not in _MOTOR_NUM_TO_PINS:
            raise ValueError(
                f"Motor num `{num}` not supported. "
                f"Possible choices are `{_MOTOR_NUM_TO_PINS.keys()}`."
            )
        pins = _MOTOR_NUM_TO_PINS[num]
        return Motor(name, self._pwm, pins.in1, pins.in2, pins.pwm)
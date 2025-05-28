from enum import IntEnum
import dataclasses

LOW, GPIO_LOW, PWM_LOW = 0, 0, 0
HIGH, GPIO_HIGH, PWM_HIGH = 1, 1, 4096

class MotorDirection(IntEnum):
    STOPPED = 0
    FORWARD = 1
    BACKWARD = -1
    
_DIRECTION_TO_SIGNALS = {
        MotorDirection.STOPPED: (LOW, HIGH),
        MotorDirection.FORWARD: (HIGH, LOW),
        MotorDirection.BACKWARD: (LOW, HIGH),
    }

_PWM_VALUES = {
        LOW: (PWM_LOW, PWM_HIGH),
        HIGH: (PWM_HIGH, PWM_LOW),
    }
    
@dataclasses.dataclass
class MotorPins:
    in1: int
    in2: int
    pwm: int
    
_MOTOR_NUM_TO_PINS = {
    1: MotorPins(10, 9, 8),
    2: MotorPins(11, 12, 13),
}
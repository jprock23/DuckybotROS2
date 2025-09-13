"""Node for both of the motors"""
import rclpy
from rclpy.node import Node
from shared_utils.constants import MotorDirection
from hat_driver.hat import Hat
from math import pi

from interfaces.msg import WheelsCmdStamped, Throttle
from geometry_msgs.msg import TwistStamped

class Motor_Node(Node):
    """Class that defines the motor node"""
    def __init__(self):
        super().__init__('motor_node')
        self.ldirc = MotorDirection.STOPPED
        self.rdirc = MotorDirection.STOPPED
        
        #Subscriptions
        # self.cmd_subscription = self.create_subscription(WheelsCmdStamped, '/wheels_cmd', self.set_setpoint, 10)
        # self.velocity_left_subscription = self.create_subscription(TwistStamped, '/left_encoder_node/velocity', self.update_left_vel, 10)
        # self.velocity_right_subscription = self.create_subscription(TwistStamped, '/right_encoder_node/velocity', self.update_right_vel, 10)
        self.throttle_subscription = self.create_subscription(Throttle, '/throttles', self.set_throttles, 10)

        #Publishers
        self.executed_cmd_publisher= self.create_publisher(WheelsCmdStamped, '/wheels_cmd_executed', 10)

        self.hat = Hat()
        self.left_motor = self.hat.get_motor(1, "left")
        self.right_motor = self.hat.get_motor(2, "right")

        self.wheel_radius = .0325

        self.curr_velL = 0.0
        self.curr_velR = 0.0

        self.left_throttle = 0.0
        self.right_throttle = 0.0


    def set_throttles(self, msg: Throttle):
        self.left_motor.set(msg.left_throttle)
        self.right_motor.set(msg.right_throttle)
        print(f'left_throttle:: {msg.left_throttle}, right_throttle:: {msg.right_throttle}')


    def destroy_node(self):
        self.left_motor.set(0)
        self.right_motor.set(0)
        return super().destroy_node()
    
def main(args=None):
    rclpy.init(args=args)
    
    motor_node = Motor_Node()
    try:
        rclpy.spin(motor_node)
    except:
        motor_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
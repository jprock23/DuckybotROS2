"""Node for both of the motors"""
import rclpy
from rclpy.node import Node
from shared_utils.constants import MotorDirection
from hat_driver.hat import Hat
from math import pi
from simple_pid import PID

from interfaces.msg import WheelsCmdStamped, Throttle
from geometry_msgs.msg import TwistStamped

class Motor_Node(Node):
    """Class that defines the motor node"""
    def __init__(self):
        super().__init__('motor_node')
        self.ldirc = MotorDirection.STOPPED
        self.rdirc = MotorDirection.STOPPED
        
        #Subscriptions
        self.cmd_subscription = self.create_subscription(WheelsCmdStamped, '/wheels_cmd', self.set_setpoint, 10)
        self.velocity_left_subscription = self.create_subscription(TwistStamped, '/left_encoder_node/velocity', self.update_left_vel, 10)
        self.velocity_right_subscription = self.create_subscription(TwistStamped, '/right_encoder_node/velocity', self.update_right_vel, 10)
        self.throttle_subscription = self.create_subscription(Throttle, '/throttles', 10)

        #Publishers
        self.executed_cmd_publisher= self.create_publisher(WheelsCmdStamped, '/wheels_cmd_executed', 10)

        kP = 2
        self.left_controller = PID(kP, 0.0, 0.0)
        self.right_controller = PID(kP, 0.0, 0.0)

        self.hat = Hat()
        self.left_motor = self.hat.get_motor(1, "left")
        self.right_motor = self.hat.get_motor(2, "right")

        self.wheel_radius = .0325

        self.curr_velL = 0.0
        self.curr_velR = 0.0

        self.left_throttle = 0.0
        self.right_throttle = 0.0

        # self.time_period = 1/30.0
        # self.control_timer = self.create_timer(self.time_period, self.calculate_control)


    def set_throttles(self, msg: Throttle):
        self.left_motor = msg.left_throttle
        self.right_motor = msg.right_throttle
        print(f'left_throttle:: {msg.left_throttle}, right_throttle:: {msg.right_throttle}')

    def update_left_vel(self, msg: TwistStamped):
        self.curr_velL = msg.twist.linear.x


    def update_right_vel(self, msg: TwistStamped):
        self.curr_velR = msg.twist.linear.x


    def calculate_control(self):
        msg = WheelsCmdStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        self.left_throttle = self.left_controller(self.curr_velL)
        self.right_throttle = self.right_controller(self.curr_velR)

        print("left_val:: ", self.curr_velL)
        print("right_val:: ", self.curr_velR)

        msg.vel_left = self.left_throttle
        msg.vel_right = self.right_throttle
        self.executed_cmd_publisher.publish(msg)
        self.left_motor.set(self.left_throttle)
        self.right_motor.set(self.right_throttle)

        
    def set_setpoint(self, msg: WheelsCmdStamped):
        """callback that subscirbes to the /wheels_cmd topic to get and apply motor controls"""
        self.get_logger().info(f'Time stamp: {msg.header.stamp.sec}, Frame_id: {msg.header.frame_id}, vel_left: {msg.vel_left}, vel_right: {msg.vel_right}')

        self.left_controller.setpoint = max(-0.25, min(msg.vel_left, 0.25))
        self.right_controller.setpoint = max(-0.25, min(msg.vel_right, 0.25))

        print("left_set::", self.left_controller.setpoint)
        print("right_set::", self.right_controller.setpoint)

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

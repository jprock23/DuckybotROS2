import rclpy
from rclpy.node import Node
from simple_pid import PID
from math import pi

from nav_msgs.msg import Odometry
from interfaces.msg import WheelEncoderStamped, WheelsCmdStamped, Throttle

class Controller_Node(Node):
    
    def __init__(self):
        super().__init__('controller_node')
        
        self.wheel_radius = .0325

        self.prev_Lticks = None
        self.prev_Rticks = None

        self.curr_velL = 0.0
        self.curr_velR = 0.0

        self.left_throttle = 0.0
        self.right_throttle = 0.0

        self.setpointL = 0.0
        self.setpointR = 0.0
        
        kP_linear, kI_linear, kD_linear = 4.0, 0.0, 0.0
        self.left_linear_controller = PID(kP_linear, kI_linear, kD_linear)
        self.right_linear_controller = PID(kP_linear, kI_linear, kD_linear)
        
        kP_angular, kI_angular, kD_angular = 1.0, 0.0, 0.0
        self.angular_controller = PID(kP_angular, kI_angular, kD_angular)
        
        #Subscribers
        self.pose_sub = self.create_subscription(Odometry, '/odometry/filtered', 10)
        self.cmd_subscription = self.create_subscription(WheelsCmdStamped, '/wheels_cmd', self.set_setpoint, 10)
        self.encoderL_subscription = self.create_subscription(WheelEncoderStamped, '/left_encoder_node/tick', self.update_left_ticks, 10)
        self.encoderR_subscription = self.create_subscription(WheelEncoderStamped, '/right_encoder_node/tick', self.update_right_ticks, 10)

        #Publishers
        self.executed_cmd_publisher = self.create_publisher(WheelsCmdStamped, '/wheels_cmd_executed', 10)
        self.throttle_publisher = self.create_publisher(Throttle, '/throttles', 10)
        
        self.time_period = 1/30.0
        self.control_timer = self.create_timer(self.time_period, self.calculate_control)

    def update_left_ticks(self, msg: WheelEncoderStamped):
        if (not self.prev_Lticks is None):
            self.curr_velL = (((msg.data - self.prev_Lticks)/float(msg.resolution)) * 2 * pi * self.wheel_radius)/self.time_period
        self.prev_Lticks = msg.data

    def update_right_ticks(self, msg: WheelEncoderStamped):
        if (not self.prev_Rticks is None):
            self.curr_velR = (((msg.data - self.prev_Rticks)/float(msg.resolution)) * 2 * pi * self.wheel_radius)/self.time_period
        self.prev_Rticks = msg.data

    def calculate_control(self):
        executed_msg = WheelsCmdStamped()
        executed_msg.header.stamp = self.get_clock().now().to_msg()
        executed_msg.header.frame_id = 'base_link'
        self.left_throttle = self.left_linear_controller(self.curr_velL)
        self.right_throttle = self.right_linear_controller(self.curr_velR)

        print(f'left_err::{self.setpointL - self.curr_velL}')
        print(f'right_err::{self.setpointR - self.curr_velR}')

        print("left_val:: ", self.left_throttle)
        print("right_val:: ", self.right_throttle)

        executed_msg.vel_left = self.left_throttle
        executed_msg.vel_right = self.right_throttle
        self.executed_cmd_publisher.publish(executed_msg)
        
        throttle_msg = Throttle()
        throttle_msg.left_throttle = self.left_throttle
        throttle_msg.right_throttle = self.right_throttle
        self.throttle_publisher.publish(throttle_msg)

        
    def set_setpoint(self, msg: WheelsCmdStamped):
        """callback that subscirbes to the /wheels_cmd topic to get and apply motor controls"""
        self.get_logger().info(f'Time stamp: {msg.header.stamp.sec}, Frame_id: {msg.header.frame_id}, vel_left: {msg.vel_left}, vel_right: {msg.vel_right}')

        self.left_controller.setpoint = max(-0.25, min(msg.vel_left, 0.25))
        self.right_controller.setpoint = max(-0.25, min(msg.vel_right, 0.25))

        print("left_set::", self.left_controller.setpoint)
        print("right_set::", self.left_controller.setpoint)

    def destroy_node(self):
        self.left_motor.set(0)
        self.right_motor.set(0)
        return super().destroy_node()
        
def main():
    rclpy.init()
    
    controller_node = Controller_Node()
    
    rclpy.spin(controller_node)
    
    controller_node.destroy_node()
    rclpy.shutdown()
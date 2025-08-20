"""Module for the node representing an encoder"""
import rclpy
from rclpy.node import Node
from math import pi

from std_msgs.msg import Header
from geometry_msgs.msg import TwistStamped
from shared_utils.constants import MotorDirection
from interfaces.msg import WheelEncoderStamped, WheelsCmdStamped

from .encoder import Encoder

class Encoder_Node(Node):
    """Node for an encoder"""
    def __init__(self):
        super().__init__('encoder_node')
        
        #Parameters
        self.declare_parameter('configuration', 'left')
        self.declare_parameter('gpio', 18)
        self.declare_parameter('resolution', 135)
        self.declare_parameter('type', 1)

        self.wheel_radius = .0325
        self.prev_ticks = None
        self.prev_time = None
        self.time_period = 1/30
        self.curr_vel = 0.0

        self.configuration = self.get_parameter('configuration').get_parameter_value().string_value
        self.gpio = self.get_parameter('gpio').get_parameter_value().integer_value
        self.resolution = self.get_parameter('resolution').get_parameter_value().integer_value
        self.type = self.get_parameter('type').get_parameter_value().integer_value
        
        #Publishers
        self.tick_publisher = self.create_publisher(WheelEncoderStamped, f"~/tick", 10)
        self.tick_timer = self.create_timer(self.time_period, self.tick_pub)

        self.vel_publisher = self.create_publisher(TwistStamped, f'~/velocity', 10)
        self.velocity_timer = self.create_timer(self.time_period, self.velocity_pub)
        
        #Subscribers
        self.subscriber = self.create_subscription(WheelsCmdStamped, '/wheels_cmd_executed', self.direction_sub, 10)
        
        self.encoder = Encoder(self.gpio)

    def tick_pub(self):
        """Publishes the tick count of the motor"""
        msg = WheelEncoderStamped()
        msg.data = self.encoder.get_ticks()
        msg.resolution = self.resolution
        msg.type = self.type

        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f'duckiebot/{self.configuration}_wheel_axis'
        self.tick_publisher.publish(msg)
        
        # self.get_logger().info(
        #     f'Publishing: Time stamp: {msg.header.stamp.sec}, Frame_id: {msg.header.frame_id}, data:: {msg.data}, resolution:: {msg.resolution}, type:: {msg.type}')
    
    def velocity_pub(self):
        curr_time_tuple = self.get_clock().now().seconds_nanoseconds()
        print("curr_time:: ", curr_time)
        curr_time = float(curr_time_tuple[0] + float(curr_time_tuple[1]/1.0e9))
        if (not self.prev_ticks is None):
            self.curr_vel = (((self.encoder.get_ticks() - self.prev_ticks)/float(self.resolution)) * 2 * pi * self.wheel_radius)/(curr_time - self.prev_time)
        self.prev_ticks = self.encoder.get_ticks()
        print("prev_time:: ", self.prev_time)
        print("time_delta:: ", curr_time - self.prev_time)
        self.prev_time = curr_time

        print("vel:: ", self.curr_vel)
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.twist.linear.x = self.curr_vel
        msg.twist.linear.y = 0.0
        msg.twist.linear.z = 0.0

        self.vel_publisher.publish(msg)

    def direction_sub(self, msg):
        """Subscribes to the /wheels_cmd topic to hear what direction the motor is moving"""
        # self.get_logger().info(f'Heard: left:: {msg.vel_left}, right:: {msg.vel_right}')
        if self.configuration == 'left':
            if msg.vel_left > 0:
                self.encoder.set_direction(MotorDirection.FORWARD)
            elif msg.vel_left < 0:
                self.encoder.set_direction(MotorDirection.BACKWARD)
            else:
                self.encoder.set_direction(MotorDirection.STOPPED)
        elif self.configuration == 'right':
            if msg.vel_right > 0:
                self.encoder.set_direction(MotorDirection.FORWARD)
            elif msg.vel_right < 0:
                self.encoder.set_direction(MotorDirection.BACKWARD)
            else:
                self.encoder.set_direction(MotorDirection.STOPPED)
    
def main(args=None):
    rclpy.init(args=args)
    
    encoder_node = Encoder_Node()
    
    try:
        rclpy.spin(encoder_node)
    except:
        encoder_node.destroy_node()
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
    
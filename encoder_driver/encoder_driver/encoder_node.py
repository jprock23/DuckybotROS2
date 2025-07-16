"""Module for the node representing an encoder"""
import rclpy
from rclpy.node import Node

from std_msgs.msg import Header
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

        self.configuration = self.get_parameter('configuration').get_parameter_value().string_value
        self.gpio = self.get_parameter('gpio').get_parameter_value().integer_value
        self.resolution = self.get_parameter('resolution').get_parameter_value().integer_value
        self.type = self.get_parameter('type').get_parameter_value().integer_value
        
        #Publishers
        self.publisher = self.create_publisher(WheelEncoderStamped, f"~/tick", 10)
        self.timer = self.create_timer(1/30.0, self.tick_pub)
        
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
        self.publisher.publish(msg)
        
        self.get_logger().info(
            f'Publishing: Time stamp: {msg.header.stamp.sec}, Frame_id: {msg.header.frame_id}, data:: {msg.data}, resolution:: {msg.resolution}, type:: {msg.type}')
    
    def direction_sub(self, msg):
        """Subscribes to the /wheels_cmd topic to hear what direction the motor is moving"""
        self.get_logger().info(f'Heard: left:: {msg.vel_left}, right:: {msg.vel_right}')
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
    
import rclpy
from rclpy.node import Node
from .encoder import Encoder

from std_msgs.msg import Header
from shared_utils.constants import MotorDirection
from interfaces.msg import WheelEncoderStamped, WheelsCmdStamped

class Encoder_Node(Node):
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
        self.publisher = self.create_publisher(WheelEncoderStamped, "~/{configuration}/tick".format(configuration=self.configuration), 10)
        self.timer = self.create_timer(0.5, self.tick_pub)
        
        #Subscribers
        self.subscriber = self.create_subscription(WheelsCmdStamped, '/wheels_cmd', self.directiob_sub, 10)
        
        self.encoder = Encoder(self.gpio)

    def tick_pub(self):
        msg = WheelEncoderStamped()
        msg.data = self.encoder.getTicks()
        msg.resolution = self.resolution
        msg.type = self.type

        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = f'duckiebot/{self.configuration}_wheel_axis'
        self.publisher.publish(msg)
        
        self.get_logger().info('Publishing: Time stamp: "%f", Frame_id: "%s", data::"%d", resolution:: "%d", type:: "%d"' % (msg.header.stamp.sec, msg.header.frame_id, msg.data,msg.resolution, msg.type))
    
    def directiob_sub(self, msg):
        self.get_logger().info('Heard: left:: "%s", right:: "%s"' % (msg.vel_left, msg.vel_right))
        if self.configuration == 'left':
            if msg.vel_left > 0:
                self.encoder.setDirection(MotorDirection.FORWARD)
            elif msg.vel_left < 0:
                self.encoder.setDirection(MotorDirection.BACKWARD)
            else:
                self.encoder.setDirection(MotorDirection.STOPPED)
        if self.configuration == 'right':
            if msg.vel_right > 0:
                self.encoder.setDirection(MotorDirection.FORWARD)
            elif msg.vel_right < 0:
                self.encoder.setDirection(MotorDirection.BACKWARD)
            else:
                self.encoder.setDirection(MotorDirection.STOPPED)
    
def main(args=None):
    rclpy.init(args=args)
    
    encoder_node = Encoder_Node()
    
    rclpy.spin(encoder_node)
    
    encoder_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
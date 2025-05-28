import rclpy
from rclpy.node import Node
from .encoder import Encoder

from std_msgs.msg import Header
from shared_utils.constants import MotorDirection
from interfaces.msg import Directions, Encoder as Encoder_msg

class Encoder_Node(Node):
    def __init__(self):
        super().__init__('encoder_node')
        
        self.declare_parameter('enc_name', 'left')
        
        #Publishers
        self.publisher = self.create_publisher(Encoder_msg, '/encoder_msg', 10)
        self.timer = self.create_timer(0.5, self.pub_cb)
        
        #Subscriber
        self.subscriber = self.create_subscription(Directions, '/motor_dirc', self.sub_cb, 10)
        
        self.lEncoder = Encoder(18, 'left')
        self.rEncoder = Encoder(19, "right")

    def pub_cb(self):
        msg = Encoder_msg()
        msg.lticks = self.lEncoder.getTicks()
        msg.rticks = self.rEncoder.getTicks()
        
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        self.publisher.publish(msg)
        
        self.get_logger().info('Publishing: Time stamp: "%s", Frame_id: "%s", lticks::"%s", rticks:: "%s"' % (msg.header.stamp.sec, msg.header.frame_id, msg.lticks, msg.rticks))
    
    def sub_cb(self, msg):
        self.get_logger().info('Heard: left:: "%s", right:: "%s"' % (msg.ldirection, msg.rdirection))
        self.lEncoder.setDirection(MotorDirection(msg.ldirection))
        self.rEncoder.setDirection(MotorDirection(msg.rdirection))
    
def main(args=None):
    rclpy.init(args=args)
    
    encoder_node = Encoder_Node()
    
    rclpy.spin(encoder_node)
    
    encoder_node.destroy_node()
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
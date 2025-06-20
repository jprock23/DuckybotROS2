import rclpy
from rclpy.node import Node

from interfaces.msg import WheelEncoderStamped
from std_msgs.msg import Header

class Encoder_Test_Node(Node):
    def __init__(self):
        super().__init__('encoder_test_node')
        
        self.publisherL = self.create_publisher(WheelEncoderStamped, '/encoder_node/left/tick', 10)
        self.publisherR = self.create_publisher(WheelEncoderStamped, '/encoder_node/right/tick', 10)

        self.TimerL = self.create_timer(0.5, self.left_cb)
        self.TimerR = self.create_timer(0.5, self.right_cb)
        
    def left_cb(self):
        msg = WheelEncoderStamped()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        msg.data = 1
        self.publisherL.publish(msg)
        
    def right_cb(self):
        msg = WheelEncoderStamped()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        
        msg.data = 7
        self.publisherR.publish(msg)
    
def main(args=None):
    rclpy.init(args=args)
    
    encoder_test_node = Encoder_Test_Node()
    
    rclpy.spin(encoder_test_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()

import rclpy
from rclpy.node import Node

from interfaces.msg import WheelsCmdStamped
from std_msgs.msg import Header

class Motor_Test_Node(Node):
    def __init__(self):
        super().__init__('motor_test_node')
        
        self.publisher = self.create_publisher(WheelsCmdStamped, '/wheels_cmd', 10)
        self.Timer = self.create_timer(0.5, self.pub_cb)
        
    def pub_cb(self):
        msg = WheelsCmdStamped()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.vel_left = 1.0
        msg.vel_right = 1.0
        self.publisher.publish(msg)
        
        self.get_logger().info('Publishing: Time stamp: "%s", Frame_id: "%s", vl::"%s", vr:: "%s"' % (msg.header.stamp.sec, msg.header.frame_id, msg.vel_left, msg.vel_right))

def main(args=None):
    rclpy.init(args=args)
    
    motor_test_node = Motor_Test_Node()
    
    rclpy.spin(motor_test_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()

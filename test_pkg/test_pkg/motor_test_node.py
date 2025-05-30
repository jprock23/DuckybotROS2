import rclpy
from rclpy.node import Node

from interfaces.msg import Throttle
from std_msgs.msg import Header

class Motor_Test_Node(Node):
    def __init__(self):
        super().__init__('motor_test_node')
        
        self.publsiher = self.create_publisher(Throttle, '/throttleCmd', 10)
        self.Timer = self.create_timer(0.5, self.pub_cb)
        
    def pub_cb(self):
        msg = Throttle()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.vl = 0.0
        msg.vr = 0.0
        self.publsiher.publish(msg)
        
        self.get_logger().info('Publishing: Time stamp: "%s", Frame_id: "%s", vl::"%s", vr:: "%s"' % (msg.header.stamp.sec, msg.header.frame_id, msg.vl, msg.vr))

def main(args=None):
    rclpy.init(args=args)
    
    motor_test_node = Motor_Test_Node()
    
    rclpy.spin(motor_test_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()

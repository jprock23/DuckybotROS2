import rclpy
from rclpy.node import Node
from hat_driver.hat import Hat

from interfaces.msg import Throttle

class Motor_Node(Node):
    def __init__(self):
        super().__init__('motor_node')
        self.subscription = self.create_subscription(Throttle, 'throttleCmd', self.listener_cb, 10)
        self.subscription
        
        self.hat = Hat()
        self.leftMotor = self.hat.get_motor(1, "left")
        self.rightMotor = self.hat.get_motor(2, "right")
        
        
    def listener_cb(self, msg):
        self.get_logger().info('Time stamp: "%d", Frame_id: "%s", v1: "%d", v2: "%d"' % (msg.header.stamp.sec, msg.header.frame_id, msg.v1, msg.v2))
        self.leftMotor.set(msg.v1)
        self.rightMotor.set(msg.v2)
        
    
def main(args=None):
    rclpy.init(args=args)
    
    motor_node = Motor_Node()
    
    rclpy.spin(motor_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
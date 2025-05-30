import rclpy
from rclpy.node import Node
from shared_utils.constants import MotorDirection
from hat_driver.hat import Hat

from std_msgs.msg import Header
from interfaces.msg import Throttle, Directions

class Motor_Node(Node):
    def __init__(self):
        super().__init__('motor_node')
        
        self.ldirc = MotorDirection.STOPPED
        self.rdirc = MotorDirection.STOPPED
        
        #Publishers
        self.publisher = self.create_publisher(Directions, '/motor_dirc', 10)
        self.Timer = self.create_timer(0.5, self.dir_cb)
        
        #Subscriptions
        self.subscription = self.create_subscription(Throttle, '/throttleCmd', self.listener_cb, 10)
        
        self.hat = Hat()
        self.leftMotor = self.hat.get_motor(1, "left")
        self.rightMotor = self.hat.get_motor(2, "right")
        
    def dir_cb(self):
        msg = Directions()
        msg.ldirection = self.ldirc
        msg.rdirection = self.rdirc
        
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        self.publisher.publish(msg)
        
        
    def listener_cb(self, msg):
        self.get_logger().info('Time stamp: "%f", Frame_id: "%s", vl: "%f", vr: "%f"' % (msg.header.stamp.sec, msg.header.frame_id, msg.vl, msg.vr))
        if(msg.vl < 0):
            self.ldirc = MotorDirection.BACKWARD
        elif(msg.vl > 0):
            self.ldirc = MotorDirection.FORWARD
        else:
            self.ldirc = MotorDirection.STOPPED
        
        if(msg.vr < 0):
            self.rdirc = MotorDirection.BACKWARD
        elif(msg.vr > 0):
            self.rdirc = MotorDirection.FORWARD
        else:
            self.rdirc = MotorDirection.STOPPED
            
        self.leftMotor.set(msg.vl)
        self.rightMotor.set(msg.vr)
        
    
def main(args=None):
    rclpy.init(args=args)
    
    motor_node = Motor_Node()
    
    rclpy.spin(motor_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
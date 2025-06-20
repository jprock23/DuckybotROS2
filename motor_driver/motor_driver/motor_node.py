import rclpy
from rclpy.node import Node
from shared_utils.constants import MotorDirection
from hat_driver.hat import Hat

from std_msgs.msg import Header
from interfaces.msg import WheelsCmdStamped

class Motor_Node(Node):
    def __init__(self):
        super().__init__('motor_node')
        
        self.ldirc = MotorDirection.STOPPED
        self.rdirc = MotorDirection.STOPPED
        
        #Subscriptions
        self.subscription = self.create_subscription(WheelsCmdStamped, '/wheels_cmd', self.motor_cb, 10)
        
        self.hat = Hat()
        self.leftMotor = self.hat.get_motor(1, "left")
        self.rightMotor = self.hat.get_motor(2, "right")
    
        
    def motor_cb(self, msg):
        self.get_logger().info('Time stamp: "%f", Frame_id: "%s", vl: "%f", vr: "%f"' % (msg.header.stamp.sec, msg.header.frame_id, msg.vl, msg.vr))
        if(msg.vel_left < 0):
            self.ldirc = MotorDirection.BACKWARD
        elif(msg.vel_left > 0):
            self.ldirc = MotorDirection.FORWARD
        else:
            self.ldirc = MotorDirection.STOPPED
        
        if(msg.vel_right < 0):
            self.rdirc = MotorDirection.BACKWARD
        elif(msg.vel_right > 0):
            self.rdirc = MotorDirection.FORWARD
        else:
            self.rdirc = MotorDirection.STOPPED
            
        self.leftMotor.set(msg.vel_left)
        self.rightMotor.set(msg.vel_right)
        
        
    
def main(args=None):
    rclpy.init(args=args)
    
    motor_node = Motor_Node()
    
    rclpy.spin(motor_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()
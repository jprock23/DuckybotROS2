"""Node for both of the motors"""
import rclpy
from rclpy.node import Node
from shared_utils.constants import MotorDirection
from hat_driver.hat import Hat

from interfaces.msg import WheelsCmdStamped

class Motor_Node(Node):
    """Class that defines the motor node"""
    def __init__(self):
        super().__init__('motor_node')
        self.ldirc = MotorDirection.STOPPED
        self.rdirc = MotorDirection.STOPPED
        #Subscriptions
        self.subscription = self.create_subscription(WheelsCmdStamped, '/wheels_cmd', self.motor_cb, 10)
        self.hat = Hat()
        self.left_motor = self.hat.get_motor(1, "left")
        self.right_motor = self.hat.get_motor(2, "right")

        self.timer = self.create_timer(1.0, self.check_timeout)

        self.last_msg_time = self.get_clock().now().to_msg()
        
    def check_timeout(self):
        curr_time = self.get_clock().now().to_msg()

        time_delta = (float(curr_time.sec) + (float(curr_time.nanosec/1e9))) - (float(self.last_msg_time.sec) + (float(self.last_msg_time.nanosec/1e9)))
        if(time_delta > 1.0):
            self.left_motor.set(0.0)
            self.right_motor.set(0.0)

    def motor_cb(self, msg):
        """callback that subscirbes to the /wheels_cmd topic to get and apply motor controls"""
        self.get_logger().info(f'Time stamp: {msg.header.stamp.sec}, Frame_id: {msg.header.frame_id}, vel_left: {msg.vel_left}, vel_right: {msg.vel_right}')
            
        self.left_motor.set(msg.vel_left)
        self.right_motor.set(msg.vel_right)
        self.last_msg_time = msg.header.stamp
        
    
def main(args=None):
    rclpy.init(args=args)
    
    motor_node = Motor_Node()
    
    rclpy.spin(motor_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()

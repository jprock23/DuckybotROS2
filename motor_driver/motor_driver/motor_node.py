"""Node for both of the motors"""
import rclpy
from rclpy.node import Node
from shared_utils.constants import MotorDirection
from hat_driver.hat import Hat
from math import pi

from interfaces.msg import WheelsCmdStamped, WheelEncoderStamped

class Motor_Node(Node):
    """Class that defines the motor node"""
    def __init__(self):
        super().__init__('motor_node')
        self.ldirc = MotorDirection.STOPPED
        self.rdirc = MotorDirection.STOPPED
        #Subscriptions
        self.cmd_subscription = self.create_subscription(WheelsCmdStamped, '/wheels_cmd', self.set_setpoint, 10)
        self.encoderL_subscription = self.create_subscription(WheelEncoderStamped, '/left_encoder_node/ticks', self.update_left_ticks, 10)
        self.encoderR_subscription = self.create_subscription(WheelEncoderStamped, '/right_encoder_node/ticks', self.update_right_ticks, 10)

        self.hat = Hat()
        self.left_motor = self.hat.get_motor(1, "left")
        self.right_motor = self.hat.get_motor(2, "right")

        self.wheel_radius = .0325

        self.prev_Lticks = 0
        self.prev_Rticks = 0

        self.curr_velL = 0.0
        self.curr_velR = 0.0

        self.left_val = 0.0
        self.right_val = 0.0

        self.setpointL = 0.0
        self.setpointR = 0.0

        self.kP = 1.0

        self.control_timer = self.create_timer(1/30.0, self.calculate_control)

        self.last_msg_time = self.get_clock().now().to_msg()

    def update_left_ticks(self, msg):
        self.curr_velL = ((msg.data - self.prev_Lticks)/msg.resolution) * 2 * pi * self.wheel_radius
        self.prev_Lticks = msg.data

    def update_right_ticks(self, msg):
        self.curr_velR = ((msg.data - self.prev_Rticks)/msg.resolution) * 2 * pi * self.wheel_radius
        self.prev_Rticks = msg.data

    def calculate_control(self):
        curr_time = self.get_clock().now().to_msg()
        time_delta = (float(curr_time.sec) + (float(curr_time.nanosec/1e9))) - (float(self.last_msg_time.sec) + (float(self.last_msg_time.nanosec/1e9)))
        if(time_delta >= 1.0):
            self.setpointL = 0.0
            self.setpointR = 0.0
            self.left_val = 0.0
            self.right_val = 0.0
        else:
            print(f'left err:: {self.setpointL - self.curr_velL}, right err:: {self.setpointR - self.curr_velR}')
            self.left_val += (self.setpointL - self.curr_velL) * self.kP
            self.right_val += (self.setpointR - self.curr_velR) * self.kP
        self.left_motor.set(self.left_val)
        self.right_motor.set(self.right_val)
        
    def set_setpoint(self, msg):
        """callback that subscirbes to the /wheels_cmd topic to get and apply motor controls"""
        self.get_logger().info(f'Time stamp: {msg.header.stamp.sec}, Frame_id: {msg.header.frame_id}, vel_left: {msg.vel_left}, vel_right: {msg.vel_right}')
        self.last_msg_time = self.get_clock().now().to_msg() # using the time when msg is received

        self.setpointL = max(-0.25, min(msg.vel_left, 0.25))
        self.setpointR = max(-0.25, min(msg.vel_right, 0.25))
        
    
def main(args=None):
    rclpy.init(args=args)
    
    motor_node = Motor_Node()
    
    rclpy.spin(motor_node)
    
    rclpy.shutdown()
    
if __name__ == "__main__":
    main()

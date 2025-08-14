from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped, StaticTransformBroadcaster

class StatePublisher(Node):

    def __init__(self):
        rclpy.init()
        super().__init__('state_publisher')

        # self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = StaticTransformBroadcaster(self)
        self.nodeName = self.get_name()
        self.get_logger().info("{0} started".format(self.nodeName))
        
        # message declarations
        chassis_transform = TransformStamped()
        chassis_transform.header.frame_id = 'base_link'
        chassis_transform.child_frame_id = 'chassis'
        chassis_transform.transform.translation.x = 0.0
        chassis_transform.transform.translation.y = 0.0
        chassis_transform.transform.translation.z = 0.0325

        chassis_transform.transform.rotation.x = 0.0
        chassis_transform.transform.rotation.y = 0.0
        chassis_transform.transform.rotation.z = 0.0
        chassis_transform.transform.rotation.z = 1.0


        left_wheel_axis_transform = TransformStamped()
        left_wheel_axis_transform.header.frame_id = 'chassis'
        left_wheel_axis_transform.child_frame_id = 'aarrgrpi/left_wheel_axis'

        right_wheel_axis_transform = TransformStamped()
        right_wheel_axis_transform.header.frame_id = 'chassis'
        right_wheel_axis_transform.child_frame_id = 'right_wheel_axis'

        camera_transform = TransformStamped()
        camera_transform.header.frame_id = 'chassis'
        camera_transform.child_frame_id = 'camera'

        computer_transform = TransformStamped()
        computer_transform.header.frame_id = 'chassis'
        computer_transform.child_frame_id = 'computer'

        left_wheel_axis_transform.transform.translation.x = 0.0
        left_wheel_axis_transform.transform.translation.y = 0.07
        left_wheel_axis_transform.transform.translation.z = 0.0

        left_wheel_axis_transform.transform.rotation.x = 0.0
        left_wheel_axis_transform.transform.rotation.y = 0.0
        left_wheel_axis_transform.transform.rotation.z = 0.0
        left_wheel_axis_transform.transform.rotation.z = 1.0

        self.broadcaster.sendTransform(left_wheel_axis_transform)
        self.broadcaster.sendTransform(chassis_transform)

def euler_to_quaternion(roll, pitch, yaw):
    qx = sin(roll/2) * cos(pitch/2) * cos(yaw/2) - cos(roll/2) * sin(pitch/2) * sin(yaw/2)
    qy = cos(roll/2) * sin(pitch/2) * cos(yaw/2) + sin(roll/2) * cos(pitch/2) * sin(yaw/2)
    qz = cos(roll/2) * cos(pitch/2) * sin(yaw/2) - sin(roll/2) * sin(pitch/2) * cos(yaw/2)
    qw = cos(roll/2) * cos(pitch/2) * cos(yaw/2) + sin(roll/2) * sin(pitch/2) * sin(yaw/2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)

def main():
    node = StatePublisher()

if __name__ == '__main__':
    main()
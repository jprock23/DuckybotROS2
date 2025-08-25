from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description()->LaunchDescription:
    
    encoder_launch_dir = PathJoinSubstitution([FindPackageShare('encoder_driver'), 'launch'])
    camera_launch_dir = PathJoinSubstitution([FindPackageShare('robot_camera'), 'launch'])
    
    motors = Node(
        package='motor_driver',
        executable='motor'
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PathJoinSubstitution([encoder_launch_dir, "encoder.launch.py"])
        ),
        IncludeLaunchDescription(
            PathJoinSubstitution([camera_launch_dir, "camera.launch.py"])
        ),
        motors
    ])
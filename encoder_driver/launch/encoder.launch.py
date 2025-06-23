from launch import LaunchDescription
from launch_ros.actions import Node

package_name = 'encoder_driver'

def generate_launch_description()->LaunchDescription:
    
    left_encoder  = Node(
            package=package_name,
            executable='encoder',
            name='left_encoder_node',
            parameters=[{
                'gpio': 18,
                'configuration': 'left',
                'resolution': 135,
                'type': 1, 
            }]
        )   
        
    right_encoder  = Node(
            package=package_name,
            executable='encoder',
            name='right_encoder_node',
            parameters=[{
                'gpio': 19,
                'configuration': 'right',
                'resolution': 135,
                'type': 1, 
            }]
        )
    
    
    return LaunchDescription([
        left_encoder,
        right_encoder,              
    ])
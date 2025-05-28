import rclpy
from .camera import Camera
from rclpy.node import Node
from cv_bridge import CvBridge

from sensor_msgs.msg import CompressedImage
from interfaces.srv import GetImage

class Camera_Node(Node):
    def __init__(self):
        super().__init__('camera_node')
        
        self.bridge = CvBridge()
        self.camera = Camera()
        
        self.srv = self.create_service(GetImage, '/camera_img', self.cb)
        
    def cb(self, request, response):
        response.Image = self.bridge.cv2_to_compressed_imgmsg(self.camera.getFrame())
        
        return response
        
def main():
    rclpy.init()
    
    camera_node = Camera_Node()
    
    rclpy.spin(camera_node)
    
    rclpy.shutdown()

if __name__ == "__main__":
    main()

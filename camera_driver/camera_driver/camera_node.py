import rclpy
from .camera import Camera
from rclpy.node import Node
from cv_bridge import CvBridge

from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import Header

from interfaces.srv import GetImage

class Camera_Node(Node):
    def __init__(self):
        super().__init__('camera_node')
        
        self.bridge = CvBridge()
        self.camera = Camera()
        
        #self.srv = self.create_service(GetImage, '/camera_img', self.cb)
        self.publisher = self.create_publisher(Image, '/camera_img', 10)
        self.Timer = self.create_timer(0.5, self.pcb)
    
    # def cb(self, request, response):
    #     response.Image = self.bridge.cv2_to_compressed_imgmsg(self.camera.getFrame())
        
    #     return response
    
    def pcb(self):
        msg = self.bridge.cv2_to_imgmsg(self.camera.getFrame(), 'mono8')
        frame = self.camera.getFrame()
        print(frame)
        print(frame.shape)

        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        
        self.publisher.publish(msg)
        
        
def main():
    rclpy.init()
    
    camera_node = Camera_Node()
    
    rclpy.spin(camera_node)
   
    rclpy.shutdown()

if __name__ == "__main__":
    main()


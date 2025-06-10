import cv2
import numpy

class Camera:
    
    def __init__(self):
        self.cam = cv2.VideoCapture(0, cv2.CAP_V4L2)

        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print("width:: ", self.frame_width)
        print("height:: ", self.frame_height)

    def getFrame(self):
        if self.cam.isOpened() == False:
            raise Exception()

        ret, frame = self.cam.read()
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        if ret == True:
          # return cv2.Mat(numpy.array(frame))
          return frame

        
        #return cv2.Mat(numpy.zeros(shape=(self.frame_height, self.frame_width)))
    
    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()
        

# Open the default camera
#cam = cv2.VideoCapture(0)

# Get the default frame width and height
#frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
#frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

#print("width:: ", frame_width)
#print("height:: ", frame_height)

# Define the codec and create VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (frame_width, frame_height))

# if cam.isOpened() == False:
#     print("Error")

# ret, frame = cam.read()

# #if ret == TRue:
#     #ret, frame = cam.read() 

# # Write the frame to the output file
# if ret == True:
#     print(frame.shape)
#     cv2.imwrite('image.jpeg', frame)

# # Release the capture and writer objects
# cam.release()
# #out.release()
# cv2.destroyAllWindows()

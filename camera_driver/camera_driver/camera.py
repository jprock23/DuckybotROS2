import cv2

class Camera:
    
    def __init__(self):
        self.cam = cam = cv2.VideoCapture(0)

        self.frame_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
    def getFrame(self):
        if cam.isOpened() == False:
            print("Error")

        ret, frame = cam.read()
        if ret == True:
            print(frame.shape)
            cv2.imwrite('image.jpeg', frame)
            
        return frame
    
    def release(self):
        cam.release()
        cv2.destroyAllWindows()
        

# Open the default camera
cam = cv2.VideoCapture(0)

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
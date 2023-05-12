import cv2
import numpy as np
import copy
import json
from simple_pid import PID

# define a video capture object
vid = cv2.VideoCapture(0)
pid = PID(1, 0.1, 0.05, setpoint=1)


def updateBounds():
    f = open("ColorCalibration.calib")
    data = json.load(f)
    
    data = data['colors']
    TrackingData = data[0]
    BlockingData = data[1]
   
    l_T = TrackingData['min'].replace('[','').replace(']','').split(',')
    l_T = [eval(i) for i in l_T]
    
    u_T = TrackingData['max'].replace('[','').replace(']','').split(',')
    u_T = [eval(i) for i in u_T]
    
    l_B = BlockingData['min'].replace('[','').replace(']','').split(',')
    l_B = [eval(i) for i in l_B]
    
    u_B = BlockingData['max'].replace('[','').replace(']','').split(',')
    u_B = [eval(i) for i in u_B]
  
    l_T = np.array(l_T)
    u_T = np.array(u_T)
    l_B = np.array(l_B)
    u_B = np.array(u_B)
    
    print(f"Colors Used\nTrack->{TrackingData['val']}\nBlock->{BlockingData['val']}")
    return l_T, u_T, l_B, u_B
    
def getContours(filteredImage):
    f_image = cv2.medianBlur(copy.deepcopy(filteredImage),5)
    img_gray = cv2.cvtColor(f_image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, 100, 255, 0)
    contours, hierarchy  = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(f_image,contours, -1, (255,0,0), 3)
    
    if contours:
        largestArea = findLargestContour(contours,f_image)
    else:
        imageMiddle = (int(round(f_image.shape[1]/2)),int(round(f_image.shape[2]/2)))
        largestArea = [(0,0),(f_image.shape[1],f_image.shape[0]), imageMiddle]
    return f_image,largestArea
    
def colorFilter(lower_range,upper_range,C_image):
    isoColor = cv2.inRange(C_image,lower_range,upper_range)
    mask = isoColor
    filteredImg = cv2.bitwise_and(C_image,C_image, mask= mask)
    return filteredImg
    
def findLargestContour(contours,image):
    c = max(contours, key = cv2.contourArea)
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
    return [(x,y),(x+w,y+h), (x+int(round(0.5*w)),int(round(y+0.5*h)))]

def drawBoxes(image,box1,box2):
    box_image = copy.deepcopy(image)
    cv2.rectangle(box_image,box1[0],box1[1],(0,0,255),2)
    cv2.rectangle(box_image,box2[0],box2[1],(0,255,0),2)
    return box_image
     
     
     
     
lower_Tracking = np.array([100,87,50])
upper_Tracking = np.array([191,255,255])
lower_Blocking = np.array([35,60,10])
upper_Blocking = np.array([50,255,255])
lower_Tracking, upper_Tracking, lower_Blocking, upper_Blocking = updateBounds()
while True:
    ret1, image = vid.read()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
   
    BlockingFilter = colorFilter(lower_Blocking,upper_Blocking,hsv)
    TrackingFilter = colorFilter(lower_Tracking,upper_Tracking,hsv)  
    
    BlurredCombine = cv2.medianBlur(np.concatenate((TrackingFilter, BlockingFilter), axis=0),5)
    contourImage_Tracking,rect_Tracking = getContours(TrackingFilter)
    contourImage_Blocking,rect_Blocking = getContours(BlockingFilter)
    contourImage = np.concatenate((contourImage_Tracking,contourImage_Blocking),axis = 0)
    boxed_image = drawBoxes(image,rect_Tracking,rect_Blocking)
    
   
    image_Hcenter = (boxed_image.shape[1])/2
    Blocking_error = image_Hcenter - rect_Blocking[2][0] 
    Tracking_error = image_Hcenter - rect_Tracking[2][0]
   
    control = pid(Tracking_error)
    #print(control)
    
    cv2.putText(boxed_image,
                f'{Blocking_error} px',
                (rect_Blocking[2][0]-20,rect_Blocking[2][1]),
                cv2.FONT_HERSHEY_SIMPLEX,0.5, 
                (0,0,0),
                2,
                cv2.LINE_4)
    cv2.putText(boxed_image,
                f'{Tracking_error} px',
                (rect_Tracking[2][0]-20,rect_Tracking[2][1]),
                cv2.FONT_HERSHEY_SIMPLEX,0.5, 
                (0,0,0),
                2,
                cv2.LINE_4)
    
    #cv2.imshow("Original",np.concatenate((image, image), axis=0))
    #cv2.imshow("Blur",BlurredCombine)
    cv2.imshow("Contours",contourImage)    
    cv2.imshow("Boxes", boxed_image)  
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()



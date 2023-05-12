import cv2
import numpy as np
import copy
import os
import json

class colorMethod():
    
    def checkBounds(self):
        print(f'Tracking from {self.lower_Tracking} -> {self.upper_Tracking}')
        print(f'Blocking from {self.lower_Blocking} -> {self.upper_Blocking}')
        
        
   
    def updateBounds(self):
        
   
        f = open("ColorCalibration.calib")
    
        if(f.readable()):
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
            
            print(f"Loaded Colors Used\nTrack->{TrackingData['val']}\nBlock->{BlockingData['val']}\n")
        else:
            l_T = np.array([100,87,50])
            u_T = np.array([191,255,255])
            l_B= np.array([35,60,10])
            u_B = np.array([50,255,255])
            print("Defaults Used")
        return l_T, u_T, l_B, u_B
     
    def getContours(self,filteredImage):
        f_image = cv2.medianBlur(copy.deepcopy(filteredImage),5)
        img_gray = cv2.cvtColor(f_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 100, 255, 0)
        contours, hierarchy  = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(f_image,contours, -1, (255,0,0), 3)
        
        if contours:
            largestArea = self.findLargestContour(contours,f_image)
        else:
            largestArea = None
        
        return f_image,largestArea
        
    def colorFilter(self,lower_range,upper_range,C_image):
        isoColor = cv2.inRange(C_image,lower_range,upper_range)
        mask = isoColor
        filteredImg = cv2.bitwise_and(C_image,C_image, mask= mask)
        return filteredImg
        
    def findLargestContour(self,contours,image):
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
       
        if (cv2.contourArea(c) > 500):
            return [(x,y),(x+w,y+h), (x+int(round(0.5*w)),int(round(y+0.5*h)))]
        else:
            return None

    def drawBoxes(self,image,box1,box2):
        box_image = copy.deepcopy(image)
        if (box1 is not None):
            cv2.rectangle(box_image,box1[0],box1[1],(0,0,255),2)
        if (box2 is not None):
            cv2.rectangle(box_image,box2[0],box2[1],(0,255,0),2)
        return box_image
                 
    def colorTracking(self,image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
       
        BlockingFilter = self.colorFilter(self.lower_Blocking,self.upper_Blocking,hsv)
        TrackingFilter = self.colorFilter(self.lower_Tracking,self.upper_Tracking,hsv)  
        
        contourImage_Tracking,rect_Tracking = self.getContours(TrackingFilter)
        contourImage_Blocking,rect_Blocking = self.getContours(BlockingFilter)
        
        boxed_image = self.drawBoxes(image,rect_Tracking,rect_Blocking)
        
        
        image_Hcenter = (boxed_image.shape[1])/2
        if(rect_Blocking is not None):
            Blocking_error = image_Hcenter - rect_Blocking[2][0] 
        else:
            Blocking_error = None
        if(rect_Tracking is not None):
            Tracking_error = image_Hcenter - rect_Tracking[2][0]
        else:
            Tracking_error = None
       
        if(rect_Blocking is not None):        
            cv2.putText(boxed_image,
                    f'{Blocking_error} px',
                    (rect_Blocking[2][0]-20,rect_Blocking[2][1]),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5, 
                    (0,0,0),
                    2,
                    cv2.LINE_4)
        if(rect_Tracking is not None):
            cv2.putText(boxed_image,
                    f'{Tracking_error} px',
                    (rect_Tracking[2][0]-20,rect_Tracking[2][1]),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5, 
                    (0,0,0),
                    2,
                    cv2.LINE_4)
        
        return boxed_image,Blocking_error,Tracking_error
    
    def __init__(self):
        self.lower_Tracking, self.upper_Tracking, self.lower_Blocking, self.upper_Blocking = self.updateBounds()
     
    



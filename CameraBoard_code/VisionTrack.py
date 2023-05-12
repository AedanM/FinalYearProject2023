import cv2
import numpy as np
import copy

import json
imHalfSize = 112

class visionMethod():
    backSub = None
    vi2d = cv2.VideoCapture(0)
    vi2d.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
    ret1, background = vi2d.read()
    
    vi2d.release()
   
   
    def SetBackground(self, bb):
        background = bb.copy()
    def removeBackground(self,image):
        bg_image = (self.background).copy()
        frame = (image).copy()
        
        # Convert the background image to grayscale
        bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
        
        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Compute the absolute difference between the background and the frame
        diff = cv2.absdiff(bg_gray, frame_gray)
        
        # Apply a threshold to the difference image
        threshold = 20
        ret, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # Apply the mask to the frame to remove the background
        fg = cv2.bitwise_and(frame, frame, mask=mask)
        # Invert the mask
        mask_inv = cv2.bitwise_not(mask)

        # Create a white image with the same dimensions as the original imag
        white = 255 * np.ones_like(frame)

        # Apply the inverted mask to the white image to turn all non-black pixels white
        result = cv2.bitwise_or(frame, white, mask=mask_inv)  
        
        return result
    def removeBackground(self,image,bckGrd):
        bg_image = (bckGrd).copy()
        frame = (image).copy()
        
        # Convert the background image to grayscale
        bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
        
        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Compute the absolute difference between the background and the frame
        diff = cv2.absdiff(bg_gray, frame_gray)
        
        # Apply a threshold to the difference image
        threshold = 20
        ret, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # Apply the mask to the frame to remove the background
        fg = cv2.bitwise_and(frame, frame, mask=mask)
        # Invert the mask
        mask_inv = cv2.bitwise_not(mask)

        # Create a white image with the same dimensions as the original imag
        white = 255 * np.ones_like(frame)

        # Apply the inverted mask to the white image to turn all non-black pixels white
        result = cv2.bitwise_or(frame, white, mask=mask_inv)  
        
        return result
    def getContours(self,filteredImage,baseImage):
            f_image = (filteredImage).copy()
            colorImage = baseImage.copy()
            f_image = cv2.medianBlur(f_image,7)
            edged = cv2.Canny(f_image, 200, 400)
           
            contours, hierarchy  = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            
            if contours:
                try:
                    max_area = 0
                    areas = []
                    largest_contour = None
                    for contour in contours:
                        area = cv2.contourArea(contour)
                        areas.append(area)
                        if area > max_area:
                            max_area = area
                            largest_contour = contour
                      
                    M = cv2.moments(largest_contour)
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])
                    cv2.drawContours(colorImage,largest_contour, -1, (0,255,0), 3)
                   
                    cv2.circle(colorImage, (cx, cy), 3, (255, 0, 255), -1)
                    largestCenter = [cx,cy]
                except:
                    largestCenter = (int(baseImage.shape[1]/2),int(baseImage.shape[0]/2))
            else:
                largestCenter = (int(baseImage.shape[1]/2),int(baseImage.shape[0]/2))
            
            return largestCenter,colorImage
                   
    def cropZoom(self, image,rectImage,center):
        cx = center[0]
        cy = center[1]
        
        rectMaxX = int(min(rectImage.shape[1],cx+imHalfSize))
        rectMaxY = int(min(rectImage.shape[0],cy+imHalfSize))
        rectMinX = int(max(1,cx-imHalfSize))
        rectMinY = int(max(0,cy-imHalfSize))
       
        
        cv2.rectangle(rectImage,(rectMaxX,rectMaxY),(rectMinX,rectMinY),(128,0,0),2)
       
        cropped_image = image[rectMinY:rectMaxY,rectMinX:rectMaxX]
       
        return cropped_image,rectImage
        

    def VisionTrack(self,V_image):
        iso = self.removeBackground(V_image.copy())
        largestCenter,colorVersion = self.getContours(iso,V_image.copy())
        crop,colorVersion = self.cropZoom(V_image.copy(),colorVersion,largestCenter)
        
        error = (largestCenter[0] - V_image.shape[1]/2)/V_image.shape[1]
        return colorVersion,crop, error, largestCenter[0]
        
    def VisionTrack(self,V_image,B_image):
        iso = self.removeBackground(V_image.copy(),B_image.copy())
        largestCenter,colorVersion = self.getContours(iso,V_image.copy())
        crop,colorVersion = self.cropZoom(V_image.copy(),colorVersion,largestCenter)
        
        error = (largestCenter[0] - V_image.shape[1]/2)/V_image.shape[1]
        return colorVersion,crop, error, largestCenter[0]   
        
    



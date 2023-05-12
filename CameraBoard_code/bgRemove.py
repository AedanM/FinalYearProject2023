import cv2
import numpy as np
import time 

background = None# cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Source_Pics\Background_Subtraction_Tutorial_background.jpg")
camera = None#cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Source_Pics\Background_Subtraction_Tutorial_frame.jpg")
video = cv2.VideoCapture(1)
imHalfSize = 112
def getBackground():
    rect, background = video.read()
def removeBackground():
        bg_image = (background).copy()
        frame = (camera).copy()
        
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
        cv2.imwrite('OpenCVDocs.jpg',result)
        return result
def removeBackground(in_frame):
        bg_image = (background).copy()
        iframe = (in_frame).copy()
        
        # Convert the background image to grayscale
        bg_gray = cv2.cvtColor(bg_image, cv2.COLOR_BGR2GRAY)
        
        # Convert the frame to grayscale
        frame_gray = cv2.cvtColor(iframe, cv2.COLOR_BGR2GRAY)
        
        # Compute the absolute difference between the background and the frame
        diff = cv2.absdiff(bg_gray, frame_gray)
        
        # Apply a threshold to the difference image
        threshold = 20
        ret, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
        
        # Apply the mask to the frame to remove the background
        fg = cv2.bitwise_and(in_frame, in_frame, mask=mask)
        # Invert the mask
        mask_inv = cv2.bitwise_not(mask)

        # Create a white image with the same dimensions as the original imag
        white = 255 * np.ones_like(in_frame)

        # Apply the inverted mask to the white image to turn all non-black pixels white
        result = cv2.bitwise_or(in_frame, white, mask=mask_inv)  
        cv2.imwrite('OpenCVDocs.jpg',result)
        return result
def getContours(filteredImage,ColorImage):
        f_image = (filteredImage).copy()
        colorImage = ColorImage.copy()
        f_image = cv2.medianBlur(f_image,7)
        edged = cv2.Canny(f_image, 200, 400)
       
        contours, hierarchy  = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        if contours:
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
            
        else:
            largestCenter = None
        
        return largestCenter,colorImage
               
def cropZoom(image,rectImage,center):
    cx = center[0]
    cy = center[1]
    
    rectMaxX = int(min(rectImage.shape[1],cx+imHalfSize))
    rectMaxY = int(min(rectImage.shape[0],cy+imHalfSize))
    rectMinX = int(max(1,cx-imHalfSize))
    rectMinY = int(max(0,cy-imHalfSize))
    #print(f'[{rectMinX},{rectMinY}] \n [{rectMaxX},{rectMaxY}]')
    
    cv2.rectangle(rectImage,(rectMaxX,rectMaxY),(rectMinX,rectMinY),(128,0,0),2)
   
    cropped_image = image[rectMinY:rectMaxY,rectMinX:rectMaxX]
   
    return cropped_image,rectImage
    


#cv2.imshow('Painted Image',colorVersion)
#cv2.imshow('Cropped Image',crop)
#cv2.imwrite('LegoScenePainted.jpg', colorVersion)
#cv2.imwrite('LegoSceneCrop.jpg',crop)
while True:
    num_frames = 120;
 
    print("Capturing {0} frames".format(num_frames))
 
    # Start time
    start = time.time()
    rect, background = video.read()
    # Grab a few frames
    for i in range(0, num_frames) :
        ret, framea = video.read()
        iso = removeBackground(framea)
        largestCenter,colorVersion = getContours(iso,framea)
        crop,colorVersion = cropZoom(framea,colorVersion,largestCenter)
    # End time
    end = time.time()
    
    # Time elapsed
    seconds = end - start
    print ("Time taken : {0} seconds".format(seconds))
 
    # Calculate frames per second
    fps  = num_frames / seconds
    print("Estimated frames per second : {0}".format(fps))
 
    # Release video
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
video.release()     
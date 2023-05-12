imHalfSize = 112
import numpy as np
import time
import cv2

def findObject(maskedFrame):
    maskedFrame = cv2.cvtColor(maskedFrame, cv2.COLOR_BGR2GRAY)
    contours,hierarchy = cv2.findContours(maskedFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the index of the largest contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    cnt=contours[max_index]
    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return (cx,cy)
    
def cropZoom(center,frame):
    cx = center[1]
    cy = center[0]
    rectMaxX = min(frame.shape[1],cx+imHalfSize)
    rectMaxY = min(frame.shape[0],cy+imHalfSize)
    rectMinX = max(1,cx-imHalfSize)
    rectMinY = max(0,cy-imHalfSize)
   
    cropped_image = frame[rectMinX:rectMaxX,rectMinY:rectMaxY]
    boxSize = (f'[{rectMinX},{rectMinY}] \n [{rectMaxX},{rectMaxY}]')
   
    cv2.putText(cropped_image,
                    boxSize,
                    center,
                    cv2.FONT_HERSHEY_SIMPLEX,0.5, 
                    (0,0,0),
                    2,
                    cv2.LINE_4)
    cv2.rectangle(frame,(rectMaxY,rectMaxX),(rectMinY,rectMinX),(128,0,0),2)
    return cropped_image



vid = cv2.VideoCapture(0)
ret1, background = vid.read()


while(True):
        ret,frame = vid.read()
        masked = cv2.inRange(frame,np.array([0,0,0]),np.array([200,200,200]))
        center = findObject(masked)
        zoomed = cropZoom(center,masked)
        
        cv2.imshow('frame',frame)
        cv2.imshow('zoomed',zoomed)
        if cv2.waitKey(1) & 0xFF == ord('q'):
           break
        
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

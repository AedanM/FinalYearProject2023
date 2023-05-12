import cv2
import time
import numpy as np
from VisionTrack import visionMethod
video = cv2.VideoCapture("jag.mp4")
background_img = cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\jag.jpg")

VT = visionMethod()
startTime = time.time()
imgArray = []
zoomArray = []
centers = []
try:
    
    while True:
        ret1, img = video.read()

        box,crop, error, center = VT.VisionTrack(img,background_img)
        centers.append([round(time.time()-startTime,2),round(error,4)])
        height, width, layers = img.shape
        size = (width,height)
        cv2.imshow("Crop",crop)
        cv2.imshow("Box",box)
        imgArray.append(box)
       
        if(error):
            zoomArray.append(crop)
            print(f"Error is {centers[len(centers)-1]}")
        #'''
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except:
    # After the loop release the cap object
    video.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

for i in range(len(imgArray)):
    out.write(imgArray[i])
out.release()
out = cv2.VideoWriter('Zoomproject.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, (224,224))

for i in range(len(zoomArray)):
    out.write(zoomArray[i])
out.release()    
#print(centers)
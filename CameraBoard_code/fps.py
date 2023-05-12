import cv2
import time
import numpy as np
video = cv2.VideoCapture("jag.mp4")
background = cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\jag.jpg")

def removeBackground(image, back):
    bg_image = (back).copy()
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
    #mask = backSub.apply(frame)
    mask_inv = cv2.bitwise_not(mask)
    
    # Create a white image with the same dimensions as the original imag
    white = 255 * np.ones_like(frame)
    
   
    # Apply the inverted mask to the white image to turn all non-black pixels white
    result = cv2.bitwise_or(frame, white, mask=mask_inv)  
    
    return result
    

num_frames = 1080;
 
print("Capturing {0} frames".format(num_frames))

# Start time
start = time.time()

# Grab a few frames
for i in range(0, num_frames):
    ret, framea = video.read()
    if(framea is None or background is None):
        print("AGGG")
    iso = removeBackground(framea,background)
# End time
end = time.time()

# Time elapsed
seconds = end - start
print ("Time taken : {0} seconds".format(seconds))

# Calculate frames per second
fps  = num_frames / seconds
print("Estimated frames per second : {0}".format(fps))
import numpy as np
import cv2
import json

lower_sat = np.array([0,0,0])
upper_sat = np.array([255,255,255])
vid = cv2.VideoCapture(0)
title_window = "Main Window"
slider_max = 255


def colorFilter(lower_range,upper_range,C_image):
    isoColor = cv2.inRange(C_image,lower_range,upper_range)
    mask = isoColor
    filteredImg = cv2.bitwise_and(C_image,C_image, mask= mask)
    return filteredImg

def getColor(img):
    key = [0,0,0]
    max = [0,0,0]
    min = [255,255,255]
    count = 0
    for i in range(w):
        for j in range(h):
            if img[i, j].all() != 0:
                key[0] = key[0] + img[i,j][0]
                key[1] = key[1] + img[i,j][1]
                key[2] = key[2] + img[i,j][2]
                if(img[i,j][0] > max[0]):
                    max[0] = img[i,j][0]
                if(img[i,j][1] > max[1]):
                    max[1] = img[i,j][1]
                if(img[i,j][2] > max[2]):
                    max[2] = img[i,j][2]
                if(img[i,j][0] < min[0]):
                    min[0] = img[i,j][0]
                if(img[i,j][1] < min[1]):
                    min[1] = img[i,j][1]
                if(img[i,j][2] < min[2]):
                    min[2] = img[i,j][2]
                count = count + 1
    key[:] = [round(x / count,0) for x in key]
    return key,min,max

def on_H_min_trackbar(val):
    lower_sat[0] = val
def on_S_min_trackbar(val):
    lower_sat[1] = val
def on_V_min_trackbar(val):
    lower_sat[2] = val
def on_H_max_trackbar(val):
    upper_sat[0] = val
def on_S_max_trackbar(val):
    upper_sat[1] = val
def on_V_max_trackbar(val):
    upper_sat[2] = val

def makeColorFile(Color1_key,Color1_min,Color1_max,Color2_key,Color2_min,Color2_max):
    f = open("ColorCalibration.calib", "w")
 
    ColorData = {
        'colors' : [
        {
            'name' : 'Tracking Color',
            'val' : str(Color1_key),
            'min' : str(Color1_min),
            'max' : str(Color1_max)
        },
        {
            'name' : 'Blocking Color',
            'val' : str(Color2_key),
            'min' : str(Color2_min),
            'max' : str(Color2_max)
        }
    ]
    }
   
    json_string = json.dumps(ColorData)
    
    f.write(json_string)

    
    

 
cv2.namedWindow("Main Window")
cv2.createTrackbar("Hue Min", title_window , 0, slider_max, on_H_min_trackbar)
cv2.createTrackbar("Hue Max", title_window , 255, slider_max, on_H_max_trackbar)
cv2.createTrackbar("Sat. Min", title_window , 0, slider_max, on_S_min_trackbar)
cv2.createTrackbar("Sat. Max", title_window , 255, slider_max, on_S_max_trackbar)
cv2.createTrackbar("Value Min", title_window , 0, slider_max, on_V_min_trackbar)
cv2.createTrackbar("Value Max", title_window , 255, slider_max, on_V_max_trackbar)
C1_key=C1_min=C1_max=C2_key=C2_min=C2_max = 0
while True:
    
    ret1, image = vid.read()
    filteredImg = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    filteredImg = colorFilter(lower_sat,upper_sat,filteredImg)
    cv2.imshow(title_window, filteredImg)
   
    w=filteredImg.shape[0]
    h=filteredImg.shape[1]

    if cv2.waitKey(1) & 0xFF == ord('1'):
        C1_key,C1_min,C1_max = getColor(filteredImg)
        print(f'Color 1 Set:\nAverage:{C1_key}\nMin:{C1_min}\nMax{C1_max}\n')
   
    if cv2.waitKey(1) & 0xFF == ord('2'):
        C2_key,C2_min,C2_max = getColor(filteredImg)
        print(f'Color 2 Set:\nAverage:{C2_key}\nMin:{C2_min}\nMax{C2_max}\n')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        makeColorFile(C1_key,C1_min,C1_max,C2_key,C2_min,C2_max)
        break
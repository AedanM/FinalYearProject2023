import numpy as np
import cv2
import os
TF_Sqaure_size = 244
leopardLibrary = r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Leopard_Pics"
peopleLibrary = r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\People_Pics"
fog1 = cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Source_Pics\fog1.jpg")
fog2 = cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Source_Pics\fog2.jpg")
rain1 = cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Source_Pics\Rain1.jpg")
rain2 = cv2.imread(r"C:\Users\aedan\OneDrive - The University of Nottingham\4th Year\Project\Source_Pics\Rain2.jpg")
overlays = [fog1, fog2,rain1,rain2]
overlaytags = ["_fog1","_fog2","_rain1","_rain2"]


def cropToMiddle(image):
    longestSide = image.shape[0]
    if(image.shape[1] > longestSide):
        longestSide = image.shape[1]
    scale_percent = TF_Sqaure_size/longestSide # percent of original size
    
    width = int(round(image.shape[1] * scale_percent ,0))
    height = int(round(image.shape[0] * scale_percent ,0))
    dim = (width, height)
  
    # resize image
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    horzPadding = TF_Sqaure_size-width
    left = int(round(horzPadding/2,0))
    right = horzPadding-left
    vertPadding = TF_Sqaure_size-height
    top = int(round(vertPadding/2,0))
    bottom = vertPadding-top
    padded = cv2.copyMakeBorder(resized, top, bottom, left, right, cv2.BORDER_REPLICATE)
        
    return padded 
def BlurImage(imageToBlur, inputName):
    blur = cv2.GaussianBlur(imageToBlur,(5,5),0)
    name = inputName +"_Blurred"
    return blur,name

def GrayImage(imageToGray, inputName):
    gray = cv2.cvtColor(imageToGray, cv2.COLOR_BGR2GRAY)
    name = inputName +"_Mono"
    return gray,name

def OverlayImage(BaseImage, inputName,OverlayImg,outputTag):

    overlayImg = cv2.resize(OverlayImg, (BaseImage.shape[1],BaseImage.shape[0]), interpolation = cv2.INTER_AREA)
    overlayImg = cv2.cvtColor(overlayImg, cv2.COLOR_BGR2GRAY)
    overlayImg = cv2.cvtColor(overlayImg, cv2.COLOR_GRAY2BGR)
    
    comb = cv2.addWeighted(BaseImage,0.6,overlayImg,0.4,0)
    name = inputName +"_"+outputTag
    return comb,name    
    
    
# folder path
dir_path = input("Leopards or People? ")
if 'L' in dir_path or 'l' in dir_path:
    dir_path = leopardLibrary
    target = "Leopard"
elif 'p' in dir_path or "P" in dir_path:
    dir_path = peopleLibrary
    target = "Person"
count = 0
# Iterate directory
for path in os.listdir(dir_path):
    # check if current path is a file
    if os.path.isfile(os.path.join(dir_path, path)):
        count += 1
print('File count:', count)


for i in range(0,count):
    imgList = []
    imgNameList = []
    fileName = f"{dir_path}\{target} ({i+1}).jpg"
    if(os.path.isfile(fileName)):
        print()
        print(f"Image {i} found")
        img = cv2.imread(fileName)
        assert img is not None, f"file {fileName} could not be read, check with os.path.exists()"
        os.chdir(dir_path+"\Edits")
        newName = f"Edited{target}_{i}"
        print(f"before {img.shape}")
        img = cropToMiddle(img)
        print(f"after {img.shape}")
    
        imgList.append(img)
        imgNameList.append(newName)
        cv2.imwrite(newName+".jpg", img)
        
        blurImg, blurName = BlurImage(img, newName)
        imgList.append(blurImg)
        imgNameList.append(blurName)
        cv2.imwrite(blurName+".jpg",blurImg)
        
       
        
        for j in range(0,len(imgList)):
            for k in range(0,1):  
               
                overlayImg, overlay_Name = OverlayImage(imgList[j],imgNameList[j], overlays[k], overlaytags[k])
                imgList.append(overlayImg)
                imgNameList.append(overlay_Name)
                cv2.imwrite(overlay_Name+".jpg", overlayImg)
        for j in range(0,len(imgList)):
            for k in range(2,3):  
                overlayImg, overlay_Name = OverlayImage(imgList[j],imgNameList[j], overlays[k], overlaytags[k])
                imgList.append(overlayImg)
                imgNameList.append(overlay_Name)
                cv2.imwrite(overlay_Name+".jpg", overlayImg)
            
        for j in range(0,len(imgList)):
            grayImg, grayName = GrayImage(imgList[j],imgNameList[j])
            imgList.append(grayImg)
            imgNameList.append(grayName)
            cv2.imwrite(grayName+".jpg", grayImg)
        print(f"Image {i} saved")
    else:
        print(f"Couldn't Find {fileName}")
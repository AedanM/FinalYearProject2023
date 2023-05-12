import cv2
from colorTrack import colorMethod
from VisionTrack import visionMethod
from simple_pid import PID
import time
#import RPi.GPIO as GPIO
#import time

#servoPIN = 12
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(servoPIN, GPIO.OUT)

#p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
#p.start(2.5) # Initialization
control = 0
# define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_AUTOFOCUS, 0) 
CT = colorMethod()
VT = visionMethod()
pid = PID(1, 0.1, 0.05, setpoint=1)
imHalfSize = 112


inputChoice = input("Color or Vision?")
if('c' in inputChoice):

    try:
        CT.checkBounds()
        while True:
            ret1, img = vid.read()
            
            boxed, BlockingErr, TrackingErr=  CT.colorTracking(img)
           
            if(TrackingErr is None and BlockingErr is None):
                display_message = ("All Quiet")
            elif(TrackingErr is None):
                display_message = "Human"
            else:
                display_message = "Predator!"
                if (TrackingErr > 5):
               
                    control = pid(TrackingErr)
               # p.ChangeDutyCycle(control)
            (w, h), _ = cv2.getTextSize(display_message, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
            cv2.rectangle(boxed,(0,0),(20+w,40),(0,0,0),-1)
            cv2.putText(boxed,
                    display_message,
                    (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX,1, 
                    (255,255,255),
                    2,
                    cv2.LINE_4)
            cv2.imshow("Boxes", boxed) 
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
       # p.stop()
        #GPIO.cleanup()
        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
else:
    centers = []
    try:
        
        while True:
            ret1, img = vid.read()
            box,crop, error, center = VT.VisionTrack(img)
            centers.append([time.time(), center,error])
            
            cv2.imshow("Crop",crop)
            cv2.imshow("Box",box)
            if(error):
                print(f"Error is {error}")
            #'''
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
    print(centers)
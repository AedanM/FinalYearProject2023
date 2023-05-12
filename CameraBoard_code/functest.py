from MessageFlag import MessageFlags
from pyLoraRFM9x import LoRa, ModemConfig
import time
from simple_pid import PID
from gpiozero import Servo


import cv2
#from tflite_support.task import core
#from tflite_support.task import processor
#from tflite_support.task import vision


pid = PID(1, 0.1, 0.05, setpoint=1)
ModuleIDs = [2,3]
Flags = MessageFlags(0,0,0,0,0,0)
BOARD.setup()
lora = LoRa(1, 5, 2, reset_pin = 25, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
CameraBool = False
StaggerLoad = []
IMG_Center = 320
TimeOut_Length = 300
StartTime = time.time()

def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    if(Flags.ObjectDetectedDef in payload.message):
        CameraBool = True
        StartTime = time.time()
        StaggerLoad.clear()
    elif(Flags.NoObjectDef in payload.message):
        StaggerLoad.append(payload.message)
        if(len(StaggerLoad)>3):
            CameraBool = False
        


#lora.on_recv = on_recv


def sendMessage(message):
    for Module in ModuleIDs:
        status = lora.send_to_wait(str(message), Module, retries=2)
        if status is True:
            print("Message sent!")
        else:
            print("No acknowledgment from recipient " + str(Module))

def TrackCenter(cTuple):
    adjustTime = time.time_ns() + 250
    while (time.time_ns() < adjustTime):
        control = pid(IMG_Center - cTuple[0])
        servo.value = control

def classifyImage(image):
    PredBool = False    
    PersBool = False
    center = (0,0)
    #feed into TF model
    '''
     # Initialize the image classification model
    base_options = core.BaseOptions(file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)

      # Enable Coral by this setting
    classification_options = processor.ClassificationOptions(max_results=max_results, score_threshold=score_threshold)
    options = vision.ImageClassifierOptions(base_options=base_options, classification_options=classification_options)

    classifier = vision.ImageClassifier.create_from_options(options)
    
    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Create TensorImage from the RGB image
    tensor_image = vision.TensorImage.create_from_array(rgb_image)
    # List classification results
    Tsgs = classifier.classify(tensor_image)'''
    
    
    Tags = 'leopard'
    PredBool = 'leopard' in Tags
    PersBool = 'human' in Tags
    M = cv2.moments(i)
    cx =   (M10 / M00)
    cy =  (M01 / M00)
    center = (cx,cy)
    return  PredBool, PersBool, center

def RunMain():
    img = cv2.imread()
    Predator_Bool, Person_Bool, centerTuple = classifyImage(img)
    if(Predator_Bool):
        sendMessage(Flags.PredatorDef)
        TrackCenter(centerTuple)
    elif(Person_Bool):
        sendMessage(Flags.HumanDef)
    else:
        sendMessage(Flags.NoObjectDef)
        


while True:
    if(CameraBool):
        RunMain()
    else:
        time.sleep(1)
        print('Zzzzzz')
    if(time.time() > (StartTime + TimeOut_Length)):
        CameraBool = False

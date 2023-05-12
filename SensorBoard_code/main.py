import machine
from micropython import const
from HCSR04 import HCSR04
from MessageFlag import MessageFlags
from ulora import LoRa, ModemConfig, SPIConfig
import time
import random
Flags = MessageFlags(0,0,0,0,0,0)
Range_Sensitivity = 40
LightsState = False
DeterrentState = False
LED_Pin = machine.Pin(2, machine.Pin.OUT)
Deter_Pin = machine.Pin(3, machine.Pin.OUT)
Range_Finder = HCSR04(trigger_pin=13, echo_pin=12,echo_timeout_us=1000000)


def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    Flags.setFlags(receivedMessage)

# Lora Parameters
RFM95_RST = 27
RFM95_SPIBUS = SPIConfig.rp2_0
RFM95_CS = 5
RFM95_INT = 28
RF95_FREQ = 868.0
RF95_POW = 20
CLIENT_ADDRESS = 1
SERVER_ADDRESS = 2

# initialise radio
#lora = LoRa(RFM95_SPIBUS, RFM95_INT, SERVER_ADDRESS, RFM95_CS, 
#            reset_pin=RFM95_RST, freq=RF95_FREQ, tx_power=RF95_POW, acks=True)

#lora.on_recv = on_recv
#lora.set_mode_rx()


def transmitMessage(message):
    print(f"Message sent ({message})")
 #   lora.send_to_wait(str(message), SERVER_ADDRESS)
    
   
def activateDeterrents():
    global DeterrentState
    if(not DeterrentState):
        print("Deter on")
        DeterrentState = True
        Deter_Pin.on()
    
def deactivateDeterrents():
    global DeterrentState
    if(DeterrentState):
        print("Deter off")
        DeterrentState = False
        Deter_Pin.off()
    
def activateFloodLights():
    global LightsState
    if(not LightsState):
        print("Lights on")
        LightsState = True
        LED_Pin.on()
    
def deactivateFloodLights():
    global LightsState
    if(LightsState):
        print("Killed Lights")
        LightsState = False
        LED_Pin.off()
    
def scanRange():
    distance = Range_Finder.distance_cm()
    print("Range: "  + str(distance))
    if(distance < Range_Sensitivity):
        Flags.setFlags(Flags.ObjectDetectedDef)
        print("We got One!!")
    else:
        Flags.setFlags(Flags.NoObjectDef)
        print("All Quiet")
    
    if(Flags.ObjectDetectedFlag):
        transmitMessage(Flags.ObjectDetectedDef)
    elif(Flags.NoObjectFlag):
        transmitMessage(Flags.NoObjectDef)

def runFunctions():
    if(Flags.NoObjectFlag):
        deactivateFloodLights()
        deactivateDeterrents()
    if(Flags.ObjectDetectedFlag):
        activateFloodLights()
    if(Flags.HumanFlag):
        deactivateDeterrents()
    if(Flags.PredatorFlag):
        activateDeterrents()
        
     

while True:
    time.sleep(3)
    print("----------------")
    scanRange()
    runFunctions()
    Flags.flagCheck()
    print(f'Lights - {LightsState}   Deterrents - {DeterrentState}')
    print("----------------")
    print('')

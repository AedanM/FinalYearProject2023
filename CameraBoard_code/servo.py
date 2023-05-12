import RPi.GPIO as GPIO
import time

servoPIN = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
duty = 0
flip = True
try:
  while True:
    p.ChangeDutyCycle(duty)
    if(flip) :
        duty += 0.1
    else:
        duty -= 0.1
    if (duty == 15 or duty == 0):
        flip = not flip
    time.sleep(0.1)
except KeyboardInterrupt:
  p.stop()
  GPIO.cleanup()
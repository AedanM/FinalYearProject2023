import pigpio
from simple_pid import PID
pid = PID(10, 0.1, 0.05, setpoint=0)
ServoPin = 21
pi = pigpio.pi()
pi.gpioServo(ServoPin,1500)
frame_size = 480
frame_center = 240

def getServoSpeed():
    val = pi.get_PWM_frequency(ServoPin)
    speed_percent = abs((val-1500)/5)
    dir = 'clockwise'
    if val < 1500:
        dir = 'counterclockwise'
    print(f'Servo is going {speed_percent}% {dir}')

def trackCenter(center):
    error = (center-frame_center)/frame_size
    print(f"Err % is {error}")
    control = pid(error)
    print(control)
    

centers = [0,120,240,360,480]

for i in centers:
    print(f"Target is at {i}")
    trackCenter(i)  
    getServoSpeed()
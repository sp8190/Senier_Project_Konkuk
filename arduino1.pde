# servo_keyboard.py
import RPi.GPIO as GPIO
import time

pin = 18    # PWM pin

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
p = GPIO.PWM(pin, 50)
p.start(0)

try:
    while True:
        key = raw_input("Enter L(left), C(center), R(right) : ")
        if key.upper() == 'L' :
            print("Left : 12.5")
            p.ChangeDutyCycle(12.5)
            time.sleep(0.5)
        if key.upper() == 'C' :
            print("Center : 7.5")
            p.ChangeDutyCycle(7.5)
            time.sleep(0.5)
        if key.upper() == 'R' :
            print("Right : 2.5")
            p.ChangeDutyCycle(2.5)
            time.sleep(0.5)
except KeyboardInterrupt:
    p.stop()
    
GPIO.cleanup()

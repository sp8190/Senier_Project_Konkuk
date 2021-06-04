# -*- coding:utf-8 -*- #한글입력
 
import RPi.GPIO as GPIO
import time
 
pin=18
 
GPIO.setmode(GPIO.BCM)          #gpio 모드 세팅
GPIO.setup(pin,GPIO.OUT)        #모터출력
p=GPIO.PWM(pin,50)              #펄스폭변조 세팅 핀,주파수
p.start(0)
try:
        while True:
                p.ChangeDutyCycle(2.5)  #0도
                print "0도"
                time.sleep(0.5)
                p.ChangeDutyCycle(6)    #90도
                print "90도"
                time.sleep(0.5)
                p.ChangeDutyCycle(9.5)  #180도
                print "180도"
                time.sleep(0.5)
except KeyboardInterrupt:               #ctrl+c 종료
        p.stop()
finally:
        GPIO.cleanup()          #필수! 정삭적인 종료를 위해 필요
 
 

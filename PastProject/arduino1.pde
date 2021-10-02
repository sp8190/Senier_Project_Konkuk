# -*- coding:utf-8 -*- #한글입력
 
import RPi.GPIO as GPIO
import time
 
pin=18
 
GPIO.setmode(GPIO.BCM)                          #gpio 모드 셋팅
GPIO.setup(pin,GPIO.OUT)                        #모터동작
GPIO.setup(12,GPIO.IN,pull_up_down=GPIO.PUD_UP) #버튼 입력
p=GPIO.PWM(pin,50)                              #펄스폭 변조 핀,주파수
p.start(0)
try:
        a=True                                  #초기화
        while True:
                button_state=GPIO.input(12)
                if button_state==False:
                        a=False if a else True
                        print "반대로이동"
                if a:
                        p.ChangeDutyCycle(9.5)
                else:
                        p.ChangeDutyCycle(2.5)
                time.sleep(0.15)
except KeyboardInterrupt:
        p.stop()
finally:
        GPIO.cleanup()
 

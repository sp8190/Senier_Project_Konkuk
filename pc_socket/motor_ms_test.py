# -*- coding: utf-8 -*-

# 라즈베리파이 GPIO 패키지
import os
import pigpio
import pyautogui
import pynput.mouse    as ms
import pynput.keyboard as kb
import RPi.GPIO as GPIO
import time
import threading
from multiprocessing import Process
import socket

os.system("sudo pigpiod") # pigpio on
os.system("raspivid -n -t 0 -h 720 -w 1280 -fps 25 -b 2000000 -o - |gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=192.168.137.219 port=5000")
time.sleep(1)
pi = pigpio.pi() # Connect to local Pi.

# 모터 상태
STOP  = 0
FORWARD  = 1
BACKWORD = 2
LEFT = 3
RIGHT = 4

# 모터 채널
CH1 = 0
CH2 = 1

# PIN 입출력 설정
OUTPUT = 1
INPUT = 0

# PIN 설정
HIGH = 1
LOW = 0

# 실제 핀 정의
#PWM PIN
ENA = 26  #37 pin
ENB = 0   #27 pin

#GPIO PIN
IN1 = 19  #37 pin
IN2 = 13  #35 pin
IN3 = 5   #31 pin
IN4 = 6   #29 pin

# 핀 설정 함수
def setPinConfig(EN, INA, INB):
    GPIO.setmode(GPIO.BCM)
    # Yellow : Pin 18 : 24(Trig)
    GPIO.setup(24, GPIO.OUT)
    # White : Pin 16 : 23(Echo)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    # 100khz 로 PWM 동작 시킴 
    pwm = GPIO.PWM(EN, 100) 
    # 우선 PWM 멈춤.   
    pwm.start(0) 
    return pwm

# 모터 제어 함수
def setMotorContorl(pwm, INA, INB, speed, stat):

    #모터 속도 제어 PWM
    pwm.ChangeDutyCycle(speed)  
    
    #앞으로
    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)
        
    #뒤로
    elif stat == BACKWORD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)

    #왼쪽으로
    elif stat == LEFT:
        if pwm == pwmA:
            GPIO.output(INA, LOW)
            GPIO.output(INB, HIGH)
        else:
            GPIO.output(INA, HIGH)
            GPIO.output(INB, LOW)

    #오른쪽으로
    elif stat == RIGHT:
        if pwm == pwmA:
            GPIO.output(INA, HIGH)
            GPIO.output(INB, LOW)
        else:
            GPIO.output(INA, LOW)
            GPIO.output(INB, HIGH)
        
    #정지
    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)
        
        
# GPIO 모드 설정 
GPIO.setmode(GPIO.BCM)
      
#모터 핀 설정
#핀 설정후 PWM 핸들 얻어옴 
pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)
        
# 모터 제어함수 간단하게 사용하기 위해 한번더 래핑(감쌈)
def setMotor(ch, speed, stat):
    if ch == CH1:
        #pwmA는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmA, IN1, IN2, speed, stat)
    else:
        #pwmB는 핀 설정 후 pwm 핸들을 리턴 받은 값이다.
        setMotorContorl(pwmB, IN3, IN4, speed, stat)
        
def on_press(key):
    print('Key %s pressed' % key)
    print(wave_distance)
    
    if str(key) == "'w'":
        if wave_distance > 10:
            setMotor(CH1, 100, FORWARD)
            setMotor(CH2, 100, FORWARD)
        
    elif str(key) == "'s'":
        setMotor(CH1, 100, BACKWORD)
        setMotor(CH2, 100, BACKWORD)
        
    elif str(key) == "'a'":
        setMotor(CH1, 100, LEFT)
        setMotor(CH2, 100, LEFT)
        
    elif str(key) == "'d'":
        setMotor(CH1, 100, RIGHT)
        setMotor(CH2, 100, RIGHT)
        
    elif str(key) == "'q'":
        #정지 
        setMotor(CH1, 80, STOP)
        setMotor(CH2, 80, STOP)
        

def on_release(key):
    print('Key %s released' %key)
    if key == kb.Key.esc: #esc 키가 입력되면 종료
        return False
    else:
        #정지 
        setMotor(CH1, 80, STOP)
        setMotor(CH2, 80, STOP)
        
def on_move(x,y):
    # print('Position : x:%s, y:%s' %(x,y))
    print("current mouse position:",pyautogui.position()) # 마우스 커서 x,y 좌표값 출력
        
    # 500 (0도) - 2500 (180도)
    value_x = (2419 - pyautogui.position().x) / 1.8 # x축 움직임
    value_y = pyautogui.position().y + 750 #y축 움직임
    
    if value_x < 500 : # 에러 방지
        value_x = 500
    
    pi.set_servo_pulsewidth(14, value_x) # 라즈베리파이 14번에 연결되어있는 서보모터 동작
    pi.set_servo_pulsewidth(15, value_y) # 라즈베리파이 15번에 연결되어있는 서보모터 동작
    time.sleep(0.1)
    
def wavesensor():
    while True:
        global wave_distance
        GPIO.output(24, False)
        time.sleep(0.5)

        GPIO.output(24, True)
        time.sleep(0.00001)
        GPIO.output(24, False)

        # 18번이 OFF가 되는 시점을 시작시간으로 설정
        while GPIO.input(23) == 0:
            start = time.time()

        # 18번이 ON이 되는 시점을 반사파 수신시간으로 설정
        while GPIO.input(23) == 1:
            stop = time.time()

        # 초음파가 되돌아오는 시간차로 거리를 계산한다
        time_interval = stop - start
        distance = time_interval * 17000
        distance = round(distance, 2)
        wave_distance = distance

        print("Distance => ", wave_distance, "cm")
    

def server_bind():
    HOST = '192.168.1.41'
    # 서버 주소, 라즈베리파이 IP 입력
    PORT = 5521
    # 클라이언트 접속 대기 포트 번호

    #전역변수 선언, 사용자의 키보드 입력을 받을 변수.
    global user_command

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #AF_INET : 주소 체계 IPv4 인터넷 프로토콜, SOCK_STREAM : TCP 통신

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # setsockopt : 소켓 옵션을 정하는 함수 
    # SOL_SOCKET : 소켓 옵션 레벨 중 하나
    # SO_REUSEADDR : 커널이 소켓을 사용하는 중에도 계속 소켓을 사용할 수 있도록 한다.

    #소켓을 특정 네트워크 인터페이스와 포트 번호에 연결.
    server_socket.bind((HOST,PORT))

    #서버가 클라이언트의 접속을 허용하도록 함.
    server_socket.listen()

    #accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓과 주소을 리턴
    client_socket, addr = server_socket.accept()

    #클라이언트의 주소 리턴
    print("Connected by ",addr)


    while True:

	    #클라이언트 보낸 메시지를 수신하기 위해 대기합니다.
	    user_command = client_socket.recv(1024)
	
	    #빈 문자열을 수신하면 루프를 중지합니다.
	    if data == 'break':
		    break

	    #수신받은 문자열을 출력합니다.
	    print("Received from ", addr, data.decode())
        user_command = data.decode()

    #소켓을 닫습니다.
    client_socket.close()
    server_socket.close()

        
t_wavesensor = threading.Thread(target=wavesensor)
t_socket = threading.Thread(target=server_bind)

# 리스너 등록
try:
    with kb.Listener(
        on_press=on_press,
        on_release=on_release) as kblistener, \
        ms.Listener(on_move=on_move) as mslistener:
        t_wavesensor.start()
        t_socket.start()
        kblistener.join()
        mslistener.join()
        



    
# 서보모터 종료
except KeyboardInterrupt:
    os.system("sudo killall pigpiod") # pigpio off
    pi.set_servo_pulsewidth(14, 0)
    pi.set_servo_pulsewidth(15, 0)
    pi.stop()
    t_wavesensor.close()
    t_socket.close()
    # 종료
    GPIO.cleanup()




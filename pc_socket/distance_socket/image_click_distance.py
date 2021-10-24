
import socket
import threading
import sys
import subprocess
import os
from datetime import datetime
import cv2 as cv2
import math
from queue import Queue
import math

queue = Queue() #쓰레드간 작업 공유, 서버와 opencv 쓰레드 간의 데이터 공유
dis_queue = Queue() # 거리 계산 쓰레드와 opencv 쓰레드 사이의 데이터 공유
s_queue = Queue() # 거리 계산 쓰레드와 서버 쓰레드 사이의 데이터 공유
#서보모터 1550기준.
def mouse_callback(event, x, y, flags, param): 
    
    if event == cv2.EVENT_LBUTTONDOWN:
        my_str = "x: "+str(x)+" y: "+str(y)+" 입니다"
        print(my_str) # 이벤트 발생한 마우스 위치 출력
        queue.put(my_str)
        dis_queue.put("opencv")
        dis_queue.put(x)
        dis_queue.put(y)
        
        


def opencv_img():
    
    img = cv2.imread("C:/Users/Park/Desktop/test3.jpg")
    cv2.namedWindow('image')  #마우스 이벤트 영역 윈도우 생성
    cv2.setMouseCallback('image', mouse_callback)

    while(True):

        cv2.imshow('image', img)

        k = cv2.waitKey(1) & 0xFF
        if k == 27:    # ESC 키 눌러졌을 경우 종료
            print("ESC 키 눌러짐")
            my_str = "break"
            queue.put(my_str)
            dis_queue.put(my_str)
            break
    cv2.destroyAllWindows()

def calculate_height():
    while(True):
        case = dis_queue.get()
        if case == "break":
            break
        degree = 0
        if case == "server":
            degree = disqueue.get()

        if case == "opencv":
            x = dis_queue.get()
            y = dis_queue.get()
            if y<=720 and y>=620:
                height = 720-y
                height = height * 0.03 * 1 + 10 #cm 기준
                if x<=640:
                    s_queue.put("L")
                    if x >= 0 and x <= 100:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x >= 100 and x <= 200:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x >= 200 and x <= 300:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x >= 300 and x <= 400:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x >= 400 and x <= 500:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x >= 500 and x <= 640:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                elif x>640:
                    s_queue.put("R")
                    if x>=1080 and x<=1280:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=980 and x<=1080:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=880 and x<=980:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=780 and x<=880:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=680 and x<=780:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=640 and x<=680:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                
            elif y<=620 and y>=520:
                height = 720-y
                height = height * 0.03 *1.4 + 10
                if x<=640:
                    s_queue.put("L")
                    if x>=0 and x<=100:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=100 and x<=200:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=200 and x<=300:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=300 and x<=400:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=400 and x<=500:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=500 and x<=640:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                elif x>640:
                    s_queue.put("R")
                    if x>=1080 and x<=1280:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=980 and x<=1080:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=880 and x<=980:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=780 and x<=880:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=680 and x<=780:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=640 and x<=680:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)

            elif y<=520 and y>=420:
                height = 720-y
                height = height * 0.03 *1.8 + 10
                if x<=640:
                    s_queue.put("L")
                    if x>=0 and x<=100:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=100 and x<=200:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=200 and x<=300:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=300 and x<=400:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=400 and x<=500:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=500 and x<=640:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                if x>640:
                    s_queue.put("R")
                    if x>=1080 and x<=1280:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=980 and x<=1080:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=880 and x<=980:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=780 and x<=880:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=680 and x<=780:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=640 and x<=680:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)

            elif y<=420 and y>=320:
                height = 720-y
                height = height * 0.03 *2.2 + 10
                if x<=640:
                    s_queue.put("L")
                    if x>=0 and x<=100:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=100 and x<=200:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=200 and x<=300:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=300 and x<=400:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=400 and x<=500:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=500 and x<=640:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                if x>640:
                    s_queue.put("R")
                    if x>=1080 and x<=1280:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=980 and x<=1080:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=880 and x<=980:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=780 and x<=880:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=680 and x<=780:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=640 and x<=680:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)

            elif y<=320 and y>=220:
                height = 720-y
                height = height * 0.03 * 3.5 + 10
                if x<=640:
                    s_queue.put("L")
                    if x>=0 and x<=100:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=100 and x<=200:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=200 and x<=300:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=300 and x<=400:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=400 and x<=500:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=500 and x<=640:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                if x>640:
                    s_queue.put("R")
                    if x>=1080 and x<=1280:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=980 and x<=1080:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=880 and x<=980:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=780 and x<=880:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=680 and x<=780:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=640 and x<=680:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)

            elif y<=220 and y>=120:
                height = 720-y
                height = height * 0.03 * 4 + 10
                if x<=640:
                    s_queue.put("L")
                    if x>=0 and x<=100:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=100 and x<=200:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=200 and x<=300:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=300 and x<=400:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=400 and x<=500:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=500 and x<=640:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                elif x>640:
                    s_queue.put("R")
                    if x>=1080 and x<=1280:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=980 and x<=1080:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=880 and x<=980:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=780 and x<=880:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=680 and x<=780:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=640 and x<=680:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)

            else:
                height = 720-y
                height = height * 0.03 * 5 + 10
                if x<=640:
                    s_queue.put("L")
                    if x>=0 and x<=100:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=100 and x<=200:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=200 and x<=300:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=300 and x<=400:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=400 and x<=500:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=500 and x<=640:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                elif x>640:
                    s_queue.put("R")
                    if x>=1080 and x<=1280:
                        width = 15
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=980 and x<=1080:
                        width = 10
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=880 and x<=980:
                        width = 5
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=780 and x<=880:
                        width = 3
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=680 and x<=780:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)
                    elif x>=640 and x<=680:
                        width = 2
                        distance = math.sqrt(height * height + width * width)
                        s_queue.put(width)
                        s_queue.put(height)
                        print(distance)

def client_send():
    HOST = '192.168.1.165'
    # 서버 주소, 라즈베리파이 IP 입력
    PORT = 5521
    # 클라이언트 접속 대기 포트 번호

    #소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #지정한 HOST와 PORT로 연결
    client_socket.connect((HOST, PORT))
    
    #라즈베리파이의 각도를 받는다.
    # degree = client_socket.recv(1024)
    # num = int.from_bytes(degree, byteorder='little') # byte를 int형으로 변환
    # dis_queue.put("server")
    # dis_queue.put(num)
    # print("Current degree : ", num)

    while True:
        #메시지를 전송합니다 opencv에서 받은 x,y좌표
        my_str = queue.get() 
        user_command = my_str

        client_socket.sendall(user_command.encode())

        #메시지를 전송합니다 거리 계산에서 나온 거리 값
        direction =s_queue.get() # 방향전달

        go_r =s_queue.get() # 가로로 얼마 갈지 전달
        
        temp =s_queue.get()# 앞으로 얼마갈지 전달
        go_l = int(temp)
        
        go = direction + "/" + str(go_r) + "/" + str(go_l)
        print(go)
        client_socket.sendall(str(go).encode())

        #메시지 수신
        
        data = client_socket.recv(1024)
        print("Received ", repr(data.decode()))
        # qkdkran https://shoark7.github.io/programming/python/difference-between-__repr__-vs-__str__

        if user_command == 'break':
            print("연결 종료")
            break
            


#쓰레드 열기
t_socket = threading.Thread(target=client_send)
t_imgShow = threading.Thread(target=opencv_img)
t_height = threading.Thread(target=calculate_height)
t_socket.start()
t_imgShow.start()
t_height.start()

k = cv2.waitKey(1) & 0xFF
if k == 27:    # ESC 키 눌러졌을 경우 종료
    print("ESC 키 눌러짐")
    t_socket.close()
    t_imgShow.close()
    t_height.close()


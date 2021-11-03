# -*- coding: utf-8 -*-
import socket
import threading
import sys
import subprocess
import os
from datetime import datetime
import cv2 as cv2
import math
from queue import Queue
from time import sleep

queue = Queue() #쓰레드간 작업 공유, 서버와 opencv 쓰레드 간의 데이터 공유
dis_queue = Queue() # 거리 계산 쓰레드와 opencv 쓰레드 사이 대기 큐
s_queue = Queue() # 거리 계산 쓰레드와 서버 쓰레드 사이의 데이터 공유
# value_queue = Queue() # 거리 계산 시 필요한 x,y 픽셀값 공유

def mouse_callback(event, x, y, flags, param): 
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        my_str = str(x)+"/"+str(y)
        print(my_str) # 이벤트 발생한 마우스 위치 출력
        queue.put(my_str)
        dis_queue.put("opencv")
        dis_queue.put(x)
        dis_queue.put(y)

def opencv_img():
    
    url = 'rtsp://192.168.1.165:8554/test'
    cap = cv2.VideoCapture(url)
    cv2.namedWindow('image')  #마우스 이벤트 영역 윈도우 생성
    cv2.setMouseCallback('image', mouse_callback)

    while(True):
        ret, frame = cap.read()    # Read 결과와 frame
        
        if(ret) :
            cv2.imshow('image', frame)    # 컬러 화면 출력

        k = cv2.waitKey(1) & 0xFF
        if k == 27:    # ESC 키 눌러졌을 경우 종료
            print("ESC 키 눌러짐")
            my_str = "break"
            queue.put(my_str)
            dis_queue.put(my_str)
            break
    cap.release()
    cv2.destroyAllWindows()

def calculate_distance():
    while(True):
        case = dis_queue.get()
        if case == "break":
            break
        degree = 0
        if case == "server": # 라즈베리파이로부터 서보모터의 각도 값을 받아올 경우 사용
            degree = disqueue.get()

        if case == "opencv": # 1550 기준
            x = dis_queue.get()
            y = dis_queue.get()
            
            if y <= 720 and y > 600: # y축 기준으로 나누기
                height = (720 - y) / 4 #앞으로 얼마를 갈지
                
                if 630 < x and x < 650: # 중심을 고른 경우
                    s_queue.put("C") 
                    s_queue.put(0)
                    s_queue.put(int(height))

                elif x <= 630: #왼쪽
                    width = 0.03 * abs(x - 630) # 좌우로 얼마나 이동할지
                    s_queue.put("L") 
                    s_queue.put((width))
                    s_queue.put(int(height))

                elif x >= 650: #오른쪽
                    width = 0.03 * abs(x - 650) 
                    s_queue.put("R")
                    s_queue.put((width))
                    s_queue.put(int(height))

            elif y <= 600 and y > 420:
                height = (600 - y) / 6 + 30

                if 635 < x and x < 645: # 중심을 고른 경우
                    s_queue.put("C") 
                    s_queue.put(0)
                    s_queue.put(int(height))
                    
                elif x <= 635: #왼쪽
                    width = (30 / 730) * abs(x - 635) # 좌우로 얼마나 이동할지
                    s_queue.put("L") 
                    s_queue.put((width))
                    s_queue.put(int(height))

                elif x >= 645: #오른쪽
                    width = (30 / 730) * abs(x - 645) # 좌우로 얼마나 이동할지
                    s_queue.put("R")
                    s_queue.put((width))
                    s_queue.put(int(height))
                
            elif y <= 420 and y > 340:           
                
                height = (420 - y) / (80 / 30) + 60

                if 635 < x and x < 645: # 중심을 고른 경우
                    s_queue.put("C") 
                    s_queue.put(0)
                    s_queue.put(int(height))
                    
                elif x <= 635: #왼쪽
                    width = (30 / 330) * abs(x - 635) # 좌우로 얼마나 이동할지
                    s_queue.put("L") 
                    s_queue.put((width))
                    s_queue.put(int(height))

                elif x >= 645: #오른쪽
                    width = (30 / 330) * abs(x - 645) # 좌우로 얼마나 이동할지
                    s_queue.put("R")
                    s_queue.put((width))
                    s_queue.put(int(height))
                
            elif y <= 340 and y > 312:
                
                height = (340 - y) / (28 / 30) + 95

                if 638 < x and x < 642: # 중심을 고른 경우
                    s_queue.put("C") 
                    s_queue.put(0)
                    s_queue.put(int(height))
                    
                elif x <= 638: #왼쪽
                    width = (30 / 200) * abs(x - 640) # 좌우로 얼마나 이동할지
                    s_queue.put("L") 
                    s_queue.put((width))
                    s_queue.put(int(height))

                elif x >= 642: #오른쪽
                    width = (30 / 200) * abs(x - 640) # 좌우로 얼마나 이동할지
                    s_queue.put("R")
                    s_queue.put((width))
                    s_queue.put(int(height))


            elif y <= 312 and y > 290:
                
                height = (312 - y) / (22 / 30) + 125

                if 638 < x and x < 642: # 중심을 고른 경우
                    s_queue.put("C") 
                    s_queue.put(0)
                    s_queue.put(int(height))
                    
                elif x <= 638: #왼쪽
                    width = (30 / 160) * abs(x - 640) # 좌우로 얼마나 이동할지
                    s_queue.put("L") 
                    s_queue.put((width))
                    s_queue.put(int(height))

                elif x >= 642: #오른쪽
                    width = (30 / 160) * abs(x - 640) # 좌우로 얼마나 이동할지
                    s_queue.put("R")
                    s_queue.put((width))
                    s_queue.put(int(height))


            elif y <= 290 and y > 280:
                
                height = (290 - y) / (10 / 20) + 135

                if 638 < x and x < 642: # 중심을 고른 경우
                    s_queue.put("C") 
                    s_queue.put(0)
                    s_queue.put(int(height))
                    
                elif x <= 638: #왼쪽
                    width = (30 / 130) * abs(x - 640) # 좌우로 얼마나 이동할지
                    s_queue.put("L") 
                    s_queue.put((width))
                    s_queue.put(int(height))

                elif x >= 642: #오른쪽
                    width = (30 / 130) * abs(x - 640) # 좌우로 얼마나 이동할지
                    s_queue.put("R")
                    s_queue.put((width))
                    s_queue.put(int(height))
                
            else: # 땅이 아닌 부분
                print("땅이 아닙니다.")

def client_send():
    HOST = '192.168.1.165'
    # 서버 주소, 라즈베리파이 IP 입력
    PORT = 5521
    # 클라이언트 접속 대기 포트 번호

    #소켓 생성
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    #지정한 HOST와 PORT로 연결
    client_socket.connect((HOST, PORT))
    

    while True:
        #메시지를 전송합니다
        my_str = queue.get()
        user_command = my_str

        #client_socket.sendall(user_command.encode())

        if user_command == 'break':
            print("연결 종료")
            break

        #메시지를 전송합니다 거리 계산에서 나온 거리 값
        direction =s_queue.get() # 방향전달
        

        go_w =s_queue.get() # 가로로 얼마 갈지 전달
      

        temp =s_queue.get()# 앞으로 얼마갈지 전달
        go_h = int(temp)
        

        go = direction + "/" + str(go_w) + "/" + str(go_h)
        print(go)
        client_socket.sendall(str(go).encode())

        #메시지 수신

        data = client_socket.recv(1024)
        print("Received ", repr(data.decode()))
        # https://shoark7.github.io/programming/python/difference-between-__repr__-vs-__str__

        
            


#쓰레드 열기
t_socket = threading.Thread(target=client_send)
t_imgShow = threading.Thread(target=opencv_img)
t_distance = threading.Thread(target=calculate_distance)
t_socket.start()
t_imgShow.start()
t_distance.start()

k = cv2.waitKey(1) & 0xFF
if k == 27:    # ESC 키 눌러졌을 경우 종료
    print("ESC 키 눌러짐")
    t_socket.close()
    t_imgShow.close()
    t_distance.close()


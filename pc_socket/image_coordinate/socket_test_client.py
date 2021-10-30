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
            if y <= 720 and y > 400: # y축 기준으로 나누기
                if 0 <= x and x < 400:
                    s_queue.put("L") # 좌로 움직이기
                    s_queue.put(20) # 좌로 15cm
                    s_queue.put(10) # 앞으로 15cm

                elif 400 <= x and x < 800:
                    s_queue.put("C") # 중간으로 직진
                    s_queue.put(0) # 좌우로 0
                    s_queue.put(10) # 앞으로 15cm

                else:
                    s_queue.put("R") # 우로 움직이기.
                    s_queue.put(20) # 우로 15cm
                    s_queue.put(10) # 앞으로 15cm

            elif y <= 400 and y > 300:
                if 0 <= x and x < 400:
                    s_queue.put("L") # 좌로 움직이기
                    s_queue.put(20) # 좌로 15cm
                    s_queue.put(40) # 앞으로 40cm

                elif 400 <= x and x < 800:
                    s_queue.put("C") # 중간으로 직진
                    s_queue.put(0) # 좌우로 0
                    s_queue.put(40) # 앞으로 40cm

                else:
                    s_queue.put("R") # 우로 움직이기.
                    s_queue.put(20) # 우로 15cm
                    s_queue.put(40) # 앞으로 40cm

            elif y <= 300 and y > 220:           
                if 0 <= x and x < 256:
                    s_queue.put("L") # 좌로 움직이기
                    s_queue.put(40) # 좌로 40cm
                    s_queue.put(80) # 앞으로 40cm

                elif 256 <= x and x < 512:
                    s_queue.put("L") # 좌로 움직이기
                    s_queue.put(20) # 좌로 20cm
                    s_queue.put(80) # 앞으로 40cm
                
                elif 512 <= x and x < 768:
                    s_queue.put("C") # 중간으로 직진
                    s_queue.put(0) # 좌우로 0
                    s_queue.put(80) # 앞으로 40cm

                elif 768 <= x and x < 1024:
                    s_queue.put("R") # 중간으로 직진
                    s_queue.put(20) # 좌우로 0
                    s_queue.put(80) # 앞으로 40cm

                else:
                    s_queue.put("R") # 우로 움직이기.
                    s_queue.put(40) # 우로 15cm
                    s_queue.put(80) # 앞으로 40cm

            elif y <= 220 and y > 160:
                if 0 <= x and x < 183:
                    s_queue.put("L") # 좌로 움직이기
                    s_queue.put(60) # 좌로 40cm
                    s_queue.put(120) # 앞으로 40cm

                elif 183 <= x and x < 366:
                    s_queue.put("L") # 좌로 움직이기
                    s_queue.put(40) # 좌로 20cm
                    s_queue.put(120) # 앞으로 40cm
                
                elif 366 <= x and x < 549:
                    s_queue.put("L") # 중간으로 직진
                    s_queue.put(20) # 좌우로 0
                    s_queue.put(120) # 앞으로 40cm

                elif 549 <= x and x < 732:
                    s_queue.put("C") # 중간으로 직진
                    s_queue.put(0) # 좌우로 0
                    s_queue.put(120) # 앞으로 40cm

                elif 732 <= x and x < 915:
                    s_queue.put("R") # 중간으로 직진
                    s_queue.put(20) # 좌우로 0
                    s_queue.put(120) # 앞으로 40cm
                
                elif 915 <= x and x < 1098:
                    s_queue.put("R") # 중간으로 직진
                    s_queue.put(40) # 좌우로 0
                    s_queue.put(120) # 앞으로 40cm

                else:
                    s_queue.put("R") # 우로 움직이기.
                    s_queue.put(60) # 우로 15cm
                    s_queue.put(120) # 앞으로 40cm

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

        client_socket.sendall(user_command.encode())

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


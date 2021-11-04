# -*- coding: utf-8 -*-
import socket
import threading
import sys
import subprocess
import os
from datetime import datetime
import cv2 as cv2
import numpy as np
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
    
    url = 'rtsp://192.168.1.243:8554/test'
    cap = cv2.VideoCapture(url)
    YOLO_net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg")

    #roi = img[100:600, 200:400]
    #width, height, channel = img.shape

    #각 사물에 해당하는 이미지(AR) 불러오기
    #1번째 이미지: person
    logo = cv2.imread('user.jpg') #person
    #2번째 이미지: refrigerator
    refri = cv2.imread('refri.jpg') #냉장고
    #3번째 이미지: bottle
    bottle = cv2.imread('bottle.jpg') #병
    #이미지 크기 조절
    size = 20
    logo = cv2.resize(logo, (size, size))
    refri = cv2.resize(refri,(size,size))
    bottle = cv2.resize(bottle,(size,size))

    img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

    img2gray_2 = cv2.cvtColor(refri, cv2.COLOR_BGR2GRAY)
    ret_2, mask_2 = cv2.threshold(img2gray_2, 1, 255, cv2.THRESH_BINARY)

    img2gray_3 = cv2.cvtColor(bottle, cv2.COLOR_BGR2GRAY)
    ret_3, mask_bottle = cv2.threshold(img2gray_3, 1, 255, cv2.THRESH_BINARY)

    # YOLO NETWORK 재구성
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = YOLO_net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

    
    cv2.namedWindow('image')  #마우스 이벤트 영역 윈도우 생성
    cv2.setMouseCallback('image', mouse_callback)

    while(True):
        ret, frame = cap.read()    # Read 결과와 frame
        h, w, c = frame.shape

        # YOLO 입력
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
        True, crop=False)
        YOLO_net.setInput(blob)
        outs = YOLO_net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []

        for out in outs:

            for detection in out:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * w)
                    center_y = int(detection[1] * h)
                    dw = int(detection[2] * w)
                    dh = int(detection[3] * h)
                    # Rectangle coordinate
                    x = int(center_x - dw / 2)
                    y = int(center_y - dh / 2)
                    boxes.append([x, y, dw, dh])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)


        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                score = confidences[i]

                # 경계상자와 클래스 정보 이미지에 입력
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5, 
                (0, 0, 0), 1)
                
                #라벨 입력(정보 입력)
                if label == 'person':
                    cv2.putText(frame, "Konkuk Stu.", (x+w-100, y+15), cv2.FONT_ITALIC, 0.5, 
                        (0, 0, 0), 1)
                    
                    #특정 위치에 이미지 불러오기
                    if ret:
                    # Flip the frame
                        #frame = cv2.flip(frame, 1)

                    # Region of Image (ROI), where we want to insert logo
                    # 화면 밖으로 나가는 것을 방지하기 위함(x창: 640 y창: 480)
                        if x>620:
                            x=620
                        elif x<0:
                            x=0
                        
                        if y>460:
                            y=460
                        elif y<0:
                            y=0
                        roi = frame[y:y+20,x:x+20]
                        
                    
                    # Set an index of where the mask is
                        roi[np.where(mask)] = 0
                        roi += logo
                        
                        
                        #frame=cv2.flip(frame,1)
                elif label == 'refrigerator':
                    cv2.putText(frame, "store food", (x+w-100, y+15), cv2.FONT_ITALIC, 0.5, 
                                (0, 0, 0), 1)
                    
                    if ret_2:
                    
                        #roi_refri = frame[y:y+20,x+w+100:x+w+120]
                        if x>620:
                            x=620
                        elif x<0:
                            x=0
                        
                        if y>460:
                            y=460
                        elif y<0:
                            y=0
                        roi_refri = frame[y:y+20,x-20:x]

                        roi_refri[np.where(mask_2)] = 0
                        roi_refri += refri
    
                elif label == 'bottle':
                    cv2.putText(frame, "store drink", (x+w-100, y+15), cv2.FONT_ITALIC, 0.5, 
                                (0, 0, 0), 1)
                    
                    if ret_3:
                        if x>620:
                            x=620
                        elif x<0:
                            x=0
                        
                        if y>460:
                            y=460
                        elif y<0:
                            y=0
                        #roi_refri = frame[y:y+20,x+w+100:x+w+120]
                        roi_bottle = frame[y:y+20,x:x+20]
                        
                    # Set an index of where the mask is
                        roi_bottle[np.where(mask_bottle)] = 0
                        roi_bottle += bottle

                else:
                    cv2.circle(frame, (x+w-10,y+10), 5, (0,0,255), -1)



        cv2.imshow('image', frame)

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
        # if case == "server": # 라즈베리파이로부터 서보모터의 각도 값을 받아올 경우 사용

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
    HOST = '192.168.1.243'
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


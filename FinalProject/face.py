#!/usr/bin/env python
# coding: utf-8

# In[56]:


import cv2
import numpy as np

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg")


#roi = img[100:600, 200:400]
#width, height, channel = img.shape

#각 사물에 해당하는 이미지(AR) 불러오기
#1번째 이미지: person
logo = cv2.imread('user.jpg')
#2번째 이미지: refrigerator
refri = cv2.imread('refri.jpg')
#3번째 이미지: bottle
bottle = cv2.imread('bottle.jpg')
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
ret_3, mask_3 = cv2.threshold(img2gray_3, 1, 255, cv2.THRESH_BINARY)
# YOLO NETWORK 재구성
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    height, width, channels = frame.shape

    # YOLO 입력
    #이미지를 가지고 4차원의 blob을 만들어 넘겨준다.
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),
    True, crop=False)
    YOLO_net.setInput(blob)
    #신경망이 인식한 결과가 들어간다.
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
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                dw = int(detection[2] * width)
                dh = int(detection[3] * height)
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
                    roi_3 = frame[y:y+20,x:x+20]
                    
                # Set an index of where the mask is
                    roi_3[np.where(mask_3)] = 0
                    roi_3 += refri

            else:
                cv2.circle(frame, (x+w-10,y+10), 5, (0,0,255), -1)



    cv2.imshow("YOLOv3", frame)

    if cv2.waitKey(1) == ord('q'): 
        break
VideoSignal.release()
cv2.destroyAllWindows()


# In[ ]:





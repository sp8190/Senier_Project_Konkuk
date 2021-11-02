#!/usr/bin/env python
# coding: utf-8

# In[35]:



import cv2
import numpy as np

# 웹캠 신호 받기
VideoSignal = cv2.VideoCapture(0)
# YOLO 가중치 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg")


#roi = img[100:600, 200:400]
#width, height, channel = img.shape

#각 사물에 해당하는 이미지(AR) 불러오기
logo = cv2.imread('user.jpg')
refri = cv2.imread('refri.jpg')
size = 20
logo = cv2.resize(logo, (size, size))
refri = cv2.resize(refri,(size,size))
img2gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)
img2gray_2 = cv2.cvtColor(refri, cv2.COLOR_BGR2GRAY)
ret_refri, mask_refri = cv2.threshold(img2gray, 1, 255, cv2.THRESH_BINARY)

# YOLO NETWORK 재구성
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
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
            #
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
                    frame = cv2.flip(frame, 1)

                # Region of Image (ROI), where we want to insert logo
                    #roi = frame[-size-10:-10, -size-10:-10]
                    #roi = frame[-size-10:-10, -size-10:-10]
                    #roi = frame[-60:-10,-60:-10]
                    
                    #성공한 예시
                    #roi = frame[x-90:x-80,y+5:y+15] 
                    #roi = frame[y+15:y+35,x+w-480:x+w-460]
                    roi = frame[y:y+20,x-20:x]
                # Set an index of where the mask is
                    roi[np.where(mask)] = 0
                    roi += logo
                    frame=cv2.flip(frame,1)
            elif label == 'refrigerator':
                cv2.putText(frame, "store food", (x+w-100, y+15), cv2.FONT_ITALIC, 0.5, 
                            (0, 0, 0), 1)
                
                if ret_refri:
                # Flip the frame
                    frame = cv2.flip(frame, 1)
 
                    roi_refri = frame[y:y+20,x+w+100:x+w+120]
                    
                    
                # Set an index of where the mask is
                    roi_refri[np.where(mask_refri)] = 0
                    roi_refri += refri
                    frame=cv2.flip(frame,1)
                
            else:
                cv2.circle(frame, (x+w-10,y+10), 5, (0,0,255), -1)



    cv2.imshow("YOLOv3", frame)

    if cv2.waitKey(1) == ord('q'): 
        break
VideoSignal.release()
cv2.destroyAllWindows()


# In[ ]:





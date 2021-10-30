#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cv2
import numpy as np

#device 내장캠, whT=영상크기
device = 0
cap = cv2.VideoCapture(device)
whT = 320

confThreshold_1 = 0.5
confThreshold_2 = 0.7
nmsThreshold = 0.3

classesFile = 'C:\senior_project\Senior_Project_Konkuk\AR\coco.names'

with open(classesFile, 'rt') as f:
        classNames = f.read().split('\n')

#모델 불러오기
model_config = 'C:\senior_project\Senior_Project_Konkuk\AR\yolov3-tiny.cfg'
model_weights = 'C:\senior_project\Senior_Project_Konkuk\AR\yolov3-tiny.weights'

net = cv2.dnn.readNetFromDarknet(model_config, model_weights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

#객체 식별 함수
def findObjects(outputs, img):
        hT, wT, cT = img.shape
        bbox = []
        classIds = []
        confs = []
    
        for output in outputs:
            for det in output:
                scores = det[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold_1:
                    w, h = int(det[2]*wT), int(det[3]*hT)
                    x, y = int((det[0]*wT) - w/2), int((det[1]*hT) - h/2)
                    bbox.append([x,y,w,h])
                    classIds.append(classId)
                    confs.append(float(confidence))
          
        #중복된 박스생성을 막기위한 NMS알고리즘
        indices = cv2.dnn.NMSBoxes(bbox, confs, confThreshold_2, nmsThreshold)
        #print(f"식별된 대상 : {len(indices)} 개")
    
    #걸러진 데이터를 토대로 이미지에 박스 및 텍스트 생성
        for i in indices:
            i = i[0]
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, f"{classNames[classIds[i]].upper()} {int(confs[i]*100)}%",
                     (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
 
while True:
    success, img = cap.read()
    
    if not success:
        break
 #성공했을때 true값 반환   
    blob = cv2.dnn.blobFromImage(img, 1/255, (whT, whT), [0,0,0], True, crop=False)
    net.setInput(blob)
    
    layerNames = net.getLayerNames()
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(outputNames)
    
    findObjects(outputs, img)
    
    cv2.imshow("Image", img)
    
    
    #q 누르면 종료
    if cv2.waitKey(1) == ord('q'): 
        break
cap.release()
cv2.destroyAllWindows()


# In[ ]:





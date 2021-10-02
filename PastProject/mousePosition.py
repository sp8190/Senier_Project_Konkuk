#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install pyautogui로 마우스제어 설치
import pyautogui
import time

pyautogui.PAUSE=1
pyautogui.FAILSAFE=True

#1초마다 마우스의 위치를 반환(x,y)
while True:
    print("current mouse position:",pyautogui.position())
    time.sleep(1)


# In[ ]:





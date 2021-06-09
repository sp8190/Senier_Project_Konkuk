import time
import pigpio
import pyautogui


pi = pigpio.pi() # Connect to local Pi.
try:
    while 1:
        print("current mouse position:",pyautogui.position()) # 마우스 커서 x,y 좌표값 출력
        
        # 500 (0도) - 2500 (180도)
        value_x = (2419 - pyautogui.position().x) / 1.8 # x축 움직임
        value_y = pyautogui.position().y + 750 #y축 움직임
        
        if value_x < 500 : # 에러 방지
            value_x = 500
        
        pi.set_servo_pulsewidth(23, value_x) # 라즈베리파이 23번에 연결되어있는 서보모터 동작
        #pi.set_servo_pulsewidth(14, value_y) # 라즈베리파이 14번에 연결되어있는 서보모터 동작
        time.sleep(0.01)

except KeyboardInterrupt:
    # switch servo off
    pi.set_servo_pulsewidth(23, 0);
    #pi.set_servo_pulsewidth(14, 0);
    pi.stop()

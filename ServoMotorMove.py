import time
import pigpio
import pyautogui


pi = pigpio.pi() # Connect to local Pi.
try:
    while 1:
        print("current mouse position:",pyautogui.position())
        
        # 500 (0도) - 2500 (180도)
        value_x = (2419 - pyautogui.position().x) / 1.8
        value_y = pyautogui.position().y + 750
        
        if value_x < 500 :
            value_x = 500
        
        pi.set_servo_pulsewidth(23, value_x)
        #pi.set_servo_pulsewidth(14, value_y)
        time.sleep(0.01)

except KeyboardInterrupt:
    # switch servo off
    pi.set_servo_pulsewidth(23, 0);
    #pi.set_servo_pulsewidth(14, 0);
    pi.stop()

import pandas as pd
import numpy as np
import cv2
import threading

df = pd.read_excel('my_test.xlsx')

print(df['y_phase 1'][2])
print("\n")
print(df['x_phase 1 left'][2])
print("\n")
print(df['x_phase 1 right'][2])
print("\n")
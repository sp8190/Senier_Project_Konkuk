import pandas as pd
import numpy as np
import cv2
import threading

df = pd.read_excel('my_test.xlsx')

degree = "lowest"

if degree == "lowest":
    index = 0
elif degree == "lower":
    index = 1
elif degree == "middle":
    index = 2
elif degree == "higher":
    index = 3
elif degree == "highest":
    index = 4

print(df['y_phase 1'][2])
print("\n")
print(df['x_phase 1 left'][2])
print("\n")
print(df['x_phase 1 right'][2])
print("\n")
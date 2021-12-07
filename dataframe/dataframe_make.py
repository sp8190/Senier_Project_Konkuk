import pandas as pd
import numpy as np
import cv2
import threading



distance_data = pd.DataFrame(
    {
        'camera': ['lowest', 'lower', 'middle', 'higher', 'highest'],
        'y_phase 1': ['', '', '600', '', ''],
        'y_phase 2': ['', '', '420', '', ''],
        'y_phase 3': ['', '', '340', '', ''],
        'y_phase 4': ['', '', '312', '', ''],
        'y_phase 5': ['', '', '290', '', ''],
        'y_phase 6': ['', '', '280', '', ''],
        'x_phase 1 left': ['', '', '630', '', ''],
        'x_phase 2 left': ['', '', '635', '', ''],
        'x_phase 3 left': ['', '', '635', '', ''],
        'x_phase 4 left': ['', '', '638', '', ''],
        'x_phase 5 left': ['', '', '638', '', ''],
        'x_phase 6 left': ['', '', '638', '', ''],
        'x_phase 1 right': ['', '', '650', '', ''],
        'x_phase 2 right': ['', '', '645', '', ''],
        'x_phase 3 right': ['', '', '645', '', ''],
        'x_phase 4 right': ['', '', '642', '', ''],
        'x_phase 5 right': ['', '', '642', '', ''],
        'x_phase 6 right': ['', '', '642', '', ''],
        'x_phase 1': ['', '', '1000', '', ''],
        'x_phase 2': ['', '', '730', '', ''],
        'x_phase 3': ['', '', '330', '', ''],
        'x_phase 4': ['', '', '200', '', ''],
        'x_phase 5': ['', '', '160', '', ''],
        'x_phase 6': ['', '', '130', '', ''],
        'phase is 30cm': ['', '', '', '', ''],
 
})

distance_data.to_excel("my_test.xlsx")
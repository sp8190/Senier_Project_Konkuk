import pandas as pd
import numpy as np
import cv2
import threading



distance_data = pd.DataFrame(
    {
        'camera': ['lowest', 'lower', 'middle', 'higher', 'highest'],
        'y_phase 1': ['1', '1', '600', '1', '1'],
        'y_phase 2': ['1', '1', '420', '1', '1'],
        'y_phase 3': ['1', '1', '340', '1', '1'],
        'y_phase 4': ['1', '1', '312', '1', '1'],
        'y_phase 5': ['1', '1', '290', '1', '1'],
        'y_phase 6': ['1', '1', '280', '1', '1'],
        'x_phase 1 left': ['1', '1', '630', '1', '1'],
        'x_phase 2 left': ['1', '1', '635', '1', '1'],
        'x_phase 3 left': ['1', '1', '635', '1', '1'],
        'x_phase 4 left': ['1', '1', '638', '1', '1'],
        'x_phase 5 left': ['1', '1', '638', '1', '1'],
        'x_phase 6 left': ['1', '1', '638', '1', '1'],
        'x_phase 1 right': ['1', '1', '650', '1', '1'],
        'x_phase 2 right': ['1', '1', '645', '1', '1'],
        'x_phase 3 right': ['1', '1', '645', '1', '1'],
        'x_phase 4 right': ['1', '1', '642', '1', '1'],
        'x_phase 5 right': ['1', '1', '642', '1', '1'],
        'x_phase 6 right': ['1', '1', '642', '1', '1'],
        'x_phase 1': ['1', '1', '1000', '1', '1'],
        'x_phase 2': ['1', '1', '730', '1', '1'],
        'x_phase 3': ['1', '1', '330', '1', '1'],
        'x_phase 4': ['1', '1', '200', '1', '1'],
        'x_phase 5': ['1', '1', '160', '1', '1'],
        'x_phase 6': ['1', '1', '130', '1', '1'],
        'phase is 30cm': ['', '', '', '', ''],
 
})

distance_data.to_excel("my_test.xlsx")
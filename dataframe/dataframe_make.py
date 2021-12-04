import pandas as pd
import numpy as np
import cv2
import threading



distance_data = pd.DataFrame(
    {
        'camera': ['lowest', 'lower', 'middle', 'higher', 'highest'],
        'y_phase 1': ['', '', '', '', ''],
        'y_phase 2': ['', '', '', '', ''],
        'y_phase 3': ['', '', '', '', ''],
        'y_phase 4': ['', '', '', '', ''],
        'y_phase 5': ['', '', '', '', ''],
        'x_phase 1': ['', '', '', '', ''],
        'x_phase 2': ['', '', '', '', ''],
        'x_phase 3': ['', '', '', '', ''],
        'x_phase 4': ['', '', '', '', ''],
        'x_phase 5': ['', '', '', '', ''],
        
})

distance_data.to_excel("my_test.xlsx")
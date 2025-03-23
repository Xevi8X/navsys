import cv2
import math
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'algorithm')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sim')))

from camera import Camera
from terrain import Terrain
from trajectory import NEDConverter
from utils import rot_Z


def calc_loc(x, y):
    camera = Camera()
    terrain = Terrain()
    ned = NEDConverter(52.2669725, 20.9239028, 106)
    pos = np.array([0.0, 0.0, -200])

    vec = camera.pixel_to_vec(x, y)
    vec = rot_Z(math.radians(280)) @ vec
    print(vec)
    loc = terrain.find_intersection(pos, vec)
    lla = ned.to_lla(loc[0], loc[1], loc[2])
    print(lla)

def click_event(event, x, y, flags, param):
    if event != cv2.EVENT_LBUTTONDOWN:
        return
    print(x, y)
    calc_loc(x, y)

image = cv2.imread('epbc.png')
cv2.imshow('image', image)
cv2.setMouseCallback('image', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()
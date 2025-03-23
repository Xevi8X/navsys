import math
import numpy as np

class Terrain:

    def __init__(self):
        pass

    def find_intersection(self, postion, direction):
        if math.isclose(direction[2], 0.0):
            return postion

        return postion - direction * (postion[2] / direction[2])
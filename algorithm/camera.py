import math
import numpy as np

from utils import rot_X, rot_Y, rot_Z

class Camera:
    def __init__(self, resolution = np.array([1280, 720]), fovx = 75, fovy = 47):
        self.resolution = resolution
        self.fovx = math.radians(fovx)
        self.fovy = math.radians(fovy)

        self.px2az = math.tan(self.fovx / 2)
        self.py2el = math.tan(self.fovy / 2)

        self.mount_rotation = rot_Y(math.radians(-15))

    def pixel_to_vec(self, x, y):
        x = 2.0 * x / self.resolution[0] - 1.0
        y = 2.0 * y / self.resolution[1] - 1.0

        dir = np.array([1 , x * self.px2az, y * self.py2el])
        dir /= np.linalg.norm(dir)

        return self.mount_rotation @ dir

if __name__ == '__main__':
    camera = Camera()

    print(camera.pixel_to_vec(640, 360))
    print(camera.pixel_to_vec(0, 0))
    print(camera.pixel_to_vec(1280, 720))
    print(camera.pixel_to_vec(640, 700))



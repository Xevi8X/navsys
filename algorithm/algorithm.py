import numpy as np
import time

from ahrs_recv import AHRSRecv
from gs_estimator import GroundSpeedEstimator
from video_recv import VideoRecv

if __name__ == '__main__':
    gs_estimator = GroundSpeedEstimator()

    video_recv = VideoRecv()
    ahrs_recv = AHRSRecv()

    def callback(timestamp, frame):
        attitude, height_amsl = ahrs_recv.get()
        gs_estimator.feed(timestamp, frame, attitude, height_amsl)
        
    video_recv.set_callback(callback)

    ahrs_recv.start()
    video_recv.start()

    while True:
        time.sleep(1)

    
import numpy as np
import time

from ahrs_recv import AHRSRecv
from gs_estimator import GroundSpeedEstimator
from video_recv import VideoRecv

if __name__ == '__main__':
    gs_estimator = GroundSpeedEstimator()

    video_recv = VideoRecv()
    ahrs_recv = AHRSRecv()

    log = open("gs.csv", "w")
    log.write("time,gs_x,gs_y,gs_z,true_gs_x,true_gs_y,true_gs_z\n")

    def callback(timestamp, frame):
        t, pos, att, gs_true = ahrs_recv.get()
        if t < 0.0:
            return
        gs = gs_estimator.feed(timestamp, frame, pos, att)
        if gs is not None:
            log.write(f"{t},{gs[0]},{gs[1]},{gs[2]},{gs_true[0]},{gs_true[1]},{gs_true[2]}\n")

    video_recv.set_callback(callback)

    ahrs_recv.start()
    video_recv.start()

    while True:
        time.sleep(1)

    
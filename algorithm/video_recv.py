import cv2 as cv
import threading
import time

class VideoRecv(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gstreamer_pipeline = (
            "udpsrc port=5000 ! application/x-rtp,media=video,encoding-name=H264,payload=96 ! "
            "rtph264depay ! avdec_h264 ! videoconvert ! appsink"
        )
        self.cap = cv.VideoCapture(self.gstreamer_pipeline, cv.CAP_GSTREAMER)
        if not self.cap.isOpened():
            raise Exception("Error: Unable to open video stream.")
        self.callback = None
        self.is_running = False
        
    def set_callback(self, callback):
        self.callback = callback

    def run(self):
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Error: Failed to read frame.")
            if self.callback:
                self.callback(time.time(), frame)

    
    def __del__(self):
        self.cap.release()


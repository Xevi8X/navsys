import struct
import numpy as np
import socket
import threading
import time

class AHRSRecv(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mtx = threading.RLock()
        self.atttude = (0.0, 0.0, 0.0)
        self.height_amsl = 0
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 6000))
        
    def get(self):
        with self.mtx:
            return self.atttude, self.height_amsl
        
    def run(self):
        while True:
            data, _ = self.sock.recvfrom(16)
            h, roll, pitch, yaw, = struct.unpack('ffff', data[:16])
            with self.mtx:
                self.atttude = (roll, pitch, yaw)
                self.height_amsl = h


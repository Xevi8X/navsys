import struct
import numpy as np
import socket
import threading
import time

class AHRSRecv(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.mtx = threading.RLock()
        self.time = -1.0
        self.attitude = (0.0, 0.0, 0.0)
        self.position = (0.0, 0.0, 0.0)
        self.velocity = (0.0, 0.0, 0.0)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 6000))
        
    def get(self):
        with self.mtx:
            return self.time, self.position, self.attitude, self.velocity
        
    def run(self):
        while True:
            data, _ = self.sock.recvfrom(40)
            t, x, y, z, roll, pitch, yaw, vx, vy, vz = struct.unpack('ffffffffff', data[:40])
            with self.mtx:
                self.time = t
                self.position = (x, y, z)
                self.attitude = (roll, pitch, yaw)
                self.velocity = (vx, vy, vz)


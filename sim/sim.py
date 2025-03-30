import time
import socket
import struct

from fg_output import FGOutput
from trajectory import *
import random

if __name__ == '__main__':
    fg_output = FGOutput()
    ned = NEDConverter(52.2669725, 20.9239028, 106)

    trajectory = TrajectoryForwardFlght(200, 25, 282, 15)
    # trajectory = TrajectoryForwardFlghtAccelerated(200, 282, 15, 30, 3, 10)
    # trajectory = TrajectoryFlatTurn(200, 25, 200)
    # trajectory = TrajectoryCoordinatedTurn(200, 25, 100)
    # trajectory = TrajectoryHeightChange(200, 25, 282, 50, 5)

    att_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    att_addr = ("127.0.0.1", 6000)


    height_deviation = 0.0
    attitude_deviation = math.radians(0.0)
    # height_deviation = 0.1
    # attitude_deviation = math.radians(0.02)


    time_start = time.time()
    while True:
        now =  time.time()
        time_elapsed = now - time_start

        x, y, z, phi, theta, psi, vx, vy, vz = trajectory.get_state(time_elapsed)
        lat, lon, alt = ned.to_lla(x, y, z)

        fg_output.set(lat, lon, alt, phi, theta, psi)

        random.gauss(0, )
        message = struct.pack('ffffffffff', 
                                time_elapsed, 
                                x, y, z + random.gauss(0, height_deviation),
                                phi + random.gauss(0, attitude_deviation),
                                theta + random.gauss(0, attitude_deviation),
                                psi  + random.gauss(0, attitude_deviation),
                                vx, vy, vz)
        att_sock.sendto(message, att_addr)

        time.sleep(0.02)
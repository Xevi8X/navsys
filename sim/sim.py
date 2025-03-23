import time
import socket
import struct

from fg_output import FGOutput
from trajectory import *

if __name__ == '__main__':
    fg_output = FGOutput()
    ned = NEDConverter(52.2669725, 20.9239028, 106)

    trajectory = TrajectoryForwardFlght(200, 25, 280)
    trajectory = TrajectoryFlatTurn(200, 25, 500)
    trajectory = TrajectoryCoordinatedTurn(200, 25, 300)

    att_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    att_addr = ("127.0.0.1", 6000)

    log = open("sim.csv", "w")
    log.write("time,x,y,z,vx,vy,vz,phi,theta,psi\n")



    time_start = time.time()
    while True:
        now =  time.time()
        time_elapsed = now - time_start

        x, y, z, phi, theta, psi, vx, vy, vz = trajectory.get_state(time_elapsed)
        lat, lon, alt = ned.to_lla(x, y, z)

        fg_output.set(lat, lon, alt, phi, math.radians(-15), psi)

        message = struct.pack('ffff', -z, phi, theta, psi)
        att_sock.sendto(message, att_addr)

        log.write(f"{now},{x},{y},{z},{vx},{vy},{vz},{phi},{theta},{psi}\n")

        time.sleep(0.02)
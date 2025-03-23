
from flightgear_python.fg_if import FDMConnection
import math


class FGOutput:
    def __init__(self):
        self.fdm_conn = FDMConnection(fdm_version=24)
        self.fdm_event_pipe = self.fdm_conn.connect_rx('localhost', 5501, self.fdm_callback)
        self.fdm_conn.connect_tx('localhost', 5502)
        self.fdm_conn.start()

    def fdm_callback(self, fdm_data, event_pipe):
        def deg2rad(deg):
            return deg * math.pi / 180.0 
    
        if event_pipe.child_poll():
            state = event_pipe.child_recv()
            fdm_data['lat_rad'] = deg2rad(state[0])
            fdm_data['lon_rad'] = deg2rad(state[1])
            fdm_data['alt_m'] = state[2]
            fdm_data['phi_rad'] = state[3]
            fdm_data['theta_rad'] = state[4]
            fdm_data['psi_rad'] = state[5]
        return fdm_data

    def set(self, latitude, longitude, altitude, roll, pitch, yaw):
        self.fdm_event_pipe.parent_send([latitude, longitude, altitude, roll, pitch, yaw])

    def deg2rad(self, deg):
        return deg * math.pi / 180.0 



if __name__ == '__main__':
    import time
    fg_output = FGOutput()
    roll = 0.0
    while True:
        fg_output.set(52.2669725, 20.9239028, 200, roll, 0, 280 * math.pi / 180.0)
        roll += 0.01
        time.sleep(0.02)

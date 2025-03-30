import math
import numpy as np

from camera import Camera
from opt_flow import OpticalFlow
from terrain import Terrain
from utils import wrap_pi, rot_X, rot_Y, rot_Z

class GroundSpeedEstimator:

    class Feature:
        def __init__(self, loc, confidence):
            self.loc = loc
            self.confidence = confidence

    class State:
        def __init__(self):
            self.valid : bool = False
            self.timestamp = 0.0
            self.rotation = np.eye(3)
            self.yaw = 0.0
            self.position = (0.0,0.0,0.0)
            self.features = {}

    class KF:
        def __init__(self):
            self.Q = np.eye(3) * 2.0
            self.R = np.eye(3) * 50.0
            self.reset()

        def reset(self):
            self.vel = np.zeros(3)
            self.P = 1e3 * self.Q
            self.NIS = 0.0

        def update(self, gs, dyaw, dt):
            f = np.array([[math.cos(dyaw), -math.sin(dyaw), 0], [math.sin(dyaw), math.cos(dyaw), 0], [0, 0, 1]])
            F = np.array([[-math.sin(dyaw), -math.cos(dyaw), 0], [math.cos(dyaw), -math.sin(dyaw), 0], [0, 0, 1]])

            vel_ = f @ self.vel
            P_ = F @ self.P @ F.T + self.Q * dt

            S = P_ + self.R
            
            K = P_ @ np.linalg.inv(S)

            y = gs - vel_
            self.vel = vel_ + K @ y
            self.P = (np.eye(3) - K) @ P_

            self.NIS = y @ np.linalg.inv(S) @ y

            return self.vel
        
        def get_covariance(self):
            return self.P.trace()
        
        def get_innov_covariance(self):
            return self.NIS

    def __init__(self):
        self.MIN_FEATURES = 3
        self.RESET_PERIOD = 1.0

        self.camera = Camera()
        self.opt_flow = OpticalFlow()
        self.terrain = Terrain()

        self.gs_kf = self.KF() 
        self.last_reset = 0.0
        self.last_state = self.State()

    def feed(self, timestamp, frame, position, attitude):
        if timestamp - self.last_reset > self.RESET_PERIOD:
            self.last_reset = timestamp
            self.opt_flow.reset()
            self.last_state.valid = False

        mask = np.ones(frame.shape[:2], dtype=np.uint8) * 255
        self.opt_flow.set_mask((mask))

        of_res = self.opt_flow.feed(frame)
        if of_res is None:
            self.last_state.valid = False
            return None
        
        (roll, pitch, yaw) = attitude
        
        state = self.State()
        state.valid = True
        state.timestamp = timestamp
        state.rotation = rot_Z(yaw) @ rot_Y(pitch) @ rot_X(roll)
        state.yaw = yaw
        state.position = np.array(position)

        features_shift = []
        features_bad = []
        
        for px_old, py_old, px_new, py_new in of_res:
            dir = self.camera.pixel_to_vec(px_new, py_new)
            ray = state.rotation @ dir


            downward = ray[2] / np.linalg.norm(ray)
            if math.fabs(math.acos(downward)) > math.radians(75):
                features_bad.append((px_new, py_new))

            loc = self.terrain.find_intersection(state.position, ray)
            feature = self.Feature(loc, downward)
            state.features[(px_new, py_new)] = feature

            if self.last_state.valid and (px_old, py_old) in self.last_state.features:
                features_shift.append((self.last_state.features[(px_old, py_old)], feature))

        self.opt_flow.remove_features(features_bad)

        dt = state.timestamp - self.last_state.timestamp
        dpos = state.position - self.last_state.position
        dyaw = wrap_pi(yaw - self.last_state.yaw)
        self.last_state = state

        if len(features_shift) < self.MIN_FEATURES:
            return None

        sum = np.zeros(3)
        confidence_sum = 0.0
        for prev_feature, feature in features_shift:
            sum += (feature.loc - prev_feature.loc - dpos) * feature.confidence
            confidence_sum += feature.confidence

        if dt <= 1e-6:
            return None

        gs = -sum / confidence_sum / dt

        if np.isnan(gs).any():
            return None
        
        gs_kf = self.gs_kf.update(gs, dyaw, dt)

        vel = np.linalg.norm(gs_kf)
        heading = math.atan2(gs_kf[1], gs_kf[0])
        
        with np.printoptions(precision=3, suppress=True):      
            print("Vel: ", vel, "Heading: ", math.degrees(heading))

        return gs_kf


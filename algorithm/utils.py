import numpy as np

def rot_X(roll):
    return np.array([[1, 0, 0], [0, np.cos(roll), -np.sin(roll)], [0, np.sin(roll), np.cos(roll)]])

def rot_Y(pitch):
    return np.array([[np.cos(pitch), 0, np.sin(pitch)], [0, 1, 0], [-np.sin(pitch), 0, np.cos(pitch)]])

def rot_Z(yaw):
    return np.array([[np.cos(yaw), -np.sin(yaw), 0], [np.sin(yaw), np.cos(yaw), 0], [0, 0, 1]])

def wrap_pi(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi
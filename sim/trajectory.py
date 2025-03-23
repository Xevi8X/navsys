
import math

class NEDConverter:
    def __init__(self, origin_lat, origin_lon, origin_alt):
        self.origin_lat_rad = math.radians(origin_lat)
        self.origin_lon_rad = math.radians(origin_lon)
        self.origin_alt = origin_alt

    def to_lla(self, x, y, z):
        R = 6378137.0
        lat = self.origin_lat_rad + (x / R)
        lon = self.origin_lon_rad + (y / (R * math.cos(self.origin_lat_rad)))
        return math.degrees(lat), math.degrees(lon), self.origin_alt - z
    

class TrajectoryForwardFlght:
    def __init__(self, altitude, speed, heading):
        self.altitude = altitude
        self.speed = speed
        self.heading = heading

    def get_state(self, time):
        x = self.speed * time * math.cos(math.radians(self.heading))
        y = self.speed * time * math.sin(math.radians(self.heading))
        z = -self.altitude
        phi = 0
        theta = 0
        psi = math.radians(self.heading)
        vx = self.speed * math.cos(math.radians(self.heading))
        vy = self.speed * math.sin(math.radians(self.heading))
        vz = 0
        return x, y, z, phi, theta, psi, vx, vy, vz
    
class TrajectoryFlatTurn:
    def __init__(self, altitude, speed, radius):
        self.altitude = altitude
        self.speed = speed
        self.turn_radius = radius

    def get_state(self, time):
        x = self.turn_radius * math.cos(self.speed * time / self.turn_radius)
        y = self.turn_radius * math.sin(self.speed * time / self.turn_radius)
        z = -self.altitude
        phi = 0
        theta = 0
        psi = (self.speed * time / self.turn_radius + math.pi / 2) % (2 * math.pi)
        vx = -self.speed * math.sin(self.speed * time / self.turn_radius)
        vy = self.speed * math.cos(self.speed * time / self.turn_radius)
        vz = 0
        return x, y, z, phi, theta, psi, vx, vy, vz
    
class TrajectoryCoordinatedTurn:
    def __init__(self, altitude, speed, radius):
        self.altitude = altitude
        self.speed = speed
        self.turn_radius = radius
        self.G = 9.81

    def get_state(self, time):
        x = self.turn_radius * math.cos(self.speed * time / self.turn_radius)
        y = self.turn_radius * math.sin(self.speed * time / self.turn_radius)
        z = -self.altitude
        phi = math.atan(self.speed * self.speed / (self.turn_radius * self.G))
        theta = 0
        psi = (self.speed * time / self.turn_radius + math.pi / 2) % (2 * math.pi)
        vx = -self.speed * math.sin(self.speed * time / self.turn_radius)
        vy = self.speed * math.cos(self.speed * time / self.turn_radius)
        vz = 0
        return x, y, z, phi, theta, psi, vx, vy, vz
